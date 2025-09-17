# === Imports ===
import os, json, re
from datetime import datetime
from typing import List, Tuple
from pathlib import Path

import numpy as np

# optional libraries
try:
    from sentence_transformers import SentenceTransformer
    HAVE_ST = True
except Exception:
    SentenceTransformer = None
    HAVE_ST = False

try:
    import faiss
    HAVE_FAISS = True
except Exception:
    faiss = None
    HAVE_FAISS = False

try:
    from langchain.schema import HumanMessage, AIMessage
    from langchain.llms.base import LLM
    HAVE_LC = True
except Exception:
    HAVE_LC = False

import gradio as gr
import tiktoken
from llama_cpp import Llama
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# === Global persona prompt ===
PERSONA_PROMPT = (
[PLACEHOLDER FOR YOUR PERSONA]
)

# === Helpers ===
def sanitize_input(user_input: str) -> str:
    user_input = re.sub(r"(?i)(assistant|system|user):", "", user_input)
    return user_input.strip()

def count_tokens_from_history(chat_history: List):
    encoding = tiktoken.get_encoding("gpt2")
    total = 0
    for msg in chat_history:
        total += len(encoding.encode(str(msg)))
    return total

def load_and_chunk_text(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 100):
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documents)

# === Llama-cpp wrapper ===
class LlamaCPP(LLM):
    model_path: str
    n_ctx: int = 8192
    n_threads: int = 4
    max_tokens: int = 512
    seed: int = 42

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._llm = Llama(
            model_path=self.model_path,
            n_ctx=self.n_ctx,
            n_threads=self.n_threads,
            seed=self.seed,
            verbose=False,
        )

    @property
    def _llm_type(self) -> str:
        return "llama_cpp"

    @property
    def _identifying_params(self):
        return {
            "model_path": self.model_path,
            "n_ctx": self.n_ctx,
            "n_threads": self.n_threads,
            "max_tokens": self.max_tokens,
            "seed": self.seed,
        }

    def _call(self, prompt: str, stop: List[str] = None) -> str:
        formatted_prompt = f"YourName: {prompt.strip()}\nModelName:"
        full_prompt = f"[INST] {PERSONA_PROMPT}\n\n{formatted_prompt} [/INST]"
        output = self._llm(full_prompt, max_tokens=self.max_tokens, stop=stop)
        return output["choices"][0]["text"].strip()

# === Main RAG App ===
class LocalRAGChatApp:
    def __init__(self, model_path: str):
        # Base LLM
        self.llm = LlamaCPP(model_path=model_path)

        # Memory and retrieval
        self.vectorstore = None
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.memory.chat_memory.add_message(AIMessage(content=PERSONA_PROMPT))

        # Chat tracking
        self.chat_chain = None
        self.chat_history: List[Tuple[str, str, str]] = []  # (timestamp, question, answer)
        self.summarized_history: List[str] = []  # keeps older chats in compressed form

    # --- File uploads ---
    def add_text_file(self, file_obj, mode="auto"):
        if file_obj is None or not hasattr(file_obj, "name"):
            return "⚠️ Invalid file input."

        new_chunks = load_and_chunk_text(file_obj.name)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        if self.vectorstore is None:
            self.vectorstore = FAISS.from_documents(new_chunks, embeddings)
        else:
            self.vectorstore.add_documents(new_chunks)

        self.chat_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            memory=self.memory,
            return_source_documents=False,
        )
        return f"✅ Added and indexed {len(new_chunks)} chunks."

    # --- Chat functions ---
    def chat(self, question: str) -> Tuple[str, int]:
        if self.chat_chain is None:
            return "⚠️ Please load a document first.", 0

        answer = self.chat_chain.run(question)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.chat_history.append((now, question, answer))
        self._summarize_old_history_if_needed()

        tokens_used = count_tokens_from_history(self.memory.chat_memory.messages)
        return answer, tokens_used

    def chat_multipass(self, question: str) -> Tuple[str, int]:
        if self.chat_chain is None:
            return "⚠️ Please load a document first.", 0

        first_answer = self.chat_chain.run(question)
        refinement_prompt = (
            f"Question: {question}\n"
            f"Initial Answer: {first_answer}\n"
            "Please improve or elaborate on the initial answer if needed."
        )
        refined_answer = self.llm(refinement_prompt)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.chat_history.append((now, question, refined_answer))
        self.memory.chat_memory.add_message(HumanMessage(content=question))
        self.memory.chat_memory.add_message(AIMessage(content=refined_answer))

        self._summarize_old_history_if_needed()
        tokens_used = count_tokens_from_history(self.memory.chat_memory.messages)
        return refined_answer, tokens_used

    # --- Summarization for old chat ---
    def _summarize_old_history_if_needed(self):
        total_tokens = count_tokens_from_history(self.memory.chat_memory.messages)
        if total_tokens > 7000:
            # Summarize oldest half of the chat
            old_msgs = self.memory.chat_memory.messages[:len(self.memory.chat_memory.messages)//2]
            summary = " ".join([m.content for m in old_msgs])
            self.summarized_history.append(summary[:1000])  # store compressed summary
            del self.memory.chat_memory.messages[:len(self.memory.chat_memory.messages)//2]

    # --- Save chat ---
    def save_chat(self, txt_file="chat_log.txt", json_file="chat_log.json"):
        if not self.chat_history:
            return "⚠️ No chat history to save."
        with open(txt_file, "a", encoding="utf-8") as f_txt, open(json_file, "a", encoding="utf-8") as f_json:
            for timestamp, q, a in self.chat_history:
                f_txt.write(f"[{timestamp}]\nQ: {q}\nA: {a}\n\n")
            json.dump(
                [{"timestamp": t, "question": q, "answer": a} for t, q, a in self.chat_history],
                f_json,
                ensure_ascii=False,
                indent=2,
            )
            f_json.write("\n")
        return f"✅ Chat saved to {txt_file} and {json_file}"

# === Gradio UI ===
  app = LocalRAGChatApp(model_path="mistral-7b-instruct-v0.1.Q4_K_M.gguf") # YOUR MODEL PATH

with gr.Blocks() as demo:
    gr.Markdown("## 🧠 Local RAG Chat with Mistral + LangChain + Token Counter")

    with gr.Row():
        file_input = gr.Files(label="📄 Upload .txt file(s)", file_types=[".txt"])
        load_button = gr.Button("📥 Load / Add File(s)")

    status = gr.Textbox(label="Status", interactive=False)
    chatbox = gr.Chatbot(label="💬 Chat History", type="messages")
    question = gr.Textbox(label="Ask a Question", placeholder="Type and press Enter...")
    multi_pass_toggle = gr.Checkbox(label="Use Multi-Pass for answers", value=False)
    token_usage = gr.Textbox(label="🧮 Token Usage", interactive=False)
    save_button = gr.Button("💾 Save Chat")

    def handle_load(files):
        if not files:
            return "⚠️ No files uploaded.", [], "", ""
        messages = []
        for file_obj in files:
            msg = app.add_text_file(file_obj)
            messages.append(msg)
        return " | ".join(messages), [], "", ""

    def handle_question(q, history, use_multi_pass):
        if not q or not q.strip():
            return history, "", ""
        q = sanitize_input(q)
        if use_multi_pass:
            answer, token_count = app.chat_multipass(q)
        else:
            answer, token_count = app.chat(q)
        history = history + [{"role": "user", "content": q}, {"role": "assistant", "content": answer}]
        token_warning = f"🧮 Token usage: {token_count} / 8192"
        if token_count > 7000:
            token_warning += " ⚠️ Approaching context limit!"
        return history, "", token_warning

    def handle_save():
        return app.save_chat()

    load_button.click(fn=handle_load, inputs=file_input, outputs=[status, chatbox, question, token_usage])
    question.submit(fn=handle_question, inputs=[question, chatbox, multi_pass_toggle], outputs=[chatbox, question, token_usage])
    save_button.click(fn=handle_save, outputs=status)

demo.launch(share=False, server_name="127.0.0.1", server_port=7869)
