# === Imports ===
import os
import json
import re
import tiktoken  # For token counting
from typing import List, Tuple
from datetime import datetime
from langchain.schema import HumanMessage, AIMessage
from langchain.llms.base import LLM  # your base class for custom LLMs
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from llama_cpp import Llama

import gradio as gr

# --- Global persona prompt ---

PERSONA_PROMPT = """PLACEHOLDER: define your system prompt."""


def sanitize_input(user_input: str) -> str:
    # Remove attempts to impersonate Ocean or inject roles
    user_input = re.sub(r"(?i)(ocean|assistant|system|user):", "", user_input)
    return user_input.strip()

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
        formatted_prompt = f"Breeze: {prompt.strip()}\nOcean:"
        full_prompt = f"[INST] {PERSONA_PROMPT}\n\n{formatted_prompt} [/INST]"
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
        
        # Add the persona intro to memory ONCE at startup
        self.memory.chat_memory.add_message(AIMessage(content=PERSONA_PROMPT))

        self.chat_chain = None
        self.chat_history: List[Tuple[str, str, str]] = []  # (timestamp, question, answer)

        # Additional structures for summarization & date-aware recall
        # summarized_history: list of dicts {"ts_range": "2025-09-01..2025-09-02", "summary": "..."}
        self.summarized_history: List[dict] = []

    # -------------------------
    # File upload + index
    # -------------------------
    def add_text_file(self, file_obj, mode="auto"):
        """
        Adds and indexes uploaded .txt files.
        mode: 'auto' (detect), 'dialogue', 'narrative' (keeps legacy behaviour compatible)
        """
        if file_obj is None or not hasattr(file_obj, "name"):
            return "⚠️ Invalid file input."

        # load & chunk
        new_chunks = load_and_chunk_text(file_obj.name)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        if self.vectorstore is None:
            self.vectorstore = FAISS.from_documents(new_chunks, embeddings)
        else:
            self.vectorstore.add_documents(new_chunks)

        # rebuild chat_chain or initialize
        self.chat_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            memory=self.memory,
            return_source_documents=False,
        )

        # store a lightweight timestamp tag in summarized_history for date-based lookup if possible
        try:
            # attempt to infer a date from filename or file content first lines
            fn = os.path.basename(file_obj.name)
            date_match = re.search(r"(\d{4}-\d{2}-\d{2})", fn)
            if not date_match:
                with open(file_obj.name, "r", encoding="utf-8", errors="ignore") as f:
                    head = f.read(2000)
                date_match = re.search(r"(\d{4}-\d{2}-\d{2})", head)
            date_tag = date_match.group(1) if date_match else None
            if date_tag:
                # record an index marker summary for quick date recall
                self.summarized_history.append({"ts_range": date_tag, "summary": f"Uploaded document: {fn}"})
        except Exception:
            pass

        return f"✅ Added and indexed {len(new_chunks)} chunks."

    # -------------------------
    # Summarization helpers
    # -------------------------
    def _summarize_old_history_if_needed(self, token_threshold: int = 7000):
        """
        If token usage from ConversationBufferMemory is approaching the model window,
        summarize older half of messages into a first-person summary and keep it in summarized_history.
        """
        total_tokens = count_tokens_from_history(self.memory.chat_memory.messages)
        if total_tokens <= token_threshold:
            return

        # choose oldest half of messages to summarize
        n = len(self.memory.chat_memory.messages) // 2
        if n <= 0:
            return

        old_msgs = self.memory.chat_memory.messages[:n]
        combined_text = "\n".join([m.content for m in old_msgs])

        # create a summarization prompt for the LLM
        summary_prompt = (
            "Summarize this earlier conversation in first-person. "
            "Keep dates and key events, be concise, and do NOT reveal chain-of-thought.\n\n"
            f"{combined_text}\n\nSummary:"
        )

        # Use the LLM wrapper to generate a summary (use _call to be safe)
        try:
            summary_text = self.llm._call(summary_prompt)
        except Exception:
            # fallback: simple truncate if llm fails
            summary_text = combined_text[:800]

        # determine a timestamp range from the oldest and newest messages summarized
        try:
            ts_first = old_msgs[0].content[:19]  # if messages include timestamps in content
        except Exception:
            ts_first = None
        # record summarized history with optional range
        self.summarized_history.append({
            "ts_range": ts_first or "older",
            "summary": summary_text
        })

        # delete the old messages from ConversationBufferMemory to free tokens
        del self.memory.chat_memory.messages[:n]

    # -------------------------
    # Date recall
    # -------------------------
    def recall_by_date(self, date_str: str) -> str:
        """Return memories related to a specific date (YYYY-MM-DD)."""

        results = []

        # 1. Check detailed chat_history (unsummarized recent chats)
        for timestamp, q, a in self.chat_history:
            if timestamp.startswith(date_str):
                results.append(f"[{timestamp}] Q: {q}\nA: {a}")

        # 2. Check summarized_history (search summary text and ts_range)
        for idx, s in enumerate(self.summarized_history):
            ts_range = s.get("ts_range", "")
            summary_text = s.get("summary", "")
            # match either explicit ts_range or substring in summary_text
            if date_str == ts_range or date_str in summary_text:
                results.append(f"[Summary {idx} | {ts_range}] {summary_text}")

        # 3. Check uploaded documents via vectorstore (search by date string)
        try:
            if self.vectorstore:
                retriever = self.vectorstore.as_retriever(search_kwargs={"k": 8})
                docs = retriever.get_relevant_documents(date_str)
                for d in docs:
                    content = getattr(d, "page_content", str(d))[:800]
                    if date_str in content:
                        results.append(f"[Doc] {content}...")
        except Exception:
            # If retriever call fails, fall back to no-op
            pass

        if not results:
            return f"⚠️ No memories found for {date_str}."
        return "\n\n".join(results)

    # -------------------------
    # Chat functions
    # -------------------------
    def chat(self, question: str) -> Tuple[str, int]:
        # Detect YYYY-MM-DD pattern and answer via recall_by_date first
        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", question)
        if date_match:
            date_str = date_match.group(1)
            recall = self.recall_by_date(date_str)
            return recall, 0

        if self.chat_chain is None:
            return "⚠️ Please load a document first.", 0

        answer = self.chat_chain.run(question)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.chat_history.append((now, question, answer))

        # add to ConversationBufferMemory for continuity
        try:
            self.memory.chat_memory.add_message(HumanMessage(content=question))
            self.memory.chat_memory.add_message(AIMessage(content=answer))
        except Exception:
            # If memory operations fail silently, we still keep chat_history
            pass

        # summarize if needed
        self._summarize_old_history_if_needed()

        tokens_used = count_tokens_from_history(self.memory.chat_memory.messages)
        return answer, tokens_used

    def chat_multipass(self, question: str) -> Tuple[str, int]:
        # Date-intercept for multipass as well
        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", question)
        if date_match:
            date_str = date_match.group(1)
            recall = self.recall_by_date(date_str)
            return recall, 0

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

        try:
            self.memory.chat_memory.add_message(HumanMessage(content=question))
            self.memory.chat_memory.add_message(AIMessage(content=refined_answer))
        except Exception:
            pass

        self._summarize_old_history_if_needed()
        tokens_used = count_tokens_from_history(self.memory.chat_memory.messages)
        return refined_answer, tokens_used

    # -------------------------
    # Save chat
    # -------------------------
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


# --- Gradio UI ---

app = LocalRAGChatApp(model_path="/mistral-7b-instruct-v0.1.Q4_K_M.gguf") # YOUR MODEL PATH

with gr.Blocks() as demo:
    gr.Markdown("## 🧠 ⏰ Local RAG Chat with Mistral + LangChain + Token Counter")

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

        # If the answer is a date-recall (no tokens), show as system block
        if token_count == 0 and re.search(r"\d{4}-\d{2}-\d{2}", q):
            # Present recall output directly (not adding to chat history)
            return history + [{"role": "system", "content": answer}], "", ""

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

demo.launch(share=False, server_name="127.0.0.1", server_port=7875)
