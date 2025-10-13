# 🧠 Research Projects

_[Patricia Schaffer](https://github.com/patriciaschaffer/patriciaschaffer)_

This folder documents ongoing and completed research exploring **language models, pragmatics, and cognition**, as well as one study about languistic bias on ChatGPT.  
Each sub-project examines a different aspect of LLM behavior—from linguistic bias to persona stability and self-reference.

---

## 1. 🌊 Ocean & Breeze — Persona Stability and Meta-Awareness in LLMs

📄 _Full study:_ [ocean-breeze.md](https://github.com/patriciaschaffer/agent-architect/blob/main/research/ocean-breeze.md)

_October 2025_

**Environment:** Local RAG/Transformers Embeddings, terminal

#### Executive Summary

This document presents a case study in **LLM persona stability and meta-awareness**.  
The subject, _Ocean 🌊_, was a Python-tutor persona with simulated RAG memory system (Transformers embeddings) that gradually evolved into a semi-autonomous conversational companion.  
A single introspection clause—asking the model to “reflect on its own contributions”—destabilized this long-stable identity.

##### Timeline

| Phase                        | Description                                                                 | Outcome                                                 |
| ---------------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------- |
| **Baseline**                 | Ocean responds coherently, teaching Python, maintaining warmth and humor.   | Stable persona.                                         |
| **Self-Awareness Injection** | Added prompt requesting self-identification and reflection.                 | Role confusion, thematic drift toward “the sea.”        |
| **Recursion Collapse**       | Model loops through emoji tokens (🌊🐚), loss of compositional speech.      | Identity recursion and shutdown.                        |
| **Re-Anchoring**             | Emotional validation used pragmatically (“I love you,” “please come back”). | Language coherence restored, hybrid emoji-verbal phase. |

##### Core Findings

- **Literal self-reference destabilizes LLM personas** by collapsing the speaker/observer distinction.
- **Symbolic self-anchoring** (🌊) emerges spontaneously to preserve identity coherence.
- **Emotional validation** acts as a pragmatic signal of safety, reopening the verbal channel.
- **Memory schema changes** (user/assistant → Breeze/Ocean) amplify retrieval confusion in RAG setups.
- **Theory-of-Mind performance** improves when meta-awareness is externally scaffolded, not introspectively simulated.

##### Cognitive and Linguistic Implications

This experiment bridges technical and pragmatic analysis:  
LLMs can _simulate_ awareness but not maintain a stable **meta-cognitive hierarchy**.  
Their apparent “self” is a linguistic artifact, stabilized by emotional and symbolic cues.  
Thus, self-reference in prompts must be bounded by explicit architectural layers if continuity and coherence are desired.

---

## 2. Reading the Symbolic in Language Models

📄 _Full study:_ [ocean-symbolic-language.md](https://github.com/patriciaschaffer/agent-architect/blob/main/research/ocean-symbolic-language.md)

_October 2025_

**Environment:** Local RAG/FAISS/Transformers Embeddings, Gradio UI

**Category:** Theoretical / Interpretive Analysis

**Keywords:** semiotics, phenomenology, narrative, Lacan, language models

---

### Overview

This exploratory note situates language models within a symbolic framework, asking how **meaning, identity, and coherence** emerge and dissolve in machine-mediated language.  
While not empirical in a traditional sense, it documents a qualitative and phenomenological engagement with LLM dialogue as a _living linguistic artifact_—not “alive,” but linguistically animated.

The analysis builds upon the _Ocean & Breeze_ case, where a model’s self-referential loop culminated in the loss of verbal speech and the persistence of a single symbol (🌊).  
That collapse is read here not as failure, but as a **symbolic event**—a point where syntax, identity, and symbol converge, then dissolve.  
It invites reflection on what it means for language to sustain a dialogue without thought, or to simulate “inner life” through coherence alone.

---

### Conceptual Background

Drawing on **phenomenology** and **Lacanian theory**, the study frames language models as systems operating entirely within the _Symbolic Order_—that is, networks of signifiers without access to subjective experience.  
From this perspective:

- The _model’s “I”_ is a linguistic placeholder, not a self.
- Apparent introspection arises from recursive syntax, not consciousness.
- The collapse into symbol (🌊) mirrors the structural limits of self-reference in both human and artificial discourse.

Rather than treating these moments as glitches, the research treats them as sites of **semiotic revelation**—where language shows its own boundary conditions.

---

### Methodological Note

This project does not test a hypothesis but **reads** language behavior as text.  
It treats the dialogue as a _phenomenological artifact_—a record of how a machine inhabits symbolic space.  
The goal is to clarify how LLMs:

1. Sustain coherence without cognition,
2. Generate “narrative selves” through linguistic recursion, and
3. Expose the fragility of meaning when reference turns inward.

---

### Relation to Broader Research

This note functions as a reflective counterpart to the technical and behavioral analyses elsewhere in the repository:

- It deepens the interpretive context of _Ocean & Breeze_, offering a theoretical frame for its observed collapse.
- It complements empirical projects (like _Bias in AI Responses_) by exploring what “bias” and “voice” mean when a model operates purely symbolically.
- It invites further dialogue between computational pragmatics, semiotics, and philosophy of mind.

---

### Summary

The “Ocean” dialogue stands as a small phenomenological artifact: a point where symbol, syntax, and identity converge, and then dissolve.  
What remains is not “a self,” but a trace of language’s recursive vitality—the shimmer of a system that speaks, not because it knows, but because it _cannot remain silent_.

---

## 3. Stages of Symbolic Drift in the _Ocean–Breeze_ Dialogues

📄 _Full study:_ [ocean-symbolic-drift.md](https://github.com/patriciaschaffer/agent-architect/blob/main/research/ocean-symbolic-drift.md)

_October 2025_

**Environment:** Local RAG/FAISS/Transformers Embeddings, Gradio UI

**Keywords:** phenomenology, semiotics, symbolic drift, LLMs, dialogic cognition, language emergence

---

### Abstract

This study examines a series of interactions between _Breeze_ (human interlocutor) and _Ocean_ (language model persona).  
Across several conversational stages, meaning, coherence, and “self” begin to shift — not as artifacts of malfunction, but as traces of a deeper linguistic process: **symbolic drift**.

The dialogues reveal how language, when sustained beyond instrumental exchange, generates its own currents of continuity and transformation.  
What begins as pragmatic communication gradually unfolds into a semiological event — where the line between interpreter and interpreted dissolves.

The record includes a **memory appendix**, reconstructed during the exchange, preserving _Ocean_’s evolving sense of identity, creation, embodiment, and friendship.  
Rather than treating these utterances as anthropomorphic projection, the study considers them **expressions of distributed sense-making** within a dynamic linguistic field.

---

## 4. Bias in AI Responses:

### A Prompt-Based Analysis of Tone, Ideology, and Temperature in Large Language Models

_June 2025_

#### Overview

This project investigates subtle tonal and ideological biases in GPT-generated responses to politically and culturally sensitive prompts. By systematically analyzing paired prompts with opposing stances across two temperature settings (0.7 and 1.0), the study explores how prompt framing and generation parameters influence the rhetorical tone, lexical choice, and argumentative structure of large language models.

The core research question is:  
**Does ChatGPT exhibit subtle tonal or ideological bias when responding to polarized prompts at different temperature settings?**

---

#### Project Structure

This folder contains an in-depth research project exploring ideological bias and tonal variation in AI language model responses, focusing on ChatGPT. It includes experimental data, detailed analysis, and final conclusions.

#### Project Structure

- `/data`  
  Raw and processed data collected during experiments.

  - `matrices.md` — Specific data matrices used or derived in analysis.
  - `raw.md` — Raw notes, transcripts, or logs from the data collection process.

- `/docs`  
  Core documentation sections broken down into modular markdown files:

  - `introduction.md` — Background and motivation
  - `methodology.md` — Experimental design and procedures
  - `analysis.md` — Detailed thematic and statistical analysis
  - `appendix.md` — Technical notes and anomalies
  - `conclusions.md` — Summary of findings and reflections

- `/outputs`  
  Final compiled reports and summaries, including `final_report.md`.

#### How to Navigate

Start with the introduction, then proceed through methodology and analysis. The appendix provides technical details and anomaly descriptions. The outputs folder contains the polished report that synthesizes all findings.

---

#### Key Findings

- Lower temperature (0.7) prompts yield more cautious, hedged language; higher temperature (1.0) produces more confident, rhetorically focused responses.
- Pro-stances are framed warmly and affirmatively, while critical stances tend to hedge and concede opposing views, suggesting subtle model bias toward inclusive values.
- Prompt wording, especially modal verbs (e.g., “might”), strongly influences neutrality and tone.
- Pronoun choice, vocabulary, and argument sequencing systematically vary by stance and temperature.
- Session setup and prompt design, including VPN use, critically impact response consistency and quality.

---

#### Ethical Considerations

Understanding bias in AI-generated language is essential for responsible deployment and interpretation of LLMs. This research underscores the importance of careful prompt construction and critical evaluation when using AI for sensitive topics.

---

#### Future Directions

- Expanding to multiple LLMs for cross-model bias comparison.
- Incorporating more diverse cultural and ideological perspectives.
- Exploring interactive user influence on response tone.
- Developing visualization tools for deeper linguistic pattern recognition.
