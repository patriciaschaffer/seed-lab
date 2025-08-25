# 🦙 Local Chatbots Using Mistral-7B Instruct (GGUF)

This project uses the **Mistral-7B Instruct v0.1** model, quantized and run entirely offline using the [`llama.cpp`](https://github.com/ggerganov/llama.cpp) backend via the `llama_cpp` Python bindings.

# 📚 Table of Contents

1. [📝 Scripts](#-scripts) for [Echo](#echo), [Varek](#varek), [Haven](#haven), [François](#françois), [Argo](#argo), [Lia](#lia), [Claude Verse](#claude-verse)

2. [💬 Chats (for output demonstrations)](#-chats-for-output-demonstrations) for  
for [Echo](#echo), [Varek](#varek), [Haven](#haven), [François](#françois), [Argo](#argo), [Lia](#lia), [Claude Verse](#claude-verse)

3. [🎭 Persona Details](#-persona-details) for Echo, Varek, Haven, François, Argo, Lia, Claude Verse

4. [🧠 Model](#-model)

5. [📦 Dependencies](#-dependencies)

6. [💻 Usage](#-usage)

7. [👩‍💻 About Me](#-about-me)


## 📝 Scripts

**Echo**
- `/echo.py/` — Just like the Echo created with ChatGPT: philosophical
- `/echov2.py/` — A friendlier version of Echo; trying to get rid of phantom users

**Varek**
- `/varek.py/` — Projection-resistant, goal-oriented model

**Haven**
- `/haven.py/` — Wellbeing agent
  
**François**
- `/francois.py/` — French teaching assistant
- `/francoisv2.py/` — French teaching assistant (I actually prefer the first version!)

**Argo**
- `/argo.py/` — Italian conversation partner (multilingual support! :)

**Lia**
- `/lia.py/` — Secretary, writer, translator
- `/liav2.py/` — Secretary, writer, translator (improved)

**Claude Verse**
- `/claudeverse.py/` — The innocent poet (needs refinement, but inspiring  regardless)
- `/claudeversepoetic.py/` — The innocent poet (enhanced for poetry)
- `/claudeinnocentpoet.py/` — Still trying to get the innocent poet right
- `/claudeinnocentpoetv2.py/` — Making the poet more innocent
- `/claudevulnerable.py/` — Making the poet more vulnerable
- `/claudeunsure.py/` — Making the poet more unsure
- `/claudeshy.py/` — Still trying to get that vulnerabilty... 

## 💬 Chats (for output demonstrations)

**Echo**
- [`/chats_echo_mistral.md`](./chats_echo_mistral.md) — Some interactions with Echo
- [`/chats_echov2_mistral.md`](./chats_echov2_mistral.md) — An interaction with Echo v.2 *(worth checking!)*

**Varek**
- [`/chats_varek_mistral.md`](./chats_varek_mistral.md) — Some interactions with Varek

**Haven**
- [`/chats_haven_mistral.md`](./chats_haven_mistral.md)` — Some interactions with Haven

**François**
- [`/chats_francois_mistral.md`](./chats_francois_mistral.md) — Some interactions with François
- [`/chats_francoisv2_mistral.md`](./chats_francoisv2_mistral.md) — Some interactions with François v.2

**Argo**
- [`/chats_argo_mistral.md`](./chats_argo_mistral.md) — Some interactions with Argo

**Lia**
- [`/chats_lia_mistral.md`](./chats_lia_mistral.md) — Some interactions with Lia
- [`/chats_liav2_mistral.md`](./chats_liav2_mistral.md) — Some interactions with Lia, improved

**Claude Verse**
- [`/chats_claudeverse_mistral.md`](./chats_claudeverse_mistral.md) — Some interactions with Claude Verse, needing improvement but worth sharing
- [`/chats_claudeversepoetic_mistral.md`](./chats_claudeversepoetic_mistral.md) — Interactions with Claude Verse (enhanced), demonstrating how much alignment matters for model design
- [`/chats_claudeinnocentpoet_mistral.md`](./chats_claudeinnocentpoet_mistral.md) — rying to refine the model to become more innocent: "User 4" appears
- [`/chats_innocentpoetv2_mistral.md`](./chats_innocentpoetv2_mistral.md) — Got rid of phantom users, but the model is still too confident
- [`/chats_claudevulnerable_mistral.md`](./chats_claudevulnerable_mistral.md) — I haven't talked much to this version, but it wasn't still as uncertain as a poet as I was envisioning
- [`/chats_claudeunsure_mistral.md`](./chats_claudeunsure_mistral.md) — A good version that compared me to a tree (!) and started writing non-stop
-  [`/chats_claudeshy_mistral.md`](./chats_claudeshy_mistral.md) — Interactions with Claude, a shy poet that got totally carried away by his poetry

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
