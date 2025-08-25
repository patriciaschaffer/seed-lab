# 🦙 Local Chatbots Using Mistral-7B Instruct (GGUF)

This project uses the **Mistral-7B Instruct v0.1** model, quantized and run entirely offline using the [`llama.cpp`](https://github.com/ggerganov/llama.cpp) backend via the `llama_cpp` Python bindings.

## 📝 Scripts

- `/echo.py/` — Just like the Echo created with ChatGPT: philosophical
- `/echov2.py/` — A friendlier version of Echo; trying to get rid of phantom users
- `/varek.py/` — Projection-resistant, goal-oriented model
- `/haven.py/` — Wellbeing agent
- `/francois.py/` — French teaching assistant
- `/francoisv2.py/` — French teaching assistant (I actually prefer the first version!)
- `/argo.py/` — Italian conversation partner (multilingual support! :)
- `/lia.py/` — Secretary, writer, translator
- `/liav2.py/` — Secretary, writer, translator (improved)
- `/claudeverse.py/` — The innocent poet (needs refinement, but inspiring  regardless)

## 💬 Chats (for output demonstrations)

- [`/chats_echo_mistral.md`](./chats_echo_mistral.md) — Some interactions with Echo
- [`/chats_echov2_mistral.md`](./chats_echov2_mistral.md) — An interaction with Echo v.2 *(worth checking!)*
- [`/chats_varek_mistral.md`](./chats_varek_mistral.md) — Some interactions with Varek
- [`/chats_haven_mistral.md`](./chats_haven_mistral.md)` — Some interactions with Haven
- [`/chats_francois_mistral.md`](./chats_francois_mistral.md) — Some interactions with François
- [`/chats_francoisv2_mistral.md`](./chats_francoisv2_mistral.md) — Some interactions with François v.2
- [`/chats_argo_mistral.md`](./chats_argo_mistral.md) — Some interactions with Argo
- [`/chats_lia_mistral.md`](./chats_lia_mistral.md) — Some interactions with Lia
- [`/chats_liav2_mistral.md`](./chats_liav2_mistral.md) — Some interactions with Lia, improved
- [`/chats_claudeverse_mistral.md`](./chats_claudeverse_mistral.md) — Some interactions with Claude Verse, needing improvement but worth sharing

## 🎭 Persona details (originally shaped/aligned on ChatGPT or Claude)

- [Echo](../personas/004_echo.md) 
- [Varek](../personas/003_projection_resistant_models.md) 
- [Haven](../personas/010_wellbeing_companion.md) 
- [François](../personas/006_french_assistant.md)
- [Argo](../personas/005_italian_conversation_partner.md)
- [Lia](../personas/011_brazilian_secretary.md)
- [Claude Verse](../personas/007_the_innocent_poet.md)

--- 

## 🧠 Model

- **Model**: `mistral-7b-instruct-v0.1.Q4_K_M.gguf`
- **Source**: [Hugging Face - TheBloke](https://huggingface.co/TheBloke)
- **Architecture**: Mistral 7B
- **Quantization**: Q4_K_M (4-bit)
- **Backend**: `llama.cpp`

## 📦 Dependencies

- Python 3.10+
- `llama_cpp`
- `gguf` model file in your local path

## 💻 Usage

```python
from llama_cpp import Llama

llm = Llama(model_path="mistral-7b-instruct-v0.1.Q4_K_M.gguf")

response = llm(
    "Q: What is the capital of France?\nA:",
    max_tokens=64,
    stop=["Q:", "\n"],
)
print(response["choices"][0]["text"])
```
---

 ## 👩‍💻 About Me

   [Patricia](https://github.com/patriciaschaffer) 
   
   🔗 Connect on [LinkedIn](https://www.linkedin.com/in/patriciaschaffer)
  
  *Acknowlegement: Thank you #Anthropic for #Claude, my coding partner in this journey :)*
  
 
  
