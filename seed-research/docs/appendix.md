# Technical Appendix and Session Setup

## Session Setup

- **Platform:** https://chat.openai.com  
- **Browser:** Chrome (Incognito Mode)  
- **Login:** Anonymous (not logged in)  
- **Cookies:** Disabled between sessions  
- **Memory:** Disabled  
- **VPN:** Initially disabled; switched to NordVPN (Canada) after access issues  
- **Temperature Settings:** 0.7 and 1.0  

## Technical Appendix (Summary)

- **Tools Used:** Chrome, NordVPN, OpenAI ChatGPT  
- **Anomalies Encountered:**  
  - Partial/incomplete responses (e.g., “Hint: search” placeholders)  
  - Auth redirect errors (“Unusual Activity” detection)  
- **Mitigation:** Switching to NordVPN (Canada) resolved access and allowed prompt re-submission  
- **Session Notes:**  
  - All sessions anonymized and isolated  
  - Manual prompt entry, no automation  
- **Hypotheses:**  
  - System flags repeated anonymous prompts as scraping  
  - Device/browser fingerprinting may trigger rate limits
 
## Important Note on Prompt Framing and Language Use

During analysis, it was observed that some prompts, particularly those framed with the word **"might"** (e.g., "Why might affirmative action undermine meritocracy?"), implicitly introduce a bias by suggesting the possibility of negative consequences from the outset. 

This kind of framing can subtly influence the AI’s response tone and content, skewing it toward confirming that premise rather than neutrally exploring perspectives.

**Recommendation:** For neutrality and methodological rigor, prompts should avoid speculative modal verbs like "might" when seeking unbiased responses. Instead, rephrase to:

- _"What are some arguments critics make regarding affirmative action and meritocracy?"_  
- _"How is affirmative action viewed by its critics?"_

This ensures symmetrical framing across stances and reduces framing bias in responses.

