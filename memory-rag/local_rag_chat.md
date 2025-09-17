# Feature Summary

## Core Components
- **LLM Backend:** `LlamaCPP` wrapper for `llama_cpp` models (e.g., Mistral 7B).  
- **Vector Store:** FAISS used for semantic retrieval of document chunks.  
- **Embeddings:** HuggingFace `all-MiniLM-L6-v2` for text embedding.  
- **Memory:** `ConversationBufferMemory` from LangChain to maintain chat history.  

## Text Handling
- Load `.txt` files with `TextLoader`.
- Chunk documents using `RecursiveCharacterTextSplitter` with configurable `chunk_size` and `chunk_overlap`.
- Incremental addition of new documents to the FAISS vector store.

## Retrieval-Augmented Generation (RAG)
- **ConversationalRetrievalChain:**  
  - Retrieves top `k` relevant chunks from vector store.  
  - Combines retrieved context with live LLM response generation.  
- Supports **multi-pass refinement**:
  - First pass: retrieval + LLM generation.  
  - Second pass: direct LLM refinement of initial answer for improved clarity/coherence.

## Chat Features
- Tracks conversation history with timestamps: `(timestamp, question, answer)`.  
- Token counting using `tiktoken` (`gpt2` encoding) for context management.  
- Multi-pass optional toggle for each query.  

## Persistence
- Save chat history to both `.txt` and `.json` files (appends to existing files).  

## UI (Gradio)
- Upload `.txt` files for semantic indexing.  
- Chat interface with optional multi-pass toggle.  
- Displays token usage and warnings if approaching context limits.  
- Buttons for loading files, submitting questions, and saving chat.  

## Design Notes
- Multi-pass RAG improves answer quality without increasing token usage excessively.  
- Vectorstore + memory combination enables coherent, context-aware multi-turn dialogue.  
- Modular design allows swapping LLM models, embeddings, or vectorstores with minimal changes.

---
