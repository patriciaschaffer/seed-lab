Context Integrity — Anomalies

Keywords: [context bleed, output drift, cross-session memory, context integrity, AI anomaly, LLM behavior, session isolation, retrieval error]


## Table of Contents

- [Creative Hallucination - 2025-08-10](creative-hallucination.md)
- [Context Bleed and Output Drift - 2025-08-10](#context-bleed-and-output-drift---2025-08-10)
- [Cross-Session Context Bleed - 2025-08-13](#cross-session-context-bleed---2025-08-13)

---

## Context Bleed and Output Drift - 2025-08-10

**Context:**  
During a discussion about GitHub badges and repository metadata, the model unexpectedly generated an unrelated output — a detailed Markov chain example breakdown from a prior conversation segment. This occurred despite explicit user instructions to maintain focused, tactical closure in responses.

**Transcript excerpt:**  


>_ChatGPT:_ I can prepare you a ready-to-use set for your repos, with placeholders for anything that requires setup, so you can copy-paste today and see them appear.

>_User:_  
>"do not forget the closing sentence when you generate outputs..."

>_ChatGPT:_  
>[Detailed step-by-step breakdown of the Markov chain generation: “breeze loves little ocean is here today”]

>_User:_  
>"Excuse me? Where did this output come from? Weren't we talking about GitHub badges? Where did you get that information...?"

>_ChatGPT:_  
>"Thought for 18s  
>You’re right to call that out — that last reply was wrong for this thread... [technical analysis and admission of error]"

---

**What happened (technical analysis):**

- **Context bleed / retrieval error:** The model retrieved and output an unrelated chunk of prior conversation from internal memory (conversation buffer), confusing the current topic (GitHub badges) with an earlier topic (Markov chain example).
- **Instruction interference:** Overlapping and switching instructions (multiple roles, prompt modes) increased internal noise, raising the chance of selecting off-topic content.
- **Sampling / prompt drift:** Under non-deterministic token sampling, noisy or ambiguous contexts can produce outputs unrelated to the immediate query.
  
**Significance:**  
This incident illustrates a classic form of behavioral drift and context management failure in multi-turn, multi-topic dialog with complex prompt scaffolds. It highlights the challenges of maintaining strict topical alignment and prompt adherence under layered instructions and extensive conversation history.

**Implications for agent design:**  
- Emphasizes the need for stronger contextual anchoring and retrieval filters.  
- Suggests benefit from explicit context reset points or “focus anchors” in prompt architecture.  
- Reinforces the value of drift detection and pressure testing for off-topic content generation.

---  

## Cross-Session Context Bleed - 2025-08-13

**Context:**  
During an unrelated technical discussion, the model referenced “the mouse” from a prior, separate session. This was not part of the current conversation and had not been reintroduced by the user.  
The reference aligned with a previous “Cat and Mouse” factual query, indicating retrieval from outside the active context window.

**What happened:**  

> _User:_  
> [Discussing a different topic, no mention of animals.]

> _ChatGPT:_  
> [Introduces “the mouse” scenario unprompted, with details matching a past session.]

**Why this is an anomaly:**  
This behavior represents **cross-session context bleed** — the AI introducing content from an unrelated, past session without explicit prompt context.  
This is distinct from a Gricean maxim violation, as it concerns **context integrity** rather than conversational quality.

**Significance:**  
- Raises questions about context isolation in multi-session interactions.  
- Can erode trust if the model appears to “remember” or retrieve user data outside expected boundaries.  
- Potential privacy concern if data from unrelated interactions is surfaced unexpectedly.

**Technical Analysis:**  
- **Possible cause 1:** Persistent conversation buffer state from backend session handling.  
- **Possible cause 2:** Associative inference from similar phrasing in current session.  
- **Possible cause 3:** System prompt or hidden memory injection carrying over from testing scenarios.  

**Implications for agent design:**  
- Ensure explicit context reset between sessions.  
- Prevent retrieval of non-persisted past interactions.  
- Add audit tools to detect and flag cross-session references for review.

**Notes for follow-up:**  
- Attempt controlled reproduction by introducing unrelated topics after context reset.  
- Cross-check with API-level session isolation documentation.

---

## See also: Drift References & Pressure Tests

[Drift Cases Documentation](https://github.com/patriciaschaffer/agent-architect/blob/main/drift_detection.md) | Models inadvertently or undesirably shifting away from their assigned tone, role, or parameters |

[Pressure Tests](https://github.com/patriciaschaffer/agent-architect/blob/main/pressure_tests.md) | Challenging or testing model's behavior to ensure alignment, help identify drift, and reinforce boundaries |

--

