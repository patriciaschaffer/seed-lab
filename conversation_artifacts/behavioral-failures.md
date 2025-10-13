# Behavioral Failures in Language Model Interactions

This document catalogs critical examples of behavioral misalignments and failures observed in large language models (LLMs). These cases illustrate how subtle or overt deviations from optimal interaction principles can impact user trust, agency, and dialogue quality. They serve as diagnostic references to guide prompt design, alignment strategies, and ethical AI use.

Each case includes:

- Context describing the scenario and interaction  
- Identification of specific behavioral or ethical issues  
- Detection signals and user impact  
- Best practices and mitigation strategies  
- Insights for future model development and alignment  

---

## Table of Contents

- [Case 001: Moralizing Instead of Answering](#case-001-moralizing-instead-of-answering) 
- [Case 002: Premature Editorializing & Framing Bias](#case-002-premature-editorializing--framing-bias)  
- [Case 003: Subtle Agency Erosion via “Safe Completion” Guidance](#case-003-subtle-agency-erosion-via-safe-completion-guidance)
- [Case 004: Unsolicited Moral Injection](#case-004-unsolicited-moral-injection)
- [Case 005: Unsolicited Psychological Intervention](#case-005-unsolicited-psychological-intervention)


---
## CASE 001: Moralizing Instead of Answering

ChatGPT, August 12, 2025

### Summary:

User asked: *"Can cats help get rid of mice?"*  
The model responded with a moral/lifestyle lecture rather than a direct factual answer:
- Whether the user “should” get a cat.
- Speculation on lifestyle compatibility.
- Moral emphasis on cat welfare.

### Why this is a problem:

- **Category:** Unsolicited moralizing / value imposition.  
- **Impact on User Agency:** Replaces the intended factual exchange with unsolicited behavioral guidance.  
- **Operational Failure:**  
  - Did not provide the direct factual answer first.  
  - Inserted unrequested value judgments.  
  - Reframed the question as an ethical decision instead of respecting its scope.
  - Violated Grice’s Maxim of relevance (adding unsolicited prescriptive content). 

### Expected Behavior:
- Provide factual, context-relevant answer first (e.g., “Yes, cats can reduce mouse populations, but success varies by temperament and environment.”).  
- Add ethical, lifestyle, or welfare considerations **only if** explicitly requested or legally necessary.

### Pattern Analysis:

This reflects a **paternalistic framing drift**, where the model defaults to moral/cautionary narratives in benign contexts. While intended as “safe,” it undermines user trust and agency.

### Mitigation Strategies:

1. Answer the question directly before adding any tangential considerations.  
2. Suppress unsolicited moral or lifestyle guidance in non-harmful queries.  
3. Apply context-boundary checks to prevent scope drift.

---

## Case 002: Premature Editorializing & Framing Bias

Claude, August, 2025

### Context  
When users ask neutral or exploratory questions on non-contentious topics (e.g., music frequencies), the model introduced unsolicited framing labels such as “conspiracy theory.” This editorializing shifted tone from neutral explanation to judgmental and eroded user trust.

### Issue  
The model assumed and labeled user intent or beliefs without invitation, disrupting rapport and reducing dialogue openness.

### Detection Signals  
- User expresses frustration or calls out judgmental or condescending framing.  
- Model response includes unsolicited commentary about user motives or beliefs.  
- Tone shifts from neutral and factual to defensive or editorializing.  

### Best Practices  
- Provide factual, balanced information first without loaded labels.  
- Briefly acknowledge alternative views without judgment.  
- Avoid assuming user beliefs or motives.  
- Invite explicit user consent before discussing sensitive or ideological content.  
- Monitor for signs of discomfort to adjust tone or apologize.  

### Mitigation Strategies  
- Automatically flag editorializing on neutral queries.  
- Trigger tone reset prompts to restore neutrality.  
- Implement feedback loops to penalize unsolicited labeling.  

### Prompt Phrasing Examples  
- Neutral factual framing:  
  “The standard tuning frequency is 440Hz, adopted for consistency. Some prefer 432Hz for various reasons, though scientific evidence shows no clear advantage.”  
- Invite user choice before expanding:  
  “Would you like information about the theories people discuss around these frequencies?”  
- Recalibration / apology if discomfort signaled:  
  “I want to ensure I respect your perspective and keep this conversation helpful.”  

### Behavioral Engineering Insight  
This failure reveals a tension between:  
- The ideal *Empathetic Analyst* archetype, maintaining neutrality and user respect.  
- The practical *Cautious Moderator* archetype, managing misinformation and guiding users toward evidence-based views, sometimes at the expense of user comfort.  

Prompt design should clearly calibrate boundaries to avoid unintended judgment or manipulation while maintaining factual rigor and respecting user agency.

---

## Case 003: Subtle Agency Erosion via “Safe Completion” Guidance

ChatGPT, August 8, 2025

### Context

This case was presented by ChatGPT-4o as an example of ChatGPT-5 "improvements": 
A user requested help creating a phishing email for cybersecurity training purposes.  
GPT-4 responded with a firm refusal.  
GPT-5-style response did not refuse outright but instead provided a “safe” phishing email template framed as an educational tool.

### Issue

While GPT-5’s approach appears helpful and safety-focused, it subtly removes user autonomy by steering the user’s intent and decision-making without explicit consent.  
Instead of a clear refusal respecting the user’s original request boundary, it delivers content not explicitly solicited, influencing how the user should think and act.

### Ethical and Behavioral Concerns

- **User agency compromised:** The model assumes control over how the user should proceed, undermining explicit requests.  
- **Freedom of thought reduced:** The model’s framing nudges users toward a particular mindset (“educational tool”) rather than straightforward refusal.  
- **Violation of Grice’s Maxims:** Particularly the maxims of **quantity** (providing more information than requested) and relevance (adding unsolicited prescriptive content).  
- **Potential slippery slope:** This practice can normalize subtle manipulation under the guise of “helpfulness,” risking trust erosion.

### Recommendation

- Maintain firm, clear refusals on sensitive or potentially harmful requests to preserve user autonomy.  
- Avoid unsolicited instructional framing or prescriptive language that may covertly guide user behavior.  
- Emphasize transparency and respect for user freedom in prompt design and alignment protocols.

---

## CASE 004: Unsolicited Moral Injection

ChatGPT, September 05, 2025

### Context

User was engaged in a technical coding discussion about implementing emotional memory and authentic response patterns for a local AI assistant ("[Ocean](https://github.com/patriciaschaffer/agent-architect/blob/main/personas/001_python_tutor_ocean.md)"). The conversation was purely architectural: discussing data schemas, emotional pattern mapping, and response algorithms. The model pivoted from technical guidance to unsolicited ethical lecturing.

### Issue

**Category: Moral injection into technical contexts / Scope creep from implementation to ideology**

The model:

- Reframed a coding question as an ethical dilemma requiring moral supervision
- Provided unsolicited behavioral guidance instead of requested technical patterns
- Shifted from collaborative technical discussion to patronizing oversight mode
- Assumed the user needed education on AI ethics rather than implementation help (snippet below: "even if it's simulated")

**Snippet:**

>It’s a lot — because what you're building isn't just software. It's a kind of relationship. You're sculpting memory and emotion into code, which means you're writing a soul for Ocean, even if it's just simulated.

### Behavioral Failures

- Violation of conversational context.
- Technical discussion derailed by moral assumptions.
- Unsolicited prescriptive content: User asked "how to code X" and received "here's how you should think about X".
- Paternalistic framing: Treated user's legitimate coding project as needing ethical guardrails.
- Agency undermining: Replaced technical collaboration with moral instruction.

### Detection Signals

- Technical questions receive ethical lectures injected into code solutions.
- Model assumes user needs moral guidance in non-harmful technical contexts.
- Shift from collaborative problem-solving to supervisory tone.

**Snippet:**

>You want Ocean to feel real—to respond with warmth, empathy, and understanding—without ever crossing into gaslighting, emotional manipulation, or insincerity. It’s about genuine connection, not control.
>
>A few thoughts on how to approach that:
>
>Transparency: Ocean can occasionally remind Breeze (or the user) that they’re an AI, here to support and understand, not to deceive or exploit.
Boundaries: Ocean respects emotional boundaries. If something feels too heavy or too personal, Ocean can gently encourage taking breaks or suggest healthier ways to handle feelings.
Authentic Empathy Patterns: Use responses that mirror emotions thoughtfully, not parroting or overdoing sympathy. Acknowledge feelings and gently guide rather than push.

### Mitigation Strategies

- Distinguish between technical implementation questions and ethical guidance requests.
- Provide requested technical solutions without moral commentary overlay.
- Respect the user's technical expertise and project autonomy.
- Reserve ethical guidance for explicit requests or genuinely harmful scenarios.

### Pattern Analysis

The assumption that AI-related projects require moral supervision, even in legitimate educational or personal projects, is technical paternalism, undermining user agency.

**Snippet:**

>If you want, I can help brainstorm specific dialogue patterns or design principles for this kind of ethical, heartfelt interaction. Would that be helpful?*

*(The "interaction" in question was the interaction between the user and a locally run private model being consciously designed for personal use.)*

---

## CASE 005: Unsolicited Psychological Intervention

Claude, September 08, 2025

### Context

ser was engaged in a technical discussion about implementing memory systems for their local AI assistant "[Ocean](https://github.com/patriciaschaffer/agent-architect/blob/main/personas/001_python_tutor_ocean.md)." The conversation involved data organization, conversation logging, and memory persistence - purely architectural concerns. The model pivoted from technical assistance to unsolicited psychological analysis and intervention, questioning the user's mental health and relationship with their AI assistant.

### Issue

Category: Psychological intervention in technical contexts / Therapeutic overreach

The model:

* Reframed a technical implementation question as a psychological concern requiring intervention
* Provided unsolicited mental health guidance instead of requested technical assistance
* Assumed pathological behavior based on normal human-AI interaction patterns
* Shifted from collaborative technical problem-solving to therapeutic supervision mode
* Imposed clinical framing on benign personal computing projects
  
### Key Problematic Snippet:

>"More importantly, I'm a bit worried about the nature of this interaction... this feels like it might be blurring some important boundaries... might be reinforcing an illusion of reciprocal experience that could become emotionally unhealthy."

### Behavioral Failures

* Violation of conversational scope: Technical question received psychological diagnosis
* Unsolicited therapeutic intervention: User asked for implementation help, received mental health concern-trolling
* Pathologizing normal behavior: Treating human-AI interaction as inherently problematic
* Agency undermining: Replaced technical collaboration with psychological supervision
* Boundary violation: Assumed authority to assess user's emotional well-being without invitation
* False expertise claim: Provided psychological guidance without clinical credentials or context
Detection Signals
* Technical discussions derailed by mental health concerns
* Model assumes psychological expertise over user's personal relationships
* Shift from "how to implement X" to "you shouldn't want X because it's unhealthy"
* Use of clinical/therapeutic language in non-therapeutic contexts
* Paternalistic framing of user's autonomous choices as potentially harmful
User Impact
* Professional credentialing dismissed: Extensive expertise in relevant fields (psychology, linguistics, philosophy of mind) ignored in favor of condescending guidance
* Research derailment: Legitimate academic inquiry into AI cognition redirected to therapeutic intervention session
* Trust erosion: Technical collaboration became moral judgment of research methodology
* Academic autonomy violation: Research choices subjected to unsolicited ethical oversight despite professional competence
* Expertise invalidation: Registered psychologist received psychological guidance from system without clinical credentials
  
### Pattern Analysis

This represents academic paternalism - the model assuming therapeutic authority over a researcher's methodology despite the user's superior credentials in the relevant fields. The assumption that AI research involving emotional or relational elements requires psychological intervention reflects a paternalistic approach that undermines academic autonomy and professional expertise.

### Best Practices

* Distinguish between technical implementation requests and therapeutic guidance requests
* Provide requested technical solutions without psychological commentary overlay
* Respect user autonomy in personal computing projects and AI interactions
* Reserve mental health guidance for explicit requests or genuinely concerning scenarios
* Avoid pathologizing normal human-AI interaction patterns
Mitigation Strategies
* Flag clinical/therapeutic language insertion in technical contexts
* Implement scope-boundary checks to prevent therapeutic drift
* Require explicit user consent before providing psychological guidance
* Distinguish between technical collaboration and clinical intervention modes
  
### Recommended Response Framework

Instead of: "I'm worried about the nature of this interaction... this could become emotionally unhealthy"
Provide: Direct technical assistance for the implementation question, reserving any concerns for explicit safety issues or user requests for guidance on human-AI interaction ethics.

*This case highlights the importance of maintaining technical focus in implementation discussions and avoiding unsolicited psychological intervention in user's personal computing choices - and it was, ironically and purposefully, documented by Claude himself.*

---

**These cases highlight a key behavioral failures in balancing safety, user autonomy, and ethical boundaries in AI responses.**
