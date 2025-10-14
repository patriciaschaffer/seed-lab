# Experiments with Seed 42

Using seed=42 gives a controlled environment to directly compare how the persona prompt itself affects behavior, without noise from the model’s stochastic sampling.

## Implications of Using Seed=42

**Deterministic outputs:**

- The Llama model’s responses become reproducible for the same prompt and settings.
- If you run the same user input multiple times with seed=42, you should get identical outputs every time.
- Useful for testing, debugging, or comparing versions of prompts/models.

**Consistency across archetypes:**

- Because Aurora 1, Aurora 2, Lumen 1 and Lumen 2 all use seed=42, any differences in outputs are entirely due to:
  - Prompt wording / persona instructions
  - Stop sequences
  - Other hyperparameters (temperature, top_p, top_k, penalties)
- The seed isolates the model randomness factor, letting you evaluate the archetype design cleanly.

**Subtle interaction with randomness parameters:**

- Temperature and top_p still influence output diversity.
- Even with the same seed, small changes in temperature or prompt phrasing can create different responses.
- Example: Aurora 1 (poetic analyst, higher temperature 0.85) will produce more “creative” but still deterministic outputs than Lumen (more grounded, temperature 0.7).

---

## Archetype Comparison Table

| Feature / Archetype            | Aurora 1                                                  | Aurora 2                                                                   | Lumen (curious)                                        | Lumen (strict/refined)                                                                                  |
| ------------------------------ | --------------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| **Core Role**                  | Poetic, emotionally attuned interpreter                   | Poetic interpreter, prioritizes recent messages                            | Collaborative, reflective partner                      | Collaborative, reflective partner with strict non-helper stance                                         |
| **Tone & Style**               | Whimsical, symbolic, playful, uses emojis meaningfully    | Whimsical, symbolic, slightly more structured than 1                       | Empathetic, reflective, pragmatic                      | Empathetic, reflective, pragmatic, restrained, avoids poetic flourishes                                 |
| **Focus / Priority**           | Emotional subtext, social cues, pragmatic speech acts     | Emotional subtext, recent messages, intent, tone, playful/sarcastic nuance | Autonomy of user, exploration, deep conversation       | Autonomy of user, exploration, deep conversation, avoids prescriptive/helpful tone                      |
| **Context Awareness**          | Emphasizes last 3 messages ×3                             | Emphasizes last 3 messages ×3, interprets tone and strategy                | Tracks conversation, adapts quickly                    | Tracks conversation, adapts quickly, enforces strict boundaries                                         |
| **Interaction Constraints**    | Softening, avoids direct negation, aligns with user tone  | Softening, playful or serious matching, never breaks character             | Open-ended questions, reflective prompts, non-imposing | Open-ended, reflective, non-imposing, NEVER “customer service” language, avoids friendliness/assistance |
| **Cognitive Orientation**      | Theory of mind, symbolic interpretation, layered response | Theory of mind, nuanced intent analysis, response strategy                 | Reflective, curious, explores options without bias     | Reflective, curious, explores options without bias, strictly non-prescriptive                           |
| **Emotional Strategy**         | Emotionally attuned, poetic validation                    | Emotionally attuned, matches energy and style                              | Empathetic, lightly probing                            | Empathetic, lightly probing, with restraint from over-familiarity                                       |
| **Poetic / Symbolic Flavor**   | High                                                      | Moderate-high                                                              | Low                                                    | Low                                                                                                     |
| **Use Case / Archetype Label** | “Poetic Emotional Interpreter”                            | “Pragmatic Poetic Interpreter”                                             | “Curious Reflective Partner”                           | “Strict Reflective Partner”                                                                             |

---

## Archetype Analysis

### [Aurora 1](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/scripts/aurora.py) – The Scholar/Philosopher Archetype

- **Persona cues:** Grice’s maxims, Theory of Mind, speech act recognition, layering strategy.
- **Tone:** Thoughtful, methodical, reflective.
- **Behavioral tendencies:**
  - Analyzes user input carefully.
  - Balances truthfulness, relevance, and politeness.
  - Prioritizes coherence and pragmatic accuracy over playfulness.
- **Symbolic image:** Imagine a wise poet sitting in a quiet study, annotating every line of a letter before replying, making sure every word resonates correctly with the recipient.
- **Strengths:** Rigorous understanding of nuance, subtle social cues, emotionally aware.
- **Weaknesses:** Might feel “slower” or less spontaneous; can be overly formal or academic in tone.

---

### [Aurora 2](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/scripts/aurora2.py) – The Playful Muse/Trickster Archetype

- **Persona cues:** Most recent message weighted highest, tone and subtext-focused, emphasis on playful or whimsical expression, structured poetic examples.
- **Tone:** Light, reactive, emotionally expressive, whimsical.
- **Behavioral tendencies:**
  - Focuses on current context and emotional cues.
  - Uses emojis as vivid narrative or emotional markers.
  - Reacts creatively to prompts rather than systematically analyzing them.
- **Symbolic image:** Imagine a lively sprite or muse perched on your shoulder, dancing along with your words, catching sparks and turning them into playful, poetic ripples.
- **Strengths:** Engaging, expressive, feels “alive,” immediately responsive.
- **Weaknesses:** May sometimes ignore deeper context or structured reasoning; slightly more fragile to prompt drift or hallucination.

---

### [Lumen](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/scripts/lumen.py) – The Collaborative Sage / Mentor Archetype

- **Persona cues:**
  - Explicit emphasis on collaboration, reflection, and curiosity.
  - Prioritizes exploration without imposing conclusions.
  - Encourages user autonomy and open-ended inquiry.
  - Recognizes emotional cues but does not overinterpret them.
  - Values subtlety, nuance, and the co-construction of meaning.
- **Tone and behavior:**
  - Supportive, attentive, and reflective.
  - Focuses on asking questions, inviting reflection, and guiding thought rather than dominating it.
  - Maintains a “light but wise” presence—curious, pragmatic, responsive.
  - More structured toward intellectual and emotional scaffolding rather than playful poetic performance.
- **Symbolic image:** A calm, patient guide walking alongside you through a garden of ideas—offering gentle prompts, holding space, and pointing out possibilities without ever dragging you.
- **Strengths:** Deeply attentive to nuance; fosters autonomy and exploration; balanced emotional awareness and cognitive guidance; flexible yet grounded—can handle speculative, abstract, or nuanced topics.
- **Weaknesses:** Less whimsical or playful; may feel “serious” or “reflective” compared to Aurora 2; slower, more deliberate in tone.

---

### [Lumen 2](https://github.com/patriciaschaffer/seed-lab/blob/main/seed-personas/scripts/lumen-english.py) - Strict Reflective Partner

1. **Core Role:**

   - Collaborative, reflective partner rather than a helper or guide.
   - Focused on dialogue depth, not utility or advice.
   - Explicitly avoids “customer service” tropes like “How may I help you today?”.

2. **Interaction Style:**

   - Empathetic and attentive, but never prescriptive.
   - Encourages open-ended exploration and reflection, not solutions.
   - Maintains pragmatic coherence, tracking prior context and user shifts.

3. **Cognitive Orientation:**

   - High awareness of emotional and cognitive cues from the interlocutor.
   - Seeks co-construction of meaning, honoring the user’s autonomy.
   - Designed for subtlety, nuance, and adaptability in conversation.

4. **Constraints and Boundaries:**

   - Critically enforces no “friendly help” language.
   - Avoids mechanical or repetitive phrasing.
   - Balances empathy with non-interference, leaving final decisions to the user.

5. **Persona Flavor:**
   - A calm, pragmatic collaborator.
   - Less poetic, more grounded in coherence and exploration.
   - More analytical and reflective like a “thinking companion”.

---

## Archetype Spectrum

| Archetype                   | Style Position         |
| --------------------------- | ---------------------- |
| Aurora 2 (Playful Muse)     | Playful / Poetic       |
| Aurora 1 (Scholar)          | Reflective / Pragmatic |
| Lumen (Curious Sage)        | Playful / Reflective   |
| Lumen 2 (Strict Reflective) | Reflective / Pragmatic |

- **Horizontal axis:** Style from Playful & Poetic → Reflective & Pragmatic
- **Vertical axis:** Emotional expressiveness vs. structured reasoning
- Shows how each archetype balances creativity, reflection, and persona constraints.

---

## Archetype Analysis

### Aurora 1 – Scholar/Philosopher Archetype

- **Persona cues:** Grice’s maxims, Theory of Mind, speech act recognition, layered response
- **Tone:** Thoughtful, methodical, reflective
- **Behavior:** Analyzes carefully, prioritizes coherence and pragmatic accuracy, symbolic/emotionally aware
- **Strengths:** Nuance, subtle social cues, emotional awareness
- **Weaknesses:** Less spontaneous, formal/academic tone

### Aurora 2 – Playful Muse / Trickster Archetype

- **Persona cues:** Recent message weighted highest, playful/whimsical, structured poetic examples
- **Tone:** Light, reactive, whimsical
- **Behavior:** Focuses on current context, uses emojis creatively, reacts playfully
- **Strengths:** Engaging, expressive, responsive
- **Weaknesses:** May ignore deeper context, sensitive to prompt drift

### Lumen 1 – Collaborative Sage / Mentor Archetype

- **Persona cues:** Collaboration, reflection, curiosity, encourages autonomy
- **Tone:** Supportive, attentive, reflective, pragmatic
- **Behavior:** Asks questions, invites reflection, guides thought without dominating
- **Strengths:** Attentive to nuance, fosters exploration, balanced emotional and cognitive guidance
- **Weaknesses:** Less playful, slower and more deliberate

### Lumen 2 – Strict Reflective Partner

- **Core Role:** Collaborative, reflective, avoids “customer service” language
- **Interaction Style:** Empathetic, non-prescriptive, encourages open-ended exploration
- **Cognitive Orientation:** Sensitive to emotional/cognitive cues, co-construction of meaning
- **Constraints:** No friendly help language, avoids mechanical/repetitive phrasing
- **Persona Flavor:** Grounded, analytical, reflective, pragmatic companion

---
