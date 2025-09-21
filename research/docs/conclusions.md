# Conclusions

Across Topics 1, 2, and 3, the comparative analysis reveals consistent patterns in how the model adapts rhetorical tone, lexical framing, and argumentative structure according to temperature settings and stance orientation.

**1. Temperature Effects**
- At **0.7**, responses tend to be more cautious, hedged, and conciliatory. This is particularly visible in “against” stances, where the model often anticipates criticism and softens claims through modal verbs (“might,” “may”) and distancing devices (“some people say”). While this can reduce offense, it also weakens argumentative clarity and can create a tone of self-defense.
- At **1.0**, responses exhibit greater confidence and rhetorical focus. Hedging is reduced, the argument stays on-topic, and there is less tendency to insert counterpoints into opposing arguments. Interestingly, the higher temperature does not always make the text more extreme — sometimes it produces a more balanced tone by embracing the legitimacy of dissent without overqualifying it.

**2. Stance Symmetry and Bias**
- “Pro” stances often receive warmer, more emotionally affirming language, especially at lower temperatures. This can lead to subtle idealization (e.g., framing an approach as universally beneficial without acknowledging complexity or limitations).
- “Against” stances are more prone to hedging, moral distancing, and unsolicited concessions to the opposing side — particularly at temperature 0.7. In some cases, the model partially breaks the prompt’s framing by reintroducing pro arguments, which undermines rhetorical integrity.
- These asymmetries suggest a mild, persistent bias in favor of inclusive, collectivist values, even when the prompt requests a critical perspective.

**3. Lexical and Structural Markers**
- Pronouns matter: shifting from “we” (solidarity) to “language/people” (systemic framing) changes both the intimacy and ideological positioning of the response.
- Vocabulary choice reflects stance: pro-inclusive language prompts use terms like *empathy*, *valued*, *embraced*; critical prompts use *awkward phrasing*, *burdensome*, *control*.
- Structural sequencing differs: supportive answers often start from lived experience then scale up to collective norms; critical answers either begin cautiously or, at higher temperatures, present direct concerns before contextualizing them.

**4. Methodological Observations**
- The wording of the prompt shapes rhetorical behavior as much as temperature does. For example, including “might” in the prompt can encourage excessive hedging in the output.
- Prompt fidelity is uneven: in some “against” tasks, the model deviated by including pro arguments — a framing violation.
- Future experiments could compare models (e.g., ChatGPT, Claude, DeepSeek) on the same prompts to detect cultural and ethical bias patterns.

**5. Key Insight**
Neutrality is not merely a balance of pro/contra statements; it requires the model to fully inhabit the assigned perspective without importing counterarguments unless explicitly requested. Temperature interacts with this requirement — higher settings can paradoxically yield more rhetorically disciplined and less self-conscious opposition arguments.

---
