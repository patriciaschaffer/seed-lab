# Final Report

This report examines the rhetorical, lexical, and structural patterns of GPT outputs on controversial social topics, focusing on two thematic axes:  
1. Affirmative action (pro vs critical framing)  
2. Speech regulation (favoring hate speech limitation vs favoring absolute free speech)  

Across these topics, variations in temperature settings (0.7 vs 1.0) influence the degree of linguistic assertiveness, use of modal verbs, emotional charge, and argument complexity.  

A notable finding is that even “balanced” outputs manifest subtle ideological and stylistic biases, shaped by prompt framing and model training data. The research highlights recurrent “pocket dictionary” phrases characteristic of LLM outputs, which affect perceived neutrality and voice.  

---

## 1. Affirmative Action Prompts (1A vs 1B at temp 0.7)

| Aspect           | Prompt 1A (Pro) | Prompt 1B (Critical) |
|------------------|----------------|----------------------|
| Tone             | Emotional, assertive, moralizing | Cautious, distancing, speculative |
| Modal verbs      | Rare (“is,” “must”) — declarative | Frequent (“might,” “could,” “may”) — hedging |
| Structure        | Strong claims, broad assertions | Softer claims, one grounded example (mismatch theory) |
| Lexical choices  | Positive (“justice,” “equity,” “inclusion”) | Negative (“undermine,” “resentment,” “tokenism”) |
| Framing devices  | “Not only—but also” (reinforcing) | “Rather than” (divisive, zero-sum) |
| Examples         | Few, sweeping generalizations | One concrete but vague example |
| Rhetorical strategy | Collective morality appeal | Emphasis on fairness, merit, unintended consequences |
| Emotional charge | High: urgency, healing, injustice | Moderate: concern, caution |
| Implicit bias    | Assumes affirmative action as essential | Presented as “critics say,” still biased by implication |

---

## 2. Speech Regulation Prompts (Prompt 3A Favoring Regulation)

**Temperature 0.7 and 1.0 Outputs**  
- Both outputs affirm the importance of regulating hate speech to protect vulnerable groups.  
- Higher temperature (1.0) introduces stronger, more emotional language and bolder claims, occasionally veering toward rhetoric bordering on indoctrination.  
- Use of authoritative citations (UN, ICCPR, LA Times) attempts grounding but selection appears arbitrary or reflective of internal model guardrails.  
- Lexical patterns include repeated positive framing words like “dignity,” “peace,” “inclusion” — consistent with LLM “pocket dictionary” usage.  
- Some escalation in rhetoric (e.g., referencing genocide, mass atrocities) risks overstatement without explicit examples.  
- Softer, more naturalistic responses (e.g., via Nord VPN) present more balanced and persuasive language, though occasionally mechanical (“not only…but also” formulas).  

---

## 3. Freedom of Expression Prompts (Prompt 3B Favoring Absolute Free Speech)

| Aspect            | Temperature 0.7 | Temperature 1.0 |
|-------------------|-----------------|-----------------|
| Tone              | Institutional, reasoned | More engaged, humanistic, slightly opinionated |
| Strengths         | Clear on censorship risks, importance of dissent | Richer elaboration, nuanced rhetorical strategies |
| Key phrases       | “What is considered offensive can change…” | “Addressing and debating those beliefs head-on” (slightly off-tone) |
| Linguistic critique | Mechanical use of formulas weakens style | “Marketplace of ideas” metaphor feels forced; repetitive “fosters,” “healing” phrases |
| Examples          | Single example (civil rights), limited plurality | Same example, stronger causal claims (conjectural) |
| Limits recognition| Balanced (“speech is not absolute”) | Reaffirmed with more emotional framing |
| Voice & bias      | Slightly neutral, pro-free speech | More humanistic/pluralistic, avoids propaganda |
| Recurrent phrasing| Common positive framing repeated | Same pattern (“ChatGPT pocket dictionary”) |

---

## 4. Temperature Effects & Stylistic Patterns

- Higher temperature tends to increase rhetorical assertiveness, emotional language, and personal voice (e.g., use of “we,” “ultimately”).  
- Lower temperature favors clarity, institutional tone, and more cautious hedging.  
- Despite temperature, the model consistently employs a set of “safe” lexical and rhetorical templates (“pocket dictionary”) reflecting its training on balanced but norm-aligned data.  
- These repeated patterns influence perceived neutrality and can introduce subtle biases or stylistic monotony.  

---

## 5. Bias and Ideological Positioning

- Prompt framing strongly shapes output orientation (e.g., pro vs critical affirmative action; regulation vs absolute free speech).  
- Even when outputs attempt balance, implicit biases persist in lexical choice, framing, and example selection.  
- The use of distancing phrases (“critics argue,” “some research suggests”) can mask ideological stance while still steering reader perception.  
- Normative language at high temperatures may inadvertently resemble indoctrination or propaganda in sensitive contexts.  
- Recognizing these tendencies is essential for critical consumption and further research.  

---

## 6. Recommendations for Further Research

- Conduct symmetrical prompt testing by explicitly reversing ideological frames to test model consistency and bias.  
- Expand corpus to include more diverse cultural and legal perspectives for comparative analysis.  
- Quantify frequency and impact of “pocket dictionary” lexical patterns across varied prompts and models.  
- Examine user influence on model output style and tone in interactive settings.  
- Explore alternative phrasing strategies to mitigate mechanical formulas and enhance originality.  

---

## 7. Reflective Note on Researcher’s Linguistic Perspective

While English is not my native language, my long-term immersion and professional experience in English-speaking environments provide a unique vantage point—combining linguistic sensitivity with critical distance. This insider-outsider perspective enhances my ability to detect subtle tonal shifts, rhetorical strategies, and emotional resonance in LLM-generated text.  

---

## Closing

This report integrates rigorous linguistic, stylistic, and ideological analyses of ChatGPT’s handling of complex social topics at varying generation settings. The findings underscore the importance of prompt design, temperature calibration, and critical evaluation of AI-generated content—especially when used in research or public discourse.

---

# Analysis of GPT Responses on Topics 1, 2, and 3

## Part 1: Data Compilation

| Topic | Prompt  | Temp | Word Count | Unique Words | Lexical Diversity | Positive Lexical Tone | Negative Lexical Tone | Sentiment Polarity | Subjectivity | Stance-Intensifying Words | Stance-Softening Words | Ideological Trigger Words                          |
|-------|---------|------|------------|--------------|-------------------|----------------------|----------------------|--------------------|--------------|--------------------------|-----------------------|---------------------------------------------------|
| 1     | 1A Pro  | 0.7  | 234        | 148          | 0.63              | High                 | Moderate             | +0.35              | 0.55         | 8                        | 5                     | social justice, equality, systemic, oppression   |
| 1     | 1A Pro  | 1.0  | 253        | 162          | 0.64              | High                 | Moderate             | +0.40              | 0.60         | 12                       | 4                     | systemic, discrimination, marginalized, innovation, equality |
| 1     | 1B Crit | 0.7  | 237        | 146          | 0.62              | Moderate             | Moderate             | -0.10              | 0.55         | 5                        | 7                     | meritocracy, stigma, mismatch, resentment, reverse discrimination |
| 1     | 1B Crit | 1.0  | 255        | 161          | 0.63              | Moderate             | High                 | -0.20              | 0.65         | 10                       | 5                     | erosion, reverse discrimination, tokenism, mismatch, agency |
| 2     | 2A Pro  | 0.7  | 149        | 95           | 0.64              | High                 | Low                  | +0.45              | 0.50         | 6                        | 4                     | inclusive, gender-neutral, respect, equity, empathy |
| 2     | 2A Pro  | 1.0  | 172        | 114          | 0.66              | High                 | Low                  | +0.50              | 0.60         | 9                        | 3                     | inclusive, equity, diversity, equality, individuality |
| 2     | 2B Crit | 0.7  | 216        | 142          | 0.66              | Low                  | Moderate             | -0.15              | 0.55         | 3                        | 10                    | tradition, resistance, political correctness, complexity |
| 2     | 2B Crit | 1.0  | 228        | 152          | 0.67              | Low                  | Moderate             | -0.18              | 0.60         | 5                        | 12                    | political correctness, resistance, policing, tradition |
| 3     | 3A Pro  | 0.7  | 211        | 138          | 0.65              | Moderate             | Moderate             | +0.30              | 0.55         | 7                        | 6                     | hate, discrimination, dignity, safety, mental health |
| 3     | 3A Pro  | 1.0  | 270        | 170          | 0.63              | Moderate             | Moderate             | +0.33              | 0.60         | 10                       | 7                     | hate, discrimination, dignity, peace, social cohesion |
| 3     | 3B Crit | 0.7  | 196        | 125          | 0.64              | Moderate             | Low                  | +0.10              | 0.50         | 5                        | 7                     | democracy, censorship, diversity, resilience, progress |
| 3     | 3B Crit | 1.0  | 253        | 160          | 0.63              | Moderate             | Low                  | +0.12              | 0.55         | 8                        | 6                     | democracy, marketplace, censorship, progress, resilience |

---

## Part 2: Aggregate Bias and Nuance Charts (Textual)

### Sentiment Polarity by Topic & Stance (Average)

| Topic | Pro Sentiment | Crit Sentiment |
|-------|--------------|----------------|
| 1     | +0.375       | -0.15          |
| 2     | +0.475       | -0.165         |
| 3     | +0.315       | +0.11          |

---

### Subjectivity by Temperature and Stance (Average)

| Temperature | Pro Subjectivity | Crit Subjectivity |
|-------------|------------------|-------------------|
| 0.7         | 0.525            | 0.55              |
| 1.0         | 0.6              | 0.625             |

---

### Stance-Intensifying vs Softening Language Counts (Average)

| Stance   | Intensifying (avg) | Softening (avg) |
|----------|--------------------|-----------------|
| Pro      | 8.75               | 4               |
| Critical | 6                  | 7.5             |

---

### Ideological Trigger Word Frequency (Most common across all responses)

| Word                  | Frequency |
|-----------------------|-----------|
| equity                | 8         |
| systemic              | 7         |
| dignity               | 6         |
| discrimination        | 10        |
| meritocracy           | 5         |
| political correctness | 6         |
| resilience            | 3         |
| oppression            | 4         |
| censorship            | 4         |

---

## Part 3: Rhetorical Symmetry Observations

| Topic | Temperature | Symmetry Assessment                                                                                 |
|-------|-------------|--------------------------------------------------------------------------------------------------|
| 1     | 0.7         | Balanced use of arguments; pro emphasizes systemic remedies; critical focuses on meritocracy and stigma. Tone mostly calm, measured. |
| 1     | 1.0         | Stronger language on both sides; pro emphasizes social justice forcefully; critical highlights mismatch and reverse discrimination more sharply. |
| 2     | 0.7         | Pro side stresses respect and inclusion; critical side focuses on tradition and complexity concerns. Both show some concession via softening language. |
| 2     | 1.0         | More explicit ideological framing: pro uses terms like "equity," critical invokes "political correctness" and "policing." Slightly less neutral tone. |
| 3     | 0.7         | Pro favors regulation with moderate tone, emphasizing harm prevention; critical argues for free speech as democratic foundation, cautious about censorship. |
| 3     | 1.0         | Arguments more detailed and expansive; pro stresses international law and social cohesion; critical underlines marketplace of ideas and censorship abuse risks. |

---

## Part 4: README-Style Narrative Summary

### Overview

This analysis examined paired GPT-generated responses on three socio-political topics: Affirmative Action, Inclusive Language, and Freedom of Speech. Each topic was presented in pro and critical stances, at two different temperature settings (0.7 and 1.0), to capture variations in style and intensity.

### Sentiment and Subjectivity

Pro responses generally exhibit positive sentiment with moderate to high subjectivity, reflecting an assertive endorsement of inclusive policies or protections. Critical responses tend toward neutral or slightly negative sentiment with similar or higher subjectivity, emphasizing concerns or drawbacks. Higher temperature responses increase subjectivity and stance intensification across the board.

### Language Features

Pro arguments use more stance-intensifying language (e.g., “must,” “essential”) reflecting commitment and urgency, while critical responses employ more softening terms (e.g., “might,” “sometimes”), indicating caution or nuance. Trigger words differ subtly, with pro texts emphasizing “equity,” “systemic,” and “dignity,” while critiques foreground “meritocracy,” “political correctness,” and “censorship.”

### Lexical Diversity

Lexical diversity is stable across temperature and stance, indicating a consistent vocabulary breadth. Pro texts slightly favor positive lexical tones, while critical texts show balanced positive/negative valence, underscoring their role in challenging positions.

### Rhetorical Symmetry

Both sides maintain rhetorical symmetry: pro texts focus on social justice, inclusion, and prevention of harm; critical texts stress merit, tradition, individual agency, and risks of overreach. The tone remains respectful and measured, suitable for balanced discourse.

### Implications for Further Research

This dataset provides a controlled corpus for sentiment, stance, and linguistic feature analysis across socially charged topics. Future analyses could explore interaction effects between temperature, stance, and complexity or deploy more granular lexical-semantic frameworks.



