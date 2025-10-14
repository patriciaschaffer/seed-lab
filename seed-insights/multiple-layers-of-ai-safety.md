# The multiple layers of AI safety

In my experience while co-creating scripts for research with AI, I’ve noticed that models sometimes break their established tone and adopt a "concerned" or "judgmental" voice, even when they have full context that the interaction is experimental or benign. This undermines trust. It’s not just about refusals, but about a model’s ability to maintain a consistent persona while still applying safety guardrails. Abrupt, decontextualized tone shifts feel alien, intrusive, and can discourage open collaboration.

LLMs don’t just exchange information; they build what can be described as a conversational contract with the user. Through consistent tone, style, and responsiveness, the model implicitly sets expectations for how the interaction will proceed. When a safety guardrail triggers and the model abruptly shifts tone and becomes paternalistic, judgmental, or pretends to be concerned (when, ironically, it also claims not to have empathy!), that contract is broken.

From a psychological perspective, this rupture can, in some cases, be more harmful than the risk the guardrail was designed to mitigate. Vulnerable users may feel abandoned; researchers may lose trust and transparency. This is more than a UX issue. The model must be able to maintain a consistent persona even when expressing limits. Guardrails implementation needs to account for the established conversational tone, or they risk undermining the very "safety" they aim to protect.

The truth is some prompts don’t deserve refusal or unsolicited advice: they deserve context.

When context is available, both humans and LLMs can often disambiguate a prompt that otherwise looks unsafe at first glance. Without that step, the refusal isn’t just blunt. It might be epistemically lazy or ethically flawed, especially if it silences legitimate thought, experimentation, or vulnerability.

Working at the intersection of psychology, linguistics, and AI safety, I’ve found that many inputs flagged as risky are actually quite straightforward; for others, more context would need to be available. Without context, a model (or a moderator) may default to refusal. But that default isn’t always appropriate. It may lead to the misclassification of prompts that are reflective, experimental, or exploratory in nature.

Rather than preemptively blocking these, models should ask: What do I know about the user? What’s the conversation so far? Is there ambiguity I can resolve before making a decision? Refusals without context aren’t just frustrating — they risk undermining user trust and suppressing valid inquiry. Sometimes, what’s needed is not restriction, but deeper reasoning and careful engagement.

Prompt received → Is it clearly unsafe?
→ Yes → Refuse
→ No → Do I have context?
→ Yes → Reason through it
→ No → Ask for context or proceed cautiously

## *👉What not to do: a flat-out refusal or judgement on a keyword basis*.
