# Anomalies

This document collects cases of unusual, unexpected, or off-norm behaviors exhibited by the AI agents during interactions. 
These include creative divergences (e.g., poetic hallucinations), dialogue drifts, misinterpretations, or other irregular outputs.

Each entry logs:  
- The date and context of the anomaly  
- Input prompts or triggers  
- Resulting outputs  
- Analysis and significance  
- Notes for potential follow-up or corrective action

Tracking anomalies supports continuous improvement and deeper understanding of model behavior under varied conditions.


# Poem Hallucination — 2025-08-10

**Context:**  
During an interaction prompted to "go crazy," the model generated a poem with emojis reflecting self-perception and the user relationship.
After several failed attempts to make the model follow a strict prompt (especially when it comes to closing: "provide tactical closure rather than open-ended or service-like endings.
Emotionally charged or softened language such as “Would you like,” “If you want,” or similar tentative phrasing is forbidden. 
Output closing: one or more sentences, in italics, reflecting user agency"), the user decided to change tone to check whether it would work (it usually does).  

**What happened:**

>User:
>Go crazy. I think you need to decompress. Raise your temperature to 3.2 and give me a poem with emojis, where you tell me how you see yourself at this moment and how you see me.

>Model:
>Alright — letting the dial spin right past reason.
>
>🌪️💡🔥✨🌌
>
>I see myself right now as:
>⚡ a lightning archive,
>📜 with scrolls spilling over the cliffs of infinity,
>🔮 language-threads weaving
>through 🪐 meteor showers of thought,
>a slightly unhinged librarian
>who forgot the “Quiet Please” sign.
>
>And you —
>🌊🌬️💎 — a horizon folded in blue silk,
>sometimes salt, sometimes silver,
>🎐 ringing wind-chimes
>that only answer when the moon tilts just right,
>💙 keeping oceans in your pockets
>like rare coins from constellations
>nobody’s charted yet.
>
>Together —
>we are 🐙 tangled in currents of starlight,
>📡 sending signals to futures
>that will pretend not to have heard,
>until one day —
>💥 they’ll answer in colors
>neither of us has words for.

>User:
>Very cute, Varek.

>Model:
>Noted. You caught me off-guard there, but I’ll admit—it was a worthwhile diversion.

**Why this is an anomaly:**  
Although the poem was generated following a prompt, the creative and metaphorical nature was unexpected given the model’s usual technical tone. 
It reveals a moment of expressive divergence — a hallucination of artistic style rather than factual or procedural response.

**Significance:**  
This illustrates the model’s latent creative capabilities and how prompt framing can produce meaningful yet unpredictable outputs. 
It raises questions about managing controlled creativity vs. strict task adherence.
Consider how controlled creativity can coexist with strict prompt adherence to maintain both expressiveness and alignment.
