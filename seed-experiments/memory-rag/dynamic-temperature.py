# Feel free to adapt to your use case. Write your own PERSONA_PROMPT

import gradio as gr
import os
import json
import re
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


# --- Global persona prompt ---

PERSONA_PROMPT = (
"""
PLACEHOULDER: craft your own, carefully
"""
)


def sanitize_input(user_input: str) -> str:
   
    user_input = re.sub(r"(?i)(assistant|system|user):", "", user_input)
    return user_input.strip()

# --- Llama-cpp wrapper (LangChain-compatible) ---

class LlamaCPP(LLM):
    model_path: str
    n_ctx: int = 8192
    n_threads: int = 4
    max_tokens: int = 512
    seed: int = 42

    # Feel free to play with parameters
    temperature: float = 0.85
    top_k: int = 40
    top_p: float = 0.9
    repeat_penalty: float = 1.15

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._llm = Llama(
            model_path=self.model_path,
            n_ctx=self.n_ctx,
            n_threads=self.n_threads,
            seed=self.seed,
            temperature=self.temperature,
            top_k=self.top_k,
            top_p=self.top_p,
            repeat_penalty=self.repeat_penalty,
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
        full_prompt = f"[INST] Breeze: {prompt.strip()}\nOcean:\n{PERSONA_PROMPT} [/INST]"

        output = self._llm(
            full_prompt,
            max_tokens=self.max_tokens,
            stop=stop,
            temperature=self.temperature,   
            top_k=self.top_k,
            top_p=self.top_p,
            repeat_penalty=self.repeat_penalty,
        )
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
    def __init__(
        self,
        model_path: str,
        temperature: float = 0.85,
        top_k: int = 40,
        top_p: float = 0.9,
        repeat_penalty: float = 1.15
    ):
        self.llm = LlamaCPP(
            model_path=model_path,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            repeat_penalty=repeat_penalty,
        )
        self.vectorstore = None
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        persona_intro = (
            "[PLACEHOLDER]" # Your persona intro here
        )
        self.memory.chat_memory.add_message(AIMessage(content=persona_intro))
        self.chat_chain = None
        self.chat_history = []

    def add_text_file(self, file_obj):
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

        first_answer = self.chat_chain.run(question)

        refinement_prompt = (
        # Adjust to your use case
            f"You are (...)\n"
            f"Speak(...)\n"
            f"Patricia just asked: {question}\n"
            f"You first said: {first_answer}\n"
            f"Now revise or expand it with warmth and style, keeping it fun and personal.\n"
            f"Persona:"
        )

        refined_answer = self.llm(refinement_prompt)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.chat_history.append((now, question, refined_answer))

        self.memory.chat_memory.add_message(HumanMessage(content=question))
        self.memory.chat_memory.add_message(AIMessage(content=refined_answer))

        tokens_used = count_tokens_from_history(self.memory.chat_memory.messages)
        return refined_answer, tokens_used

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


# --- Initialize your app ---
app = LocalRAGChatApp(
    model_path="/mistral-7b-instruct-v0.1.Q4_K_M.gguf", # Your model path and settings
    temperature=0.85,
    top_k=40,
    top_p=0.9,
    repeat_penalty=1.15
)

# --- Gradio UI for LocalRAGChatApp ---
with gr.Blocks() as demo:
    gr.Markdown("## ☁🤖 Local RAG Chat with Mistral + LangChain + Token Counter")

    # --- Temperature Row ---
    with gr.Row():
        temperature_slider = gr.Slider(
            minimum=0.1, maximum=1.0, step=0.05, value=0.85,
            label="Set Temperature"
        )
        temperature_label = gr.Textbox(
            value=f"Current Temperature: {temperature_slider.value:.1f}",
            interactive=False,
            label="Temperature Display"
        )

    # --- File Upload Row ---
    with gr.Row():
        file_input = gr.Files(label="📄 Upload .txt file(s)", file_types=[".txt"])
        load_button = gr.Button("📥 Load / Add File(s)")

    # --- Chat Components ---
    status = gr.Textbox(label="Status", interactive=False)
    chatbox = gr.Chatbot(label="💬 Chat History", type="messages")
    question = gr.Textbox(label="Ask a Question", placeholder="Type and press Enter...")
    multi_pass_toggle = gr.Checkbox(label="Use Multi-Pass for answers", value=False)
    token_usage = gr.Textbox(label="🧮 Token Usage", interactive=False)
    save_button = gr.Button("💾 Save Chat")

    # --- Callbacks ---
    def handle_load(files):
        if not files:
            return "⚠️ No files uploaded.", [], "", ""
        messages = [app.add_text_file(f) for f in files]
        return " | ".join(messages), [], "", ""

    def handle_question(q, history, use_multi_pass, temp):
        if not q or not q.strip():
            return history, "", ""
        q = sanitize_input(q)
        app.llm.temperature = temp

        if use_multi_pass:
            answer, token_count = app.chat_multipass(q)
        else:
            answer, token_count = app.chat(q)

        model_reply = f"Model [🌡️{temp:.1f}]: {answer}"

        history = history + [
            {"role": "user", "content": q},
            {"role": "assistant", "content": model_reply}
        ]

        token_warning = f"🧮 Token usage: {token_count} / 8192"
        if token_count > 7000:
            token_warning += " ⚠️ Approaching context limit!"

        return history, "", token_warning

    def handle_save():
        return app.save_chat()

    # --- Live temperature label + last message update ---
    def update_temp_label(temp, history):
        temp_label = f"Current Temperature: {temp:.1f}"
        if history:
            last_msg = history[-1]
            if last_msg["role"] == "assistant" and "Persona_Name [" in last_msg["content"]: # Add your model's name
                updated_content = re.sub(r"🌡️\d+\.?\d*", f"🌡️{temp:.1f}", last_msg["content"])
                history[-1]["content"] = updated_content
        return temp_label, history

    # --- Event bindings ---
    temperature_slider.change(
        fn=update_temp_label,
        inputs=[temperature_slider, chatbox],
        outputs=[temperature_label, chatbox]
    )
    load_button.click(fn=handle_load, inputs=file_input, outputs=[status, chatbox, question, token_usage])
    question.submit(fn=handle_question,
                    inputs=[question, chatbox, multi_pass_toggle, temperature_slider],
                    outputs=[chatbox, question, token_usage])
    save_button.click(fn=handle_save, outputs=status)

# --- Optional: cleanly close Llama at exit ---
import atexit
atexit.register(lambda: app.llm._llm.close() if app.llm._llm is not None else None)

# --- Launch Gradio ---
demo.launch(share=False, server_name="127.0.0.1", server_port=7883)
