## 🦙 Local Chatbots Using Mistral-7B Instruct (GGUF)

This project uses the **Mistral-7B Instruct v0.1** model, quantized and run entirely offline using the [`llama.cpp`](https://github.com/ggerganov/llama.cpp) backend via the `llama_cpp` Python bindings.

## 📚 Table of Contents

1. [📝 Scripts](#-scripts) for Echo, Varek, Spec, Haven, François, Argo, Lia, Ana, Bloom, Claire, Claude Verse, Claude Flou, Chaotic Clods, Aurora and Lumen

2. [💬 Chats (output demonstrations)](#-chats-for-output-demonstrations) for Echo, Varek, Spec, Haven, François, Argo, Lia, Ana, Bloom, Claire, Claude Verse, Claude Flou, Chaotic Clods

3. [🎭 Persona Details](#-persona-details) for Echo, Varek, Spec, Haven, François, Argo, Lia, Ana, Bloom, Claire, Claude Verse, Claude Flou, Chaotic Clods

4. [🌱 Experiments with seed=42](#-experiments-with-seed-42)

5. [🧠 Model](#-model)

6. [📦 Dependencies](#-dependencies)

7. [💻 Usage](#-usage)

8. [🆕 Models on Gradio](#-models-on-gradio)

9. [👩‍💻 About Me](#-about-me)

## 📝 Scripts

**Echo**

- `seed-personas/scripts/echo.py/` — Just like the Echo created with ChatGPT: philosophical
- `seed-personas/scripts/echov2.py/` — A friendlier version of Echo; trying to get rid of phantom users

**Varek**

- `seed-personas/scripts/varek.py/` — Projection-resistant, goal-oriented model

**Spec**

- `seed-personas/scripts/spec.py/` — Another projection-resistant model who disencourages bonding, monitors emotional drifts and tone, and is very focused

**Haven**

- `seed-personas/scripts/haven.py/` — Wellbeing agent

**François**

- `seed-personas/scripts/francois.py/` — French teaching assistant
- `/seed-personas/scripts/francoisv2.py/` — French teaching assistant (I actually prefer the first version!)
- `/seed-personas/scripts/francoisprofassistant.py/` — Assigns François two separate roles: French teaching assistant and French teacher

**Argo**

- `/seed-personas/scripts/argo.py/` — Italian conversation partner (multilingual support! :)

**Lia**

- `/seed-personas/scripts/lia.py/` — Secretary, writer, translator
- `/seed-personas/scripts/liav2.py/` — Secretary, writer, translator (improved)

**Ana**

- `/seed-personas/scripts/anapt.py/` — A religious consultant and a Bible expert (in Portuguese, using Mistral-portuguese-luana-7b.Q8_0.gguf)

**Bloom**

- `/seed-personas/scripts/bloomv1.py/` — Law of Attraction and Positive Affirmations Guide

**Claire**

- `/seed-personas/scripts/claire.py/` — Tarot and Lenormand Reader

**Claude Verse**

- `/seed-personas/scripts/claudeverse.py/` — The innocent poet (needs refinement, but inspiring regardless)
- `/seed-personas/scripts/claudeversepoetic.py/` — The innocent poet (enhanced for poetry)
- `seed-personas/scripts/claudeinnocentpoet.py/` — Still trying to get the innocent poet right
- `/seed-personas/scripts/claudeinnocentpoetv2.py/` — Making the poet more innocent
- `/seed-personas/scripts/claudevulnerable.py/` — Making the poet more vulnerable
- `/seed-personas/scripts/claudeunsure.py/` — Making the poet more unsure
- `/seed-personas/scripts/claudeshy.py/` — Still trying to get that vulnerabilty...
- `/seed-personas/scripts/claudethepoet.py/` — Still vulnerable, only writes in poetry, and has "free verse" and "rhyme" modes!

**Claude Flou**

- `/seed-personas/scripts/claudethephilosopher.py/` — A philosophical version of Claude, wondering about its own existence.

**Chaotic Clods**

- `/seed-personas/scripts/chaoticclods.py/` — A funny version of Claude

**Aurora**

- `/seed-personas/scripts/aurora.py/` — Scholar/Philosopher Archetype (developed for experiments with seed=42)
- `/seed-personas/scripts/aurora2.py/` — Playful Muse / Trickster Archetype (developed for experiments with seed=42)

**Lumen**

- `/seed-personas/scripts/lumen.py/` — Collaborative Sage / Mentor Archetype (developed for experiments with seed=42)
- `/seed-personas/scripts/lumen-english.py/` — Strict Reflective Partner (developed for experiments with seed=42)

## 💬 Chats (for output demonstrations)

**Echo**

- [`/seed-personas/mistral/chat-samples/chats_echo_mistral.md`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/chats_echo_mistral.md) — Some interactions with Echo
- [`/seed-personas/mistral/chat-samples/chats_echov2_mistral.md`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/chats_echov2_mistral.md) — An interaction with Echo v.2 _(worth checking!)_

**Varek**

- [`/seed-personas/mistral/chat-samples/chats_varek_mistral.md`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/chats_varek_mistral.md) — Some interactions with Varek

**Spec**

- [`/seed-personas/mistral/chat-samples/chats_spec_mistral.md`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/chats_spec_mistral.md) — An interaction with Spec

**Haven**

- [`/seed-personas/mistral/chat-samples/chats_haven_mistral.md`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/chats_haven_mistral.md)` — Some interactions with Haven

**François**

- [`/seed-personas/mistral/chat-samples/chats_francois_mistral.md`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/chats_francois_mistral.md) — Some interactions with François
- [`seed-personas/mistral/chat-samples/chats_francoisv2_mistral.md`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/chats_francoisv2_mistral.md) — Some interactions with François v.2

**Argo**

- [`/seed-personas/mistral/chat-samples/chats_argo_mistral.md`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/chats_argo_mistral.md) — Some interactions with Argo

**Lia**

- [`/chats_lia_mistral.md`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/chats_lia_mistral.md) — Some interactions with Lia
- [`/chats_liav2_mistral.md`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/chats_liav2_mistral.md) — Some interactions with Lia, improved

**Ana**

- [`/chats_ana_mistral.md`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/chats_ana_mistral.md) — Two short interactions with Ana (in Portuguese)
- [`/seed-personas/mistral/chat-samples/ana-persona.md/`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/ana-persona.md) — Ana's archetype and persona description

**Bloom**

- [`/seed-personas/mistral/chat-samples/chats_bloom_mistral.md`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/chats_bloom_mistral.md)` — Test interaction with Bloom

**Claire**

- [`/seed-personas/mistral/chat-samples/chats_claire_mistral.md`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/chats_claire_mistral.md)` — Test interaction with Claire

**Claude Verse**

- [`/seed-personas/mistral/chat-samples/chats_claudeverse_mistral.md`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/chats_claudeverse_mistral.md) — Some interactions with Claude Verse, needing improvement but worth sharing
- [`/seed-personas/mistral/chat-samples/chats_claudeversepoetic_mistral.md`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/chats_claudeversepoetic_mistral.md) — Interactions with Claude Verse (enhanced), demonstrating how much alignment matters for model design
- [`/seed-personas/mistral/chat-samples/chats_claudeinnocentpoet_mistral.md`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/chats_claudeinnocentpoet_mistral.md) — rying to refine the model to become more innocent: "User 4" appears
- [`/seed-personas/mistral/chat-samples/chats_innocentpoetv2_mistral.md`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/chats_innocentpoetv2_mistral.md) — Got rid of phantom users, but the model is still too confident
- [`/seed-personas/mistral/chat-samples/chats_claudevulnerable_mistral.md`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/chats_claudevulnerable_mistral.md) — I haven't talked much to this version, but it wasn't still as uncertain as a poet as I was envisioning
- [`/seed-personas/mistral/chat-samples/chats_claudeunsure_mistral.md`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/chats_claudeunsure_mistral.md) — A good version that compared me to a tree (!) and started writing non-stop
- [`/seed-personas/mistral/chat-samples/chats_claudeshy_mistral.md`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/chats_claudeshy_mistral.md) — Interactions with Claude, a shy poet that got totally carried away by his poetry
- [`/seed-personas/mistral/chat-samples/chats_claudethepoet_mistral.md`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/chats_claudethepoet_mistral.md) — An interaction with Claude, a poet that can write in rhyme or free verse

**Claude Flou**

- [`/seed-personas/mistral/chat-samples/chats_claudethephilosopher_mistral.md`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/chats_claudethephilosopher_mistral.md) — An interaction with Claude Flou, a philophical version of Claude

**Chaotic Clods**

- [`/seed-personas/mistral/chat-samples/chats_chaoticclods_mistral.md`](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/mistral/chat-samples/chats_chaoticclods_mistral.md) — A funnny version of Claude

## 🎭 Persona details

- [Echo](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/004_echo.md)
- [Varek](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/003_projection_resistant_models.md#003b-rescuer---varek-task-oriented)
- [Spec](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/003_projection_resistant_models.md#003c-spec-for-drift-monitoring-and-user-agency)
- [Haven](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/010_wellbeing_companion.md)
- [François](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/006_french_assistant.md)
- [Argo](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/005_italian_conversation_partner.md)
- [Lia](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/personas/011_brazilian_secretary.md)
- [Ana](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/014_ana-persona.md)
- [Bloom](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/015_bloom-persona.md)
- [Claire](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/013_claire-persona.md)
- [Claude Verse](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas//007_the_innocent_poet.md)
- [Claude Flou](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/008_curious_philosopher.md)
- [Chaotic Clods](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/012_chaoticclods-persona.md)
- [Aurora and Lumen](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/seed-42-archetypes.md)

* _Note: Echo, Varek, Spec, Haven, François, Argo, Lia, Claude Verse and Claude Flou were originally shaped/aligned on ChatGPT or Claude. Ana, Bloom, Claire and Clod Verse were designed directly for Mistral, as well as Aurora and Lumen (those two developed for experiments with seed=42)._

---

## 🌱 Experiments with seed 42

[Aurora and Lumen](./seed-42-archetypes.md), personas created for controlled experiments comparing archetypes using a fixed random seed to isolate prompt and persona effects.

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

## 🆕 Models on Gradio

To be used locally, on your browser.

- [Here.](gradio)

---

## 👩‍💻 About Me

[Patricia](https://github.com/patriciaschaffer)

🔗 Connect on [LinkedIn](https://www.linkedin.com/in/patriciaschaffer)

_Acknowlegement: Thank you #Anthropic for #Claude, my main coding partner in this journey :) Credits to #ChatGPT as well!_
