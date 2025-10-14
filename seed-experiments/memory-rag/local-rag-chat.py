"""


persona_intro = (
    " [YOUR INTRO] "

)

self.memory.chat_memory.add_message(AIMessage(content=persona_intro))
self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

"""

import gradio as gr
import os
import json
import tiktoken  
from typing import List, Tuple
from datetime import datetime
from langchain.schema import HumanMessage, AIMessage
from langchain.llms.base import LLM 
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from llama_cpp import Llama


PERSONA_PROMPT = (
    "[YOUR PERSONA]"
)

# --- Llama-cpp wrapper (LangChain-compatible) ---

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
        full_prompt = f"<s>[INST] {PERSONA_PROMPT}\n\n{prompt} [/INST]"
        output = self._llm(full_prompt, max_tokens=self.max_tokens, stop=stop)
        return output["choices"][0]["text"].strip()



# --- Load and split text ---

def load_and_chunk_text(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 100):
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documents)


# --- Token counting ---

def count_tokens_from_history(chat_history: List):
    encoding = tiktoken.get_encoding("gpt2")
    total = 0
    for msg in chat_history:
        total += len(encoding.encode(str(msg)))
    return total


# --- Main RAG app ---

class LocalRAGChatApp:
    def __init__(self, model_path: str):
        self.llm = LlamaCPP(model_path=model_path)
        self.vectorstore = None
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        persona_intro = (
        "YOUR INTRO... ETC"
)

        self.memory.chat_memory.add_message(AIMessage(content=persona_intro))
        self.chat_chain = None
        self.chat_history: List[Tuple[str, str, str]] = []  # (timestamp, question, answer)

    def add_text_file(self, file_obj):
        if file_obj is None or not hasattr(file_obj, "name"):
            return "⚠️ Invalid file input."

        new_chunks = load_and_chunk_text(file_obj.name)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        if self.vectorstore is None:
            self.vectorstore = FAISS.from_documents(new_chunks, embeddings)
        else:
            self.vectorstore.add_documents(new_chunks)

        # Build or update the chain
        self.chat_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            memory=self.memory,
            return_source_documents=False,
        )
        return f"✅ Added and indexed {len(new_chunks)} chunks."
    
    
    def chat(self, question: str) -> Tuple[str, int]:
        if self.chat_chain is None:
            return "⚠️ Please load a document first.", 0

        answer = self.chat_chain.run(question)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.chat_history.append((now, question, answer))

        tokens_used = count_tokens_from_history(self.memory.chat_memory.messages)
        return answer, tokens_used
    
    def chat_multipass(self, question: str) -> Tuple[str, int]:
        if self.chat_chain is None:
            return "⚠️ Please load a document first.", 0

        # First pass: initial answer using the full retrieval chain
        first_answer = self.chat_chain.run(question)

        # Compose prompt for second pass to refine the first answer
        refinement_prompt = (
            f"Question: {question}\n"
            f"Initial Answer: {first_answer}\n"
            "Please improve or elaborate on the initial answer if needed."
    )

        # Second pass: refinement via direct LLM call (no retrieval)
        refined_answer = self.llm(refinement_prompt)

        # Log final refined answer
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.chat_history.append((now, question, refined_answer))

        # Store the conversation in memory
        self.memory.chat_memory.add_message(HumanMessage(content=question))
        self.memory.chat_memory.add_message(AIMessage(content=refined_answer))

        tokens_used = count_tokens_from_history(self.memory.chat_memory.messages)

        return refined_answer, tokens_used




    def save_chat(self, txt_file="chat_log.txt", json_file="chat_log.json"):
        if not self.chat_history:
            return "⚠️ No chat history to save."

        # Append to txt and json
        with open(txt_file, "a", encoding="utf-8") as f_txt, open(json_file, "a", encoding="utf-8") as f_json:
            for timestamp, q, a in self.chat_history:
                f_txt.write(f"[{timestamp}]\nQ: {q}\nA: {a}\n\n")
            json.dump(
                [
                    {"timestamp": t, "question": q, "answer": a}
                    for t, q, a in self.chat_history
                ],
                f_json,
                ensure_ascii=False,
                indent=2,
            )
            f_json.write("\n")

        return f"✅ Chat saved to {txt_file} and {json_file}"


# --- Gradio UI ---

app = LocalRAGChatApp(model_path="/mistral-7b-instruct-v0.1.Q4_K_M.gguf") # YOUR PATH

with gr.Blocks() as demo:
    gr.Markdown("## 🧠 Local RAG Chat with Mistral + LangChain + Token Counter")

    with gr.Row():
        file_input = gr.Files(label="📄 Upload .txt file(s)", file_types=[".txt"])
        load_button = gr.Button("📥 Load / Add File(s)")

    status = gr.Textbox(label="Status", interactive=False)
    chatbox = gr.Chatbot(label="💬 Chat History")
    question = gr.Textbox(label="Ask a Question", placeholder="Type and press Enter...")
    use_multipass = gr.Checkbox(use_multipass = gr.Checkbox(label="Use Multi-Pass for answers", value=False)
, value=False)
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

        if use_multi_pass:
            answer, token_count = app.chat_multipass(q)
        else:
            answer, token_count = app.chat(q)

        history = history + [(q, answer)]
        token_warning = f"🧮 Token usage: {token_count} / 8192"
        if token_count > 7000:
            token_warning += " ⚠️ Approaching context limit!"

        return history, "", token_warning


    def handle_save():
        return app.save_chat()

    load_button.click(fn=handle_load, inputs=file_input, outputs=[status, chatbox, question, token_usage])
    
    question.submit(
    fn=handle_question,
    inputs=[question, chatbox, multi_pass_toggle],
    outputs=[chatbox, question, token_usage]
)


demo.launch(share=False, server_name="127.0.0.1", server_port=7876)

