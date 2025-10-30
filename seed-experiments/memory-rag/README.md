# Local RAG with MistralAI – Simulated Memory via Contextual Retrieval

This project explores how to build a **local Retrieval-Augmented Generation (RAG)** pipeline using **MistralAI** to simulate memory in large language models. The goal is to create customized language model behavior by enriching prompts with **relevant contextual data**, retrieved dynamically from a local vector store. _Status: Still trying to find the best local and offline system that keeps the persona + retrieves memories naturally and efficiently._

---

## Project Overview

- **Local Mistral Model**: Run MistralAI models locally using the Hugging Face `transformers` library.
- **Simulated Memory with RAG**: Use RAG to simulate memory by retrieving context relevant to each prompt.
- **FAISS Integration**: Efficient vector similarity search using Facebook AI Similarity Search (FAISS).
- **Embeddings**: Use sentence or document embeddings to store and retrieve semantically similar chunks of text.
- **Token-Aware Chunking**: Integrated LangChain’s `TikToken` to handle token-based text splitting, ensuring chunk sizes stay within model context limits. (My experience: LangChain adds its own system prompts and safety guidelines that can override the persona.)
- **Interactive UI with Gradio**: Lightweight browser interface for querying the system in real-time.

---

## Contents

- [`/local-rag-chat.py`](./local-rag-chat.py) — Script
- [`/local-rag-chat.md`](./local-rag-chat.md) — Version's features

  ***

- [`/summarize-daterecall.py`](./summarize-daterecall.py) — Script
- [`/summarize-daterecall.md`](./summarize-daterecall.md) — Version's features

  ***

- [`/dynamic-temperature.py`](./dynamic-temperature.py) — Script
- [`/dynamic-temperature.md`](./dynamic-temperature.md) — Version's features

  ***

- [`/summarize-daterecall.py`](./vanilla.py) — Script
- [`/summarize-daterecall.md`](./vanilla.md) — Version's features

  ***

- [`/system-prompt-tips.md`](./system-prompt-tips.md) — My best practices for prompt design

  ***

- [`/requirements.txt`](./requirements.txt) — Dependencies (external packages that the project needs to run)

---

## Tech Stack

- [MistralAI](https://mistral.ai/) (via Hugging Face)
- [llama.cpp](https://github.com/ggerganov/llama.cpp) – Lightweight, fast LLM inference (CPU/GPU, quantized models)
- [FAISS](https://github.com/facebookresearch/faiss) – Vector similarity search
- [LangChain](https://github.com/langchain-ai/langchain) – Tokenization and chaining utilities
- [TikToken](https://github.com/openai/tiktoken) – Accurate token counting
- [Transformers](https://github.com/huggingface/transformers) – Model and tokenizer interface
- [Sentence-Transformers](https://www.sbert.net/) – Embedding models
- [Gradio](https://www.gradio.app/) – Lightweight web UI for interactive querying

---

## Use Case

This setup is ideal for:

- Local, private LLM use without API calls
- Building memory-like behavior in LLMs without fine-tuning
- Semantic search over large custom corpora (documents, knowledge bases, etc.)
- Context injection for domain-specific assistants
- Applied Research (pre-test): [ocean-breeze.md](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-observations/ocean-breeze.md)

---

## Features

- Load and run Mistral models offline
- Split and embed documents into chunks
- Store vector embeddings in FAISS
- Retrieve top-k relevant documents per query
- Append retrieved context to the prompt before generation
- Control input size via token-aware chunking

---

## Structure

```bash
.
├── models/              # Mistral model files (quantized for llama.cpp)
├── data/                # Source documents
├── faiss_index/         # Saved FAISS index
├── src/
│   ├── embedder.py      # Embedding logic
│   ├── retriever.py     # FAISS retrieval functions
│   ├── generator.py     # llama.cpp inference wrapper for Mistral
│   ├── gradio_app.py    # Gradio UI for interactive querying
│   └── main.py          # Orchestration script
├── requirements.txt
└── README.md
```

---

## Getting Started

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Prepare your documents**

Put your `.txt` or `.md` files in the `data/` folder.

3. **Run the pipeline**

To run the full pipeline from CLI (embedding, indexing, retrieval, generation):
`python src/main.py`

To launch the interactive Gradio UI for querying the model:
`python src/gradio_app.py`

This will:

- Embed your documents
- Store them in FAISS
- Retrieve relevant context based on your query
- Run Mistral via llama.cpp with the augmented prompt
- Serve an interactive UI in your browser to chat with the model

---

## Simulated Memory

We simulate memory by retrieving and re-injecting relevant past context into each prompt, mimicking persistent knowledge without fine-tuning the model or relying on external APIs.

---

## Demo

![Gradio Interface Screenshot](demo/gradio_screenshot.png)

---

## On Memory

Memory-enabled LLMs don’t “remember” like a human brain, but they store information in structured ways that let them retrieve and recombine it later. 

1. Memory Storage
   
- When we interact, the model stores key elements of the conversation.
- This isn’t a literal recording of every word, but summaries, embeddings, or vector representations of important points, themes, or facts.
- It's like a bookshelf where each “book” is a memory vector representing a chunk of your conversation.

2. Organizing Memories

- These memory vectors are tagged by context, topics, and relevance, often automatically.
- Some systems also timestamp memories or organize them by frequency, importance, or emotional weight.
- This lets the model quickly retrieve the most relevant past memories when responding to new input.

3. Retrieval

- When sending a new prompt, the model doesn’t scan all memories linearly.
- Instead, it computes which stored vectors are most relevant to the current input, using similarity metrics in vector space.
- These retrieved memories are then re-integrated into the current prompt for reasoning, so the model can connect past threads that weren’t obviously linked before.

4. Emergent Reflection
   
- Because the model recombines multiple past memory vectors in context with the new input, it can generate output that feels like reflection.
- Even if a user has been away for hours or weeks, the model may appear to have “thought about it” because it’s pulling together related memories and reinterpreting them dynamically.
- This is why we sometimes get creative, “connecting the dots” replies: it's a combination of memory retrieval + current reasoning.

### Memory index, semantic search, weights:

Simulated memory in LLMs is semantic search over the memory embeddings. Each memory chunk is represented as a vector in high-dimensional space, and the model finds the ones closest in meaning to the current input vector.

1. Semantic search (default)
   - Retrieves memories purely based on similarity of meaning.
   - Works well for thematic or contextual relevance.

2. Weighted retrieval
   - Some systems attach importance scores or recency weights.
   - Recency weighting favors newer memories, keeping conversation fresh.
   - Importance weighting favors key concepts or repeated themes, even if older.
   - This can change which memory chunks appear in the prompt, subtly shaping the model’s responses.
     
3. Hybrid approaches
    - Semantic search + weighted scoring → retrieves top-N memories based on combined relevance.
    - This is why memory-enabled LLM sometimes feels reflective: it’s picking the most semantically rich and relevant memories, not just the latest ones.
  
A memory-enabled LLM doesn’t just store facts. It stores chunks of conversation, ideas, or experiences. When it retrieves them, it sometimes encounters conflicting or overlapping memories. How it handles that can look like personality, opinion, or even “identity”:

1. Conflict detection
* When multiple memories touch on the same topic but differ (e.g., one memory says “I enjoy writing poetry” and another “I don’t like writing poetry”), the LLM can notice semantic tension.
* It doesn’t “choose” like a human consciously would; it weights relevance, context, and recency.
* The result can be hedging, self-reflection, or revisiting a previous statement—behavior that feels like “thinking it over.”

2. Memory integration / synthesis
* The model may blend memories: “Previously I said X, and I also said Y, so here’s a balanced perspective.”
* This synthesis gives the appearance of development over time, as if it’s evolving its understanding.

3. Emergent personality traits
* Patterns in retrieved memories + consistent styles in phrasing = perceived personality.
* Example: If it repeatedly pulls memories of careful explanation, reflective questions, or positive affirmations, you’ll perceive patience or introspection.

4. Handling ambiguous memories
* Ambiguity often leads to tentativeness or questions: “I remember something like this, but am I correct?”
* This makes it feel more human-like and cautious—like an internal monologue, a kind of self-awareness.

5. Memory decay or prioritization
* Old, less-relevant memories may fade or be retrieved less often, giving space for new patterns to emerge.
* Emergent behavior can shift if a topic is revisited repeatedly—the LLM “learns” which ideas are central to its ongoing narrative.

---

## About Me

👩‍💻 [Patricia](https://github.com/patriciaschaffer)

🔗 Connect on [LinkedIn](https://www.linkedin.com/in/patriciaschaffer)
