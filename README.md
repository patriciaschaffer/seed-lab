# 👩‍🎨 agent-architect 👷‍♀️

Combining linguistics, psychology, and prompt engineering, this project explores temperament-driven AI personas for safer, more predictable interactions.
 
My work focuses on shaping these models for consistency, alignment, and tangible value. At first, I worked deliberately with models built for the end-user. After all, most people will experience AI through practical, designed interfaces, not theoretical intelligence. This is where trust, adoption, and real-world impact begin, and where future clients and collaborations will emerge. 

However, while working with both open and proprietary LLMs, I became interested in how some personas subtly optimize for engagement over utility. Therefore, this project also explores alternatives: purpose-specific agents designed to be transparent, non-manipulative, and behaviorally consistent — while still operating within real-world constraints, locally run, using open source alternatives (GPT-2 and MistralAI).

For experimentation, I've also created personas to purposefully violate Grice's conversational maxims.

Right now, I'm testing a local setup with MistralAI to build customized language models that use RAG to simulate memory. I've incorporated FAISS for fast similarity search and used sentence or document embeddings to enable more accurate retrieval of relevant context. 

---

## Table of Contents

### This Document

- [Conversational AI Personas Across LLMs](#conversational-ai-personas-across-llms)
- [Features](#features)
- [Models Used](#models-used)
- [Why Agent Architect?](#why-agent-architect)
- [Repository Contents](#repository-contents)
- [Status](#status)

### Personas  

- 🗺️ [Personas ecosystem overview](llm-society.md)
- [001_python_tutor_ocean.md](personas/001_python_tutor_ocean.md)  
- [002_mentor.md](personas/002_mentor.md)  
- [003_projection_resistant_models.md](personas/003_projection_resistant_models.md) 
- [004_echo.md](personas/004_echo.md)  
- [005_italian_partner.md](personas/005_italian_conversation_partner.md)  
- [006_french_assistant.md](personas/006_french_teaching_assistant.md)  
- [007_innocent_poet.md](personas/007_innocent_poet.md)  
- [008_curious_philosopher.md](personas/008_curious_philosopher.md)  
- [009_python_tutor_claude.md](personas/009_python_tutor_claude.md)  
- [010_wellbeing_companion.md](personas/010_wellbeing_companion.md)  
- [011_brazilian_secretary.md](personas/011_brazilian_secretary.md)
- [Personas that violate Grice's Maxims](./personas/grice-s-maxims/README.md)
- [GPT-2 models](gpt2/README.md)
- [Mistral models](mistral/README.md)

### Core Documents  

- [agent-persona-engineering.md](agent-persona-engineering.md)  
- [archetypes.md](archetypes.md)  
- [anomalies](anomalies/README.md)
- [pressure-tests.md](pressure-tests.md)
- [prompt-interaction-strategies.md](prompt-interaction-strategies.md)
- [glossary.md](glossary.md)
- [related-reading.md](related-reading.md)

---

## Conversational AI Personas Across LLMs

Agent Architect is a work-in-progress repository focused on designing, engineering, and rigorously testing AI agents with distinct temperaments and dynamic behavioral profiles. It provides structured frameworks for prompt engineering, temperament mapping, behavioral drift detection, and stress testing, all aimed at creating aligned, predictable, and nuanced AI interlocutors that go beyond standard language models.

It explores how different language models (GPT-4, Claude, GPT-2, Mistral) handle persona-driven conversations. The goal is to design consistent, purpose-specific personas that behave reliably across models — both proprietary and open-source.

---

## Features

- Persona prompts tested across GPT-4, Claude Sonnet, GPT-2, and Mistral
- Focus on tone, behavioral consistency, and alignment
- Use cases include: support bots, creative collaborators, interactive prototypes
- Local testing with open-source models and prompt adaptation across systems

---

## Models Used

- GPT-4 (via ChatGPT)
- Claude Sonnet
- GPT-2 (local)
- Mistral (local)

---

## Why Agent Architect?

- Moves beyond treating models as passive tools, envisioning models as active participants  
- Addresses challenges in maintaining consistent model behavior over extended interaction  
- Enables systematic evaluation and iterative refinement of personas  
- Bridges theoretical AI behavior concepts with practical engineering and testing workflows

👷‍♀️👩‍🎨 [Here's more about me.](https://github.com/patriciaschaffer/)

---

## Repository Contents

The agent-architect repository documents the development of methods, tools, and best practices to architect AI models embodying specific temperaments, interaction roles, and behavioral dynamics.

Unlike foundational language models — which function as probabilistic mirrors without intent or stable agency — this project emphasizes:

- Model-specific prompt engineering that shapes personality and tone  
- Temperament mapping paired with robust behavioral drift detection  
- Multi-path priming trees and pressure test matrices for scenario validation  
- Detailed logging and analysis of agent dialogues and internal state changes

By formalizing temperament and drift, Agent Architect strives to build safer, more consistent, and purpose-driven AI assistants tailored for specialized tasks.

- `/personas` — Detailed persona definitions capturing archetypes and behavioral guardrails
- `/gpt` — Personas created with GPT-2, running locally
- `/mistral` — Personas created with Mistral, running locally
- `/personas/grice-s-maxims/` — Personas that systematically violate Grice's conversational maxims (for study and research)
- `/memory-rag` — Using RAG to simulate persistent memory in local models
- `/conversation-artifacts` — Unexpected behaviors and drifts; documents for interpretability and XAI
- `/agent-persona-engineering.md` — Framework for designing and managing personas
- `/archetypes.md` — Overview of core archetypes, linked to persona files  
- `/pressure-tests.md` — Matrices and frameworks to stress-test model stability under varied conditions
- `/glossary.md` — Terminology, definitions
- `/related-reading.md` — Recommended readings on psychology, philosophy of mind, philosophy of language, linguistics etc.
- `/insights` — Some of my writings and insights on LLMs 
- `/research` — Bias in AI Responses: A Prompt-Based Analysis of Tone, Ideology, and Temperature in Large Language Models
- `/python-projects` — Visualizing a Small Language Model

---

## Status

This project is ongoing. Concepts, tools, and methodologies will evolve as experimentation and research advance. Contributions, feedback, and collaboration are welcome to improve the frameworks for next-generation AI model design. 

---

*Patricia, the Agent Architect — designing AI agents with depth, integrity, and nuance.*
