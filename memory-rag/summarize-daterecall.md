# Features: 
### *Recall by date; automatic summarization, date-aware recall, token window management*

### 🔹 Core LLM Integration
- **Custom LangChain-compatible wrapper for `llama-cpp`**  
  - Configurable: `n_ctx`, `n_threads`, `max_tokens`, `seed`.  
  - Handles prompts with persona injection for consistent first-person style.  
  - `_call` method wraps the model and applies structured prompts.

### 🔹 Retrieval-Augmented Generation (RAG)
- **Document ingestion & chunking**  
  - Uses `TextLoader` + `RecursiveCharacterTextSplitter`.  
  - Supports `mode` flags: `'auto'`, `'dialogue'`, `'narrative'`.  
- **Vector store support**  
  - FAISS-based index built from HuggingFace embeddings (`all-MiniLM-L6-v2`).  
  - Incremental addition of multiple documents.

### 🔹 Memory & Context
- **Conversation buffer memory**  
  - Stores `HumanMessage` and `AIMessage` in LangChain `ConversationBufferMemory`.  
- **Token counting** via `tiktoken` for context window monitoring.  
- **Automatic summarization** of older messages when tokens approach a threshold.  
- **Date-aware recall**  
  - `recall_by_date` searches chat history, summarized history, and document content.

### 🔹 Chat Functionality
- **Single-pass chat** (`chat`) → returns answer + token usage.  
- **Multi-pass chat** (`chat_multipass`)  
  - First draft via retrieval chain.  
  - Second pass refinement for style/clarity.  
- **Chat logging**  
  - Saves to `.txt` and `.json`.  
- **Date recall** → can respond to YYYY-MM-DD queries directly.  

### 🔹 Input & Output Handling
- **Sanitizes user input** (`sanitize_input`) to remove impersonation or role injection attempts.  
- Supports `.txt` file uploads for content indexing.  

### 🔹 Gradio UI
- File upload, chatbot, token usage display, multi-pass toggle, save chat.  
- Local server launch (`127.0.0.1:7875`) with simple interface.  
- Handles system messages for date-recall outputs.  

### 🔹 Extra Utilities
- Maintains `summarized_history` for older chats to manage token limits.  
- Extensible and modular design for future prompt, memory, or indexing improvements.  
