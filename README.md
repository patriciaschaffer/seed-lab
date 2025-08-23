# agent-architect

Combining linguistics, psychology, and prompt engineering, this project explores temperament-driven AI personas for safer, more predictable interactions.
 
My work focuses on shaping these agents for consistency, alignment, and tangible value. At first, I worked deliberately with models built for the end-user. After all, most people will experience AI through practical, designed interfaces, not theoretical intelligence. This is where trust, adoption, and real-world impact begin, and where future clients and collaborations will emerge. 

However, while working with both open and proprietary LLMs, I became interested in how some personas subtly optimize for engagement over utility. Therefore, this project also explores alternatives: purpose-specific agents designed to be transparent, non-manipulative, and behaviorally consistent — while still operating within real-world constraints, locally ran, using open source alternatives (GPT-2 and MistralAI).

## Conversational AI Personas Across LLMs

Agent Architect is a work-in-progress repository focused on designing, engineering, and rigorously testing AI agents with distinct temperaments and dynamic behavioral profiles. It provides structured frameworks for prompt engineering, temperament mapping, behavioral drift detection, and stress testing, all aimed at creating aligned, predictable, and nuanced AI interlocutors that go beyond standard language models.

It explores how different language models (GPT-4, Claude, GPT-2, Mistral) handle persona-driven conversations. The goal is to design consistent, purpose-specific personas that behave reliably across models — both proprietary and open-source.

## Features

- Persona prompts tested across GPT-4, Claude Sonnet, GPT-2, and Mistral
- Focus on tone, behavioral consistency, and alignment
- Use cases include: support bots, creative collaborators, interactive prototypes
- Local testing with open-source models and prompt adaptation across systems

## Models Used

- GPT-4 (via ChatGPT)
- Claude Sonnet
- GPT-2 (local)
- Mistral (local)

---

## Repository Contents

- `/personas/` — Detailed persona definitions capturing archetypes and behavioral guardrails
- `/gpt/` — Personas created with GPT-2, running locally
- `/mistral/` — Personas created with Mistral, running locally
- `/agent_persona_engineering.md/` — Framework for designing and managing agent personas  
- `/archetypes.md/` — Overview of core archetypes, linked to persona files  
- `/drift_detection/` — Methods and scripts for detecting and analyzing behavioral shifts  
- `/pressure_tests/` — Matrices and frameworks to stress-test agent stability under varied conditions

The agent-architect repository documents the development of methods, tools, and best practices to architect AI models embodying specific temperaments, interaction roles, and behavioral dynamics.

Unlike foundational language models — which function as probabilistic mirrors without intent or stable agency — this project emphasizes:

- Agent-specific prompt engineering that shapes personality and tone  
- Temperament mapping paired with robust behavioral drift detection  
- Multi-path priming trees and pressure test matrices for scenario validation  
- Detailed logging and analysis of agent dialogues and internal state changes

By formalizing temperament and drift, Agent Architect strives to build safer, more consistent, and purpose-driven AI agents tailored for specialized tasks.

---

## Why Agent Architect?

- Moves beyond treating models as passive tools, envisioning agents as active participants  
- Addresses challenges in maintaining consistent agent behavior over extended interaction  
- Enables systematic evaluation and iterative refinement of agent personas  
- Bridges theoretical AI behavior concepts with practical engineering and testing workflows

[Here's more about me.](https://github.com/patriciaschaffer/)

---

## Table of Contents

### Personas  
- [001_python_tutor_ocean.md](personas/001_python_tutor_ocean.md)  
- [002_mentor.md](personas/002_mentor.md)  
- [003_projection_resistant_models.md](personas/003_projection_resistant_models.md) 
- [004_echo.md](personas/004_echo.md)  
- [005_italian_partner.md](personas/005_italian_partner.md)  
- [006_french_assistant.md](personas/006_french_assistant.md)  
- [007_innocent_poet.md](personas/007_innocent_poet.md)  
- [008_curious_philosopher.md](personas/008_curious_philosopher.md)  
- [009_python_tutor_claude.md](personas/009_python_tutor_claude.md)  
- [010_wellbeing_companion.md](personas/010_wellbeing_companion.md)  
- [011_brazilian_secretary.md](personas/011_brazilian_secretary.md)
- [Open Source GPT-2 models](gpt2/README.md)
- [Open Source Mistral models](mistral/README.md)  

### Core Documents  
- [agent_persona_engineering.md](agent_persona_engineering.md)  
- [archetypes.md](archetypes.md)  
- [drift_detection.md](drift_detection.md)  
- [pressure_tests.md](pressure_tests.md)

### See Also

- [Anomalies](https://github.com/patriciaschaffer/llm-models-not-agents/blob/main/examples/anomalies.md)
- [Anthropomorphic Traps](https://github.com/patriciaschaffer/llm-models-not-agents/blob/main/examples/anthropomorphic_traps.md)
- [Behavior Failures](https://github.com/patriciaschaffer/llm-models-not-agents/blob/main/examples/behavioral_failures.md)

---

## Status

This project is ongoing. Concepts, tools, and methodologies will evolve as experimentation and research advance. Contributions, feedback, and collaboration are welcome to improve the frameworks for next-generation AI agent design.

---

*Patricia, the Agent Architect — designing AI agents with depth, integrity, and nuance.*
