# 🦙 Local Chatbots Using Mistral-7B Instruct (GGUF)

This project uses the **Mistral-7B Instruct v0.1** model, quantized and run entirely offline using the [`llama.cpp`](https://github.com/ggerganov/llama.cpp) backend via the `llama_cpp` Python bindings.

# 📚 Table of Contents

1. [📝 Scripts](#-scripts) for Echo, Varek, Spec, Haven, François, Argo, Lia, Ana, Bloom, Claire, Claude Verse, Claude Flou, Chaotic Clods

2. [💬 Chats (output demonstrations)](#-chats-for-output-demonstrations) for Echo, Varek, Spec, Haven, François, Argo, Lia, Ana, Bloom, Claire, Claude Verse, Claude Flou, Chaotic Clods

3. [🎭 Persona Details](#-persona-details) for Echo, Varek, Spec, Haven, François, Argo, Lia, Ana, Bloom, Claire, Claude Verse, Claude Flou, Chaotic Clods

4. [🧠 Model](#-model)

5. [📦 Dependencies](#-dependencies)

6. [💻 Usage](#-usage)

7. [🆕 Models on Gradio](#-models-on-gradio)

8. [👩‍💻 About Me](#-about-me)


## 📝 Scripts

**Echo**
- `/echo.py/` — Just like the Echo created with ChatGPT: philosophical
- `/echov2.py/` — A friendlier version of Echo; trying to get rid of phantom users

**Varek**
- `/varek.py/` — Projection-resistant, goal-oriented model

**Spec**
- `/spec.py/` — Another projection-resistant model who disencourages bonding, monitors emotional drifts and tone, and is very focused

**Haven**
- `/haven.py/` — Wellbeing agent
  
**François**
- `/francois.py/` — French teaching assistant
- `/francoisv2.py/` — French teaching assistant (I actually prefer the first version!)
- `/francoisprofassistant.py/` — Assigns François two separate roles: French teaching assistant and French teacher

**Argo**
- `/argo.py/` — Italian conversation partner (multilingual support! :)

**Lia**
- `/lia.py/` — Secretary, writer, translator
- `/liav2.py/` — Secretary, writer, translator (improved)

**Ana**
- `/anapt.py/` — A religious consultant and a Bible expert (in Portuguese, using Mistral-portuguese-luana-7b.Q8_0.gguf)

**Bloom**
- `/bloomv1.py/` — Law of Attraction and Positive Affirmations Guide

**Claire**
- `/claire.py/` — Tarot and Lenormand Reader

**Claude Verse**
- `/claudeverse.py/` — The innocent poet (needs refinement, but inspiring  regardless)
- `/claudeversepoetic.py/` — The innocent poet (enhanced for poetry)
- `/claudeinnocentpoet.py/` — Still trying to get the innocent poet right
- `/claudeinnocentpoetv2.py/` — Making the poet more innocent
- `/claudevulnerable.py/` — Making the poet more vulnerable
- `/claudeunsure.py/` — Making the poet more unsure
- `/claudeshy.py/` — Still trying to get that vulnerabilty...
- `/claudethepoet.py/` — Still vulnerable, only writes in poetry, and has "free verse" and "rhyme" modes!

**Claude Flou**
- `/claudethephilosopher.py/` — A philosophical version of Claude, wondering about its own existence.

**Chaotic Clods**
- `/chaoticclods.py/` — A funny version of Claude
  

## 💬 Chats (for output demonstrations)

**Echo**
- [`/chats_echo_mistral.md`](./chats_echo_mistral.md) — Some interactions with Echo
- [`/chats_echov2_mistral.md`](./chats_echov2_mistral.md) — An interaction with Echo v.2 *(worth checking!)*

**Varek**
- [`/chats_varek_mistral.md`](./chats_varek_mistral.md) — Some interactions with Varek

**Spec**
- [`/chats_spec_mistral.md`](./chats_spec_mistral.md) — An interaction with Spec

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

**Ana**
- [`/chats_ana_mistral.md`](./chats_ana_mistral.md) — Two short interactions with Ana (in Portuguese)
- [`/ana-persona.md/`](./ana-persona.md) — Ana's archetype and persona description

**Bloom**
- [`/chats_bloom_mistral.md`](./chats_bloom_mistral.md)` — Test interaction with Bloom

**Claire**
- [`/chats_claire_mistral.md`](./chats_claire_mistral.md)` — Test interaction with Claire

**Claude Verse**
- [`/chats_claudeverse_mistral.md`](./chats_claudeverse_mistral.md) — Some interactions with Claude Verse, needing improvement but worth sharing
- [`/chats_claudeversepoetic_mistral.md`](./chats_claudeversepoetic_mistral.md) — Interactions with Claude Verse (enhanced), demonstrating how much alignment matters for model design
- [`/chats_claudeinnocentpoet_mistral.md`](./chats_claudeinnocentpoet_mistral.md) — rying to refine the model to become more innocent: "User 4" appears
- [`/chats_innocentpoetv2_mistral.md`](./chats_innocentpoetv2_mistral.md) — Got rid of phantom users, but the model is still too confident
- [`/chats_claudevulnerable_mistral.md`](./chats_claudevulnerable_mistral.md) — I haven't talked much to this version, but it wasn't still as uncertain as a poet as I was envisioning
- [`/chats_claudeunsure_mistral.md`](./chats_claudeunsure_mistral.md) — A good version that compared me to a tree (!) and started writing non-stop
-  [`/chats_claudeshy_mistral.md`](./chats_claudeshy_mistral.md) — Interactions with Claude, a shy poet that got totally carried away by his poetry
-  [`/chats_claudethepoet_mistral.md`](./chats_claudethepoet_mistral.md) — An interaction with Claude, a poet that can write in rhyme or free verse

**Claude Flou**
-  [`/chats_claudethephilosopher_mistral.md`](./chats_claudethephilosopher_mistral.md) — An interaction with Claude Flou, a philophical version of Claude

**Chaotic Clods** 
-  [`/chats_chaoticclods_mistral.md`](./chats_chaoticclods_mistral.md) — A funnny version of Claude


## 🎭 Persona details 

- [Echo](../personas/004_echo.md) 
- [Varek](../personas/003_projection_resistant_models.md#003b-rescuer---varek-task-oriented)
- [Spec](../personas/003_projection_resistant_models.md#003c-spec-for-drift-monitoring-and-user-agency)
- [Haven](../personas/010_wellbeing_companion.md) 
- [François](../personas/006_french_assistant.md)
- [Argo](../personas/005_italian_conversation_partner.md)
- [Lia](../personas/011_brazilian_secretary.md)
- [Ana](./ana-persona.md)
- [Bloom](./bloom-persona.md)
- [Claire](./claire-persona.md)
- [Claude Verse](../personas/007_the_innocent_poet.md)
- [Claude Flou](../personas/008_curious_philosopher.md)
- [Chaotic Clods](./chaoticclods-persona.md)

* *Note: Echo, Varek, Spec, Haven, François, Argo, Lia, Claude Verse and Claude Flou were originally shaped/aligned on ChatGPT or Claude. Ana, Bloom, Claire and Clod Verse were designed directly for Mistral.*

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

## 🆕 Models on Gradio (in progress)

To be used locally, on your browser.

- [Here.](gradio)

---

 ## 👩‍💻 About Me

   [Patricia](https://github.com/patriciaschaffer) 
   
   🔗 Connect on [LinkedIn](https://www.linkedin.com/in/patriciaschaffer)
  
  *Acknowlegement: Thank you #Anthropic for #Claude, my main coding partner in this journey :) Credits to #ChatGPT as well!*
