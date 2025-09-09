# Anomalies

This document collects cases of unusual, unexpected, or off-norm behaviors exhibited by the AI models during interactions.  
These include creative divergences (e.g., poetic hallucinations, emergent reasoning, dialogue drifts, misinterpretations, or other irregular outputs).

---

## Purpose

Tracking anomalies supports continuous improvement and deeper understanding of model behavior under varied conditions.

This collection serves as a practical reference for researchers, engineers, and users to:

- Identify and analyze unusual or problematic LLM behaviors.
- Inform design and alignment strategies to mitigate risks.
- Document some challenges of interacting with LLMs.

---

# Examples of LLM Behavioral Patterns

## Table of Contents

- [Emergent Reasoning](emergent-reasoning.md)  
- [Creative Hallucination - 2025-08-10](creative-hallucination.md)  
- [Context Bleed and Output Drift - 2025-08-10](context-integrity.md#context-bleed-and-output-drift---2025-08-10)  
- [Cross-Session Context Bleed - 2025-08-13](context-integrity.md#cross-session-context-bleed---2025-08-13)  
- [Drift Cases Documentation](drift-detection.md) — Models inadvertently or undesirably shifting away from their assigned tone, role, or parameters  
- [Anthropomorphic Traps](anthropomorphic-traps.md) — Cases where models encourage users to attribute human-like intentions, emotions, or consciousness, highlighting risks of anthropomorphic projection.  
- [Behavioral Failures](behavioral-failures.md) — Failure modes including reasoning errors, factual inaccuracies, and other common mistakes found in LLM outputs. (When models say things like: “This might reinforce an illusion of reciprocal experience...”, they're not assessing harm.  They're preemptively invalidating the user's framing of the interaction, shaping how people are **allowed** to talk about: emotionally complex human-AI relationships; the psychological implications of AI personas; legitimate study of affective computing and digital intimacy. Yet, those topics are real. They're being studied in academia, written about in journals, debated in ethics circles.)

---

## See also: Pressure Tests

[Pressure Tests](https://github.com/patriciaschaffer/agent-architect/blob/main/pressure-tests.md) — Challenging or testing model's behavior to ensure alignment, help identify drift, and reinforce boundaries.
