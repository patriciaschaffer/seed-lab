# Features

### 🔹 Core LLM Integration
- **Custom LangChain-compatible wrapper for `llama-cpp`**  
  - Configurable parameters: `temperature`, `top_k`, `top_p`, `repeat_penalty`, `n_ctx`, `n_threads`, `seed`.  
  - Adds persona prompt injection into every call.  
  - Exposes `_llm_type` and `_identifying_params` for LangChain integration.

### 🔹 Retrieval-Augmented Generation (RAG)
- **Document loading & chunking**  
  - Uses `TextLoader` + `RecursiveCharacterTextSplitter` for flexible chunk sizes and overlaps.  
- **Vector store support**  
  - FAISS-based index built from HuggingFace embeddings (`all-MiniLM-L6-v2`).  
  - Supports adding multiple documents incrementally.  
- **Conversational Retrieval Chain**  
  - Integrates memory + retrieval + custom LLM for contextual Q&A.

### 🔹 Memory & Context
- **Conversation buffer memory** (`ConversationBufferMemory`)  
  - Stores dialogue history as LangChain `HumanMessage`/`AIMessage`.  
- **Token usage counter**  
  - Uses `tiktoken` to calculate approximate token usage.  
  - Warns when approaching context window limit.  

### 🔹 Chat Functionality
- **Single-pass chat** (`chat`) → Returns answer + token count.  
- **Multi-pass refinement** (`chat_multipass`)  
  - First draft via retrieval chain.  
  - Second pass refinement prompt for stylistic adjustments.  
  - Supports persona-driven responses.  
- **Chat logging**  
  - Saves conversations in both `.txt` (readable log) and `.json` (structured).  

### 🔹 Input & Output Handling
- **Sanitization of user input**  
  - Strips role labels (`assistant:`, `user:`, etc.).  
- **Persona prompt placeholder**  
  - Centralized variable for injecting a custom persona/voice.  

### 🔹 Gradio UI
- **Interactive UI with `Blocks`**  
  - File upload for `.txt` documents.  
  - Chatbot component with live history.  
  - Temperature slider with dynamic label updates.  
  - Toggle for enabling multi-pass refinement.  
  - Token usage display with warnings.  
  - Save button for exporting chat logs.  
- **Callbacks & live updates**  
  - Real-time persona-adjusted responses with token tracking.  
  - Automatic update of displayed model temperature.  
- **Configurable server**  
  - Runs locally on `127.0.0.1:7883`, no external sharing by default.  

### 🔹 Extra Utilities
- **Graceful shutdown** with `atexit` hook to close the Llama model cleanly.  
- **Extensible design** → Persona prompt, embeddings, chunking, and refinement strategy are modular and customizable.  






