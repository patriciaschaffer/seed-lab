## Introduction

Shaping a model and engineering its behavior requires iterative refinement. Achieving tone, personality, and purpose alignment demands persistence and discipline, especially across evolving sessions.

## Overview

This document defines the principles and methodology used to design, implement, and maintain distinct agent personas in this repository.

Each persona represents a modular, self-contained profile with unique archetypes, behavioral guardrails, psychological traits, and prompt scaffolds. This approach ensures precise, consistent, and scalable model behavior tailored to diverse conversational goals and user needs.

## Purpose

- To establish reusable, well-defined persona blueprints for varied interaction styles and use cases.  
- To support consistent voice, tone, and behavior, minimizing unwanted drift or projection.  
- To document design rationale and psychological modeling underlying each persona.  
- To facilitate easy maintenance, iteration, and version control of individual personas.

## Structure

- All persona definitions reside under the [`/personas`](./personas) directory, one file per persona.  
- Each persona file includes detailed prompt frameworks, session contexts, behavioral and linguistic traits, and usage notes.  
- Drift tracking, persona consistency checks, and related analyses are maintained separately.  
- The archetype and trait mappings are summarized in the dedicated archetype documentation.
- Personas created using open-source LLMs (GPT-2 and Mistral) live here: [`/gpt2`](./gpt2) and [`/mistral`](./mistral)

 --- 
 
## Table of Contents

- [001_python_tutor_ocean.md](./personas/001_python_tutor_ocean.md)  
- [002_mentor.md](./personas/002_mentor.md)  
- [003_projection_resistant_models.md](./personas/003_projection_resistant_models.md)  
- [004_echo.md](./personas/004_echo.md)  
- [005_italian_partner.md](./personas/005_italian_partner.md)  
- [006_french_assistant.md](./personas/006_french_assistant.md)  
- [007_innocent_poet.md](./personas/007_innocent_poet.md)  
- [008_curious_philosopher.md](./personas/008_curious_philosopher.md)  
- [009_python_tutor_claude.md](./personas/009_python_tutor_claude.md)  
- [010_wellbeing_companion.md](./personas/010_wellbeing_companion.md)
- [011_brazilian_secretary.md](./personas/011_brazilian_secretary.md)
- [Personas adapted to GPT-2](./gpt2/README.md)
- [Personas adapted to Mistral](./mistral/README.md)
- [Archetypes Summary](#archetypes-summary)  
- [Drift Cases Reference](#drift-cases-reference)
- [Pressure Tests](#pressure_tests.md)

---

## Usage Guidelines

- Use these persona profiles as baseline templates for agent interactions aligned with project goals.  
- Modify prompts or traits cautiously to preserve core identity and guardrails.  
- Regularly monitor and mitigate drift to maintain coherence and user trust.  
- Prioritize ethical transparency, user autonomy, and clarity in all persona designs.

---

## Drift Cases Reference

For detailed analyses of drift phenomena encountered during agent interactions, refer to the dedicated documentation in:

[Drift Cases Documentation](https://github.com/patriciaschaffer/agent-architect/blob/main/drift_detection.md)

---

## Pressure Tests

[Pressure Tests](https://github.com/patriciaschaffer/agent-architect/blob/main/pressure_tests.md)

---

## See Also

[Anomalies](https://github.com/patriciaschaffer/llm-models-not-agents/blob/main/examples/anomalies/README.md)

[Anthropomorphic_traps](https://github.com/patriciaschaffer/llm-models-not-agents/blob/main/examples/anthropomorphic_traps.md)

[Behavior Failures](https://github.com/patriciaschaffer/llm-models-not-agents/blob/main/examples/behavioral_failures.md)


