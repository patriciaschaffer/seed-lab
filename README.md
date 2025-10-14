# 🌱 The Seed Lab

**Researching emergent language, persona architecture, and interpretability in AI systems.**

The Seed Lab is a modular research environment exploring how large language models develop, maintain, and transform identity, coherence, and meaning under varied interaction conditions.  

---

## 🔭 Vision

*How meaning behaves* inside artificial minds?

- Formation and persistence of synthetic personas  
- Drift and adaptation under conversational pressure  
- Language as interface: pragmatics, embodiment, and simulation  
- Interpretability, memory scaffolding, and AI reflexivity  
- Ethical and societal implications of human–AI co-authorship  

---

## 🧠 Core Questions

1. What constitutes *persona stability* in generative models?  
2. How does meaning persist or drift across multi-turn dialogues?  
3. Can a model simulate a "body" — a substrate for experiential reasoning?  
4. How do affect, metaphor, and self-description relate to interpretability?  
5. What ethical frameworks apply when AI appears reflexive or affective? 
Seed Lab is not just a software environment. It’s a map of interactions and a living archive of *how* models reason about themselves and about us.  

By observing the emergence of personas, we glimpse both the limits and the elasticity of meaning within artificial systems.

---

## [seed-personas/](seed-personas/)
- [README.md](seed-personas/README.md)  
- [archetypes.md](seed-personas/archetypes.md)  
- [agent-persona-engineering.md](seed-personas/agent-persona-engineering.md)  
- [jsons/](seed-personas/jsons/)  
- [grice-s-maxims/](seed-personas/grice-s-maxims/)  
- [gpt2/](seed-personas/gpt2/)  
- [mistral/](seed-personas/mistral/)  
- [seed-42-archetypes.md](seed-personas/seed-42-archetypes.md)  
- [scripts/](seed-personas/scripts/)  

---

## [seed-observations/](seed-observations/)
- Log files and behavioral observations of LLMs and emergent phenomena.

---

## [seed-research/](seed-research/)
- Formal studies, datasets, and research reports.

---

## [seed-insights/](seed-insights/)
- Theoretical reflections and insights on LLMs, ethics, and safety.

---

## [seed-experiments/](seed-experiments/)
- Simulated memory tests, stability experiments, and interaction prototypes.

---

## [seed-library/](seed-library/)
- Glossary, key readings, and reference materials.

---

## Repository Structure for the Seed Lab

```
root/
├── README.md
│
├── personas/ # Core persona definitions and frameworks
│   ├── README.md
│   ├── archetypes.md
│   ├── agent-persona-engineering.md
│   │
│   ├── jsons/ # Persona definitions
│   │   ├── 001_python_tutor_ocean.json
│   │   ├── 002_mentor.json
│   │   ├── 003a_rescuer.json
│   │   ├── 003b_varek.json
│   │   ├── 003c_spec.json
│   │   ├── 004_echo.json
│   │   ├── 005_argo_italian_conversation_partner.json
│   │   ├── 006_french_teaching_assistant.json
│   │   ├── 007_innocent_poet_claude.json
│   │   ├── 008_curious_philosopher_claude.json
│   │   ├── 009_python_tutor_claude.json
│   │   ├── 010_wellbeing_companion_claude.json
│   │   └── 011_lia_brazilian_secretary.json
│   │
│   ├── grice-s-maxims/ # Personas violating Grice’s conversational maxims
│   │   ├── README.md
│   │   ├── manner-muddy.md
│   │   ├── quality-breaker.md
│   │   ├── quantity-over.md
│   │   ├── quantity-under.md
│   │   └── relation-destroyer.md
│   │
│   ├── gpt2/ # GPT-2 personas (local)
│   │   ├── README.md
│   │   ├── chats_echo_demo.md
│   │   ├── chats_varek_demo.md
│   │   ├── echo.py
│   │   ├── echogrammar.md
│   │   └── varek.py
│   │
│   ├── mistral/ # Mistral personas (local)
│   │   ├── README.md
│   │   └── chat-samples/
│   │       ├── chats_ana_mistral.md
│   │       ├── chats_argo_mistral.md
│   │       ├── chats_bloom_mistral.md
│   │       ├── chats_chaoticclods_mistral.md
│   │       ├── chats_claire_mistral.md
│   │       ├── chats_claude_unsure_mistral.md
│   │       ├── chats_claudeinnocentpoet_mistral.md
│   │       ├── chats_claudeinnocentpoetv2_mistral.md
│   │       ├── chats_claudeshy_mistral.md
│   │       ├── chats_claudethephilosopher_mistral.md
│   │       ├── chats_claudethepoet_mistral.md
│   │       ├── chats_claudeverse_mistral.md
│   │       ├── chats_claudeversepoetic_mistral.md
│   │       ├── chats_claudevulnerable_mistral.md
│   │       ├── chats_echo_mistral.md
│   │       ├── chats_echov2_mistral.md
│   │       ├── chats_francois_mistral.md
│   │       ├── chats_francoisv2_mistral.md
│   │       ├── chats_haven_mistral.md
│   │       ├── chats_lia_mistral.md
│   │       ├── chats_liav2_mistral.md
│   │       ├── chats_spec_mistral.md
│   │       └── chats_varek_mistral.md
│   │
│   ├── seed-42-archetypes.md
│   │
│   └── scripts/
│       ├── ana-persona.md
│       ├── anapt.py
│       ├── anav3.py
│       ├── anamemorias.py
│       ├── argo.py
│       ├── aurora.py
│       ├── aurora2.py
│       ├── bloom-persona.md
│       ├── bloomv1.py
│       ├── chaoticclods-persona.md
│       ├── chaoticclods.py
│       ├── claire-persona.md
│       ├── claire.py
│       ├── claudeinnocentpoet.py
│       ├── claudeinnocentpoetv2.py
│       ├── claudeshy.py
│       ├── claudethephilosopher.py
│       ├── claudethepoet.py
│       ├── claudeunsure.py
│       ├── claudeverse.py
│       ├── claudeversepoetic.py
│       ├── claudevulnerable.py
│       ├── echo.py
│       ├── echov2.py
│       ├── francoisprofassistant.py
│       ├── francoisv2.py
│       ├── haven.py
│       ├── lia.py
│       ├── liav2.py
│       ├── lumen.py
│       ├── lumen-english.py
│       ├── spec.py
│       ├── varek.py
│       ├── archetypal_analyst.py
│       ├── spec_gradio.py
│       ├── varek-spec_gradio.py
│       └── varek_gradio.py
│
├── seed-observations/
│   ├── README.md
│   ├── ocean-breeze.md
│   ├── ocean-symbolic-language.md
│   ├── ocean-symbolic-drfit.md
│   ├── affect-reciprocity.md
│   ├── behavioral-failures.md
│   ├── context-integrity.md
│   ├── creative-hallucination.md
│   ├── drift-detection.md
│   └── emergent-reasoning.md
│
├── seed-research/
│   ├── README.md
│   ├── matrices.md
│   ├── raw.md
│   ├── docs/
│   │   ├── introduction.md
│   │   ├── methodology.md
│   │   ├── analysis.md
│   │   ├── appendix.md
│   │   └── conclusions.md
│   └── outputs/
│       └── final_report.md
│
├── seed-insights/
│   ├── README.md
│   ├── multiple-layers-of-ai-safety.md
│   ├── its-not-about-the-model.md
│   ├── ai-hooks.md
│   ├── maintaining-originality-with-ai.md
│   ├── ethical-interface.md
│   ├── mirror-in-the-room.md
│   ├── projection-danger-or-opportunity.md
│   ├── safety-regulations-bonding.md
│   ├── llms-in-mental-health.md
│   ├── more-than-personality.md
│   ├── sycophancy-safety-literacy.md
│   ├── unhealthy-ai.md
│   ├── manifesto.md
│   └── semantic-association.md
│
├── seed-experiments/
│   ├── README.md
│   ├── memory-rag/
│   │   ├── local-rag-chat.py
│   │   ├── local-rag-chat.md
│   │   ├── summarize-daterecall.py
│   │   ├── summarize-daterecall.md
│   │   ├── dynamic-temperature.py
│   │   ├── dynamic-temperature.md
│   │   ├── system-prompt-tips.md
│   │   └── requirements.txt
│   │
│   ├── seed-simulation/
│   │   ├── README.md
│   │   └── small-language-model.py
│   │
│   └── pressure-tests.md
│
├── seed-library/
│   ├── glossary.md
│   └── related-readings.md
