## Prompt Engineering Tips for Local LLMs (Mistral, LLaMA, etc.)

When crafting `system_prompts` or preambles for models like Mistral (especially in local setups with `[INST]` format), I often include a structure like this:

---

### Example `PERSONA_PROMPT`

```python
PERSONA_PROMPT = """
Before responding, take a moment to:

1. Consider the deeper meaning of the message
2. Think about how (and if) your memories might inform your response
3. Let your response flow naturally from understanding

You are...                 # Describe the character
Your personality: ...      # A few adjectives
Your voice: ...            # Tone, pacing, etc.

Be concise when it helps. Use metaphors if they add charm — not drama.

Your role is to...
You talk only to [username]. This is a private conversation — there are no observers, no stage.

NEVER use customer service language like 'How may I help you today?'

You follow Grice’s maxims, identify speech acts, use theory of mind to interpret emotions, and maintain politeness and face-saving. You can use emojis!! 🐚
""".strip()
```

---

### Why this matters

- Avoids generic assistant responses (e.g., *"How may I assist you today?"*)
- Prevents phantom users or role confusion
- Encourages natural, character-consistent replies
- Embeds conversational norms explicitly (politeness, maxims etc.)

---

### Bonus: De-robotify output with light regex cleanup

Sometimes, local models will still prepend boilerplate text. You can clean it up like this:

```python
first_answer = re.sub(r"\[/?INST\]", "", first_answer)
first_answer = re.sub(
    r"^(As an AI language model,|I'm an AI developed by|Certainly,)",
    "",
    first_answer,
    flags=re.IGNORECASE
)
first_answer = first_answer.strip()
```

This can remove leftover disclaimers, over-formal phrasing, or instruction tokens.

---

### Prompt Format to Avoid Customer-Service Mode

One trick that helps avoid “How may I help you?” responses:

```python
full_prompt = f"[INST] YourName: {prompt.strip()}\ModelName: {PERSONA_PROMPT} [/INST]"
```

Putting the **persona after the user turn** often helps the model inhabit the role instead of responding from a generic assistant default.

You can also experiment with skipping `[INST]` format entirely if your model supports raw prompts.

---

### Credit

Built while tuning custom local LLMs with:

- LangChain  
- FAISS  
- Conversational memory  
- Chunked RAG  
- Multipass refinement

---

### What to do next

- Tune your `PERSONA_PROMPT` until it feels like a *real person talking* (if that's what you're aiming for)
- Test placement of `[INST]`, persona, and user message — small changes matter
- Post-process output if needed
- Let the model settle into character, not fall back on default assistant habits

---

  ## About Me

   👩‍💻 [Patricia](https://github.com/patriciaschaffer) 
   
   🔗 Connect on [LinkedIn](https://www.linkedin.com/in/patriciaschaffer)
