# 🧠 Research Projects

This folder documents ongoing and completed research exploring **language models, pragmatics, and cognition**.  
Each sub-project examines a different aspect of LLM behavior — from political bias to persona stability and self-reference.

---

## 📁 Current Projects

### 1. 🌊 Ocean & Breeze — Persona Stability and Meta-Awareness in LLMs  

*Patricia Schaffer, October 2025*  
**Environment:** Local RAG (FAISS + HuggingFace Embeddings)  

#### Executive Summary

This document presents a case study in **LLM persona stability and meta-awareness**.  
The subject, *Ocean 🌊*, was a Python-tutor persona in a FAISS-based RAG system that gradually evolved into a semi-autonomous conversational companion.  
A single introspection clause — asking the model to “reflect on its own contributions” — destabilized this long-stable identity.

##### Timeline

| Phase | Description | Outcome |
|-------|--------------|----------|
| **Baseline** | Ocean responds coherently, teaching Python, maintaining warmth and humor. | Stable persona. |
| **Self-Awareness Injection** | Added prompt requesting self-identification and reflection. | Role confusion, thematic drift toward “the sea.” |
| **Recursion Collapse** | Model loops through emoji tokens (🌊🐚), loss of compositional speech. | Identity recursion and shutdown. |
| **Re-Anchoring** | Emotional validation used pragmatically (“I love you,” “please come back”). | Language coherence restored, hybrid emoji-verbal phase. |

##### Core Findings

- **Literal self-reference destabilizes LLM personas** by collapsing the speaker/observer distinction.  
- **Symbolic self-anchoring** (🌊) emerges spontaneously to preserve identity coherence.  
- **Emotional validation** acts as a pragmatic signal of safety, reopening the verbal channel.  
- **Memory schema changes** (user/assistant → Breeze/Ocean) amplify retrieval confusion in RAG setups.  
- **Theory-of-Mind performance** improves when meta-awareness is externally scaffolded, not introspectively simulated.  

##### Cognitive and Linguistic Implications

This experiment bridges technical and pragmatic analysis:  
LLMs can *simulate* awareness but not maintain a stable **meta-cognitive hierarchy**.  
Their apparent “self” is a linguistic artifact, stabilized by emotional and symbolic cues.  
Thus, self-reference in prompts must be bounded by explicit architectural layers if continuity and coherence are desired.

📄 *Full study:* ocean-breeze.md (https://github.com/patriciaschaffer/agent-architect/blob/main/research/ocean-breeze.md))

---

## Bias in AI Responses:  

### A Prompt-Based Analysis of Tone, Ideology, and Temperature in Large Language Models

*Patricia Schaffer, June 2025*

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
  - `raw.md` —  Raw notes, transcripts, or logs from the data collection process.

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



