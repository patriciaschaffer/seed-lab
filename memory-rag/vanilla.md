## Features

### Retrieval-Augmented Generation (RAG)
- Upload `.txt` files via UI.
- Automatically chunked with `RecursiveCharacterTextSplitter`.
- Embedded using **HuggingFaceEmbeddings** (`all-MiniLM-L6-v2`).
- Indexed into a **FAISS** vectorstore.
- Retrieval via **ConversationalRetrievalChain** for contextual answers.

### Chat & Memory
- Dual chat modes:
  - **Single-pass**: Direct response from the chain.
  - **Multi-pass**: Initial response + refinement step.
- Persistent memory with **ConversationBufferMemory**.
- Automatic **summarization of old history** when token usage > 7000, to preserve long-term context.

### Token Tracking
- Uses **tiktoken** for accurate token counting.
- Real-time usage displayed in UI, with warnings when nearing context limit (8192).

### 💾 Persistence
- Save conversations in both `.txt` and `.json` formats.
- Chat history includes timestamped user/assistant exchanges.

### Custom Llama.cpp Wrapper
- Integrated `LlamaCPP` class extending LangChain’s `LLM`.
- Custom call formatting:
  - Injects persona prompt.
  - Structures dialogue as `User: … \n Model:`.
- Configurable parameters: context size, max tokens, threads, seed.

### Gradio Interface
- File upload & indexing.
- Chatbox for conversation history.
- Token usage display.
- Toggle for **multi-pass answers**.
- Save chat button.

### ⚙️ Optional Dependencies
- **sentence-transformers** (for embeddings).
- **faiss** (for vector search).
- **langchain** (for schema/messages & conversational chain).
- Graceful fallback if not installed.

---
