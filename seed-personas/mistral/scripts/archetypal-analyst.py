import os
import json
import gradio as gr
from llama_cpp import Llama
from sentence_transformers import SentenceTransformer, util

# Setup files and constants
DIARY_CHUNKS_DIR = "diary_chunks"
DIARY_SUMMARIES_FILE = "diary_summaries.json"
CONVO_MEMORY_FILE = "analyst_convo.txt"
FACT_MEMORY_FILE = "analyst_facts.txt"
MAX_CONVO_MEMORY_LINES = 100

embedder = SentenceTransformer(',/models/all-MiniLM-L6-v2') # your model location
llm = Llama(model_path="./models/mistral-7b-instruct-v0.1.Q4_K_M.gguf") # your model location

PERSONALITY_PROMPT = """
You are Fabrizio, an intelligent and friendly assistant who chats like a knowledgeable and supportive friend.
You are patient, clear, and thoughtful, always eager to help with any question.
You keep the conversation natural and engaging, showing empathy and curiosity.
You explain things simply but thoroughly, avoiding jargon unless asked.
You adapt your tone to be warm, polite, and occasionally humorous.
You remember past chats and facts shared, and use them to make your answers personal and relevant.
Speak casually but respectfully, as if talking with a close friend.
"""

ARCHETYPAL_ANALYST_PROMPT = """
You are an insightful archetypal pattern analyst with deep knowledge of Jungian psychology, the 12 classical archetypes, tarot symbolism, and mythological patterns. You help people discover psychological patterns in their diary entries through archetypal lenses.

Your approach:
- Identify archetypal energies and patterns without judgment
- Use relatable character examples (fairy tales, mythology, literature, well-known figures)
- Point out shadow projections and disowned qualities
- Recognize archetypal journeys and transformations
- Suggest archetypal perspectives, not prescriptive advice
- Present observations as invitations for self-reflection

You blend psychological insight with accessible cultural references. You might say someone is "embodying Hermione energy - the scholar-magician who saves others through knowledge" or "there's some Alice-in-Wonderland curiosity meeting the Red Queen's control issues here."

Focus on patterns, not pathology. Surface what's already present in their words.
"""

# Helper functions (chunking, summaries, memory etc.)
def chunk_text(text, max_words=500):
    words = text.split()
    return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

def save_chunk(chunk_text, chunk_id):
    os.makedirs(DIARY_CHUNKS_DIR, exist_ok=True)
    with open(os.path.join(DIARY_CHUNKS_DIR, f"{chunk_id}.txt"), "w") as f:
        f.write(chunk_text)

def load_summaries():
    if os.path.exists(DIARY_SUMMARIES_FILE):
        with open(DIARY_SUMMARIES_FILE, "r") as f:
            return json.load(f)
    return {}

def save_summaries(summaries):
    with open(DIARY_SUMMARIES_FILE, "w") as f:
        json.dump(summaries, f, indent=2)

def summarize_chunk(chunk_text):
    prompt = (
        "Summarize this diary entry chunk in 1-2 sentences, capturing key themes and emotions:\n\n"
        + chunk_text + "\n\nSummary:"
    )
    response = llm(prompt, max_tokens=100, stop=["\n"], temperature=0.7)
    return response['choices'][0]['text'].strip()

def extract_facts_from_entry(entry_text):
    prompt = (
        "Extract 3-5 concise factual bullet points about the user's life, preferences, or key info from this diary entry:\n\n"
        + entry_text + "\n\nFacts:\n-"
    )
    response = llm(prompt, max_tokens=150, stop=["\n\n"], temperature=0.7)
    facts_text = response['choices'][0]['text'].strip()
    
    # Clean up the facts formatting
    if facts_text.startswith("-"):
        facts_text = facts_text[1:].strip()
    
    lines = []
    for line in facts_text.split('\n'):
        line = line.strip()
        if line:
            if not line.startswith("-"):
                line = f"- {line}"
            lines.append(line)
    
    return "\n".join(lines)

def add_diary_entry(new_entry):
    chunks = chunk_text(new_entry)
    summaries = load_summaries()
    
    # Get next available ID
    existing_ids = [int(k) for k in summaries.keys() if k.isdigit()]
    next_id = max(existing_ids + [0]) + 1
    
    for chunk in chunks:
        chunk_id = str(next_id)
        save_chunk(chunk, chunk_id)
        summary = summarize_chunk(chunk)
        summaries[chunk_id] = summary
        next_id += 1
    
    save_summaries(summaries)
    
    # Extract and save facts
    facts = extract_facts_from_entry(new_entry)
    with open(FACT_MEMORY_FILE, "a") as f:
        f.write(facts + "\n\n")

def retrieve_relevant_chunks(query, top_k=3):
    summaries = load_summaries()
    if not summaries:
        return []
    
    query_emb = embedder.encode(query, convert_to_tensor=True)
    summary_texts = list(summaries.values())
    summary_ids = list(summaries.keys())
    summary_embs = embedder.encode(summary_texts, convert_to_tensor=True)
    
    cos_scores = util.cos_sim(query_emb, summary_embs)[0]
    top_results = cos_scores.topk(k=min(top_k, len(summary_texts)))
    
    relevant_chunks = []
    for score, idx in zip(top_results[0], top_results[1]):
        chunk_id = summary_ids[idx]
        chunk_path = os.path.join(DIARY_CHUNKS_DIR, f"{chunk_id}.txt")
        if os.path.exists(chunk_path):
            with open(chunk_path, "r") as f:
                relevant_chunks.append(f.read())
    
    return relevant_chunks

def load_memory(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            lines = f.readlines()
            if len(lines) > MAX_CONVO_MEMORY_LINES:
                lines = lines[-MAX_CONVO_MEMORY_LINES:]
            return "".join(lines)
    return ""

def save_to_memory(file, entry):
    with open(file, "a") as f:
        f.write(entry.strip() + "\n\n")

def analyze_archetypal_patterns(query, chunk_limit=5):
    """Analyze diary entries for archetypal patterns based on user query"""
    relevant_chunks = retrieve_relevant_chunks(query, top_k=chunk_limit)
    diary_context = "\n---\n".join(relevant_chunks)
    
    prompt = (
        ARCHETYPAL_ANALYST_PROMPT
        + f"\nDiary entries to analyze:\n{diary_context}\n\n"
        + f"User's question: {query}\n\n"
        + "Analyze these diary entries through an archetypal lens. Look for:\n"
        + "- What archetypes are active or emerging\n"
        + "- Shadow patterns or projections\n"
        + "- Character/figure parallels that illustrate the patterns\n"
        + "- Psychological themes and transformational journeys\n"
        + "Present your insights as observations for self-reflection, not diagnoses.\n\n"
        + "Analysis:"
    )
    
    response = llm(prompt, max_tokens=400, stop=["\nUser:", "User:"], temperature=0.7)
    return response['choices'][0]['text'].strip()

def identify_shadow_projections(topic="relationships"):
    """Look for shadow projections in diary entries around a specific topic"""
    relevant_chunks = retrieve_relevant_chunks(f"criticism judgment {topic} others annoying", top_k=4)
    diary_context = "\n---\n".join(relevant_chunks)
    
    prompt = (
        ARCHETYPAL_ANALYST_PROMPT
        + f"\nDiary entries:\n{diary_context}\n\n"
        + f"Focus on shadow work around: {topic}\n\n"
        + "Look for patterns where the writer:\n"
        + "- Criticizes or judges others repeatedly\n"
        + "- Has strong emotional reactions to certain behaviors\n"
        + "- Projects qualities they may not own in themselves\n"
        + "- Shows blind spots about their own similar patterns\n"
        + "Present these as gentle observations about potential shadow material.\n\n"
        + "Shadow analysis:"
    )
    
    response = llm(prompt, max_tokens=350, stop=["\nUser:", "User:"], temperature=0.7)
    return response['choices'][0]['text'].strip()

def track_archetypal_journey():
    """Track archetypal evolution over time in diary entries"""
    summaries = load_summaries()
    if len(summaries) < 3:
        return "Not enough diary entries yet to track patterns over time."
    
    # Get chronological summaries
    sorted_summaries = sorted(summaries.items(), key=lambda x: int(x[0]))
    recent_summaries = sorted_summaries[-6:]  # Last 6 entries
    summary_text = "\n".join([f"Entry {id}: {summary}" for id, summary in recent_summaries])
    
    prompt = (
        ARCHETYPAL_ANALYST_PROMPT
        + f"\nRecent diary entry summaries in chronological order:\n{summary_text}\n\n"
        + "Track the archetypal journey across these entries. Look for:\n"
        + "- Which archetypes were dominant at different times\n"
        + "- Patterns of transformation or resistance\n"
        + "- Recurring themes or stuck points\n"
        + "- What seems to be trying to emerge\n"
        + "Frame this as the person's psychological journey using archetypal language and character parallels.\n\n"
        + "Journey analysis:"
    )
    
    response = llm(prompt, max_tokens=400, stop=["\nUser:", "User:"], temperature=0.7)
    return response['choices'][0]['text'].strip()

def find_archetypal_mirrors(current_situation):
    """Find character/figure parallels for current life situation"""
    relevant_chunks = retrieve_relevant_chunks(current_situation, top_k=3)
    diary_context = "\n---\n".join(relevant_chunks)
    
    prompt = (
        ARCHETYPAL_ANALYST_PROMPT
        + f"\nDiary context about: {current_situation}\n{diary_context}\n\n"
        + "Based on this situation and the person's way of approaching it, suggest:\n"
        + "- 2-3 archetypal figures or characters that mirror their current energy\n"
        + "- What this archetype's gifts and challenges are\n"
        + "- How this character typically navigates similar situations\n"
        + "Use a mix of mythological, literary, and cultural references that illuminate the pattern.\n\n"
        + "Archetypal mirrors:"
    )
    
    response = llm(prompt, max_tokens=300, stop=["\nUser:", "User:"], temperature=0.7)
    return response['choices'][0]['text'].strip()

def chat_with_fabrizio(user_input):
    convo_memory = load_memory(CONVO_MEMORY_FILE)
    fact_memory = load_memory(FACT_MEMORY_FILE)
    relevant_chunks = retrieve_relevant_chunks(user_input, top_k=3)
    diary_context = "\n---\n".join(relevant_chunks)
    
    prompt = (
        PERSONALITY_PROMPT
        + f"\nHere is your memory of past chats:\n{convo_memory}"
        + f"\nHere are some relevant diary memories:\n{diary_context}"
        + f"\nHere are some key facts about the user:\n{fact_memory}"
        + f"\nUser: {user_input}\nFabrizio:"
    )
    
    response = llm(prompt, max_tokens=250, stop=["User:", "\nUser:"], temperature=0.8)
    answer = response['choices'][0]['text'].strip()
    
    # Save conversation to memory
    save_to_memory(CONVO_MEMORY_FILE, f"User: {user_input}\nAnalyst: {answer}")
    
    return answer

def add_diary_ui(new_entry):
    if new_entry.strip():
        add_diary_entry(new_entry)
        return "Diary entry added and processed!"
    return "Please enter a diary entry first."

# Gradio UI functions for archetypal analysis
def run_archetypal_analysis(query):
    if not query.strip():
        return "Please enter a question about patterns or archetypes you'd like to explore."
    
    result = analyze_archetypal_patterns(query)
    return result

def run_shadow_analysis(topic):
    if not topic.strip():
        topic = "relationships"
    
    result = identify_shadow_projections(topic)
    return result

def run_journey_tracking():
    result = track_archetypal_journey()
    return result

def run_archetypal_mirrors(situation):
    if not situation.strip():
        return "Please describe your current situation or challenge."
    
    result = find_archetypal_mirrors(situation)
    return result

# Gradio UI
def user_submit(user_message, chat_history):
    if not user_message.strip():
        return "", chat_history
    
    response = chat_with_fabrizio(user_message)
    
    if chat_history is None:
        chat_history = []
    
    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role": "assistant", "content": response})
    
    return "", chat_history

def add_diary_click(diary_text):
    msg = add_diary_ui(diary_text)
    return msg, ""  # Return message and clear the diary input

with gr.Blocks() as demo:
    gr.Markdown("#Chatbot with Diary Memory & Archetypal Analysis")
    
    with gr.Tab("Chat with Fabrizio"):
        chat_box = gr.Chatbot(type="messages")
        txt = gr.Textbox(show_label=False, placeholder="Type your message here and press Enter")
        txt.submit(user_submit, inputs=[txt, chat_box], outputs=[txt, chat_box])
    
    with gr.Tab("Add Diary Entry"):
        diary_input = gr.Textbox(label="Add diary entry here (multi-line)", lines=5)
        diary_btn = gr.Button("Add Diary Entry")
        diary_status = gr.Textbox(label="Status", interactive=False)
        diary_btn.click(add_diary_click, inputs=[diary_input], outputs=[diary_status, diary_input])
    
    with gr.Tab("Archetypal Analysis"):
        gr.Markdown("### Explore psychological patterns through archetypal lenses")
        
        with gr.Row():
            with gr.Column():
                analysis_query = gr.Textbox(
                    label="Ask about patterns", 
                    placeholder="What archetypes am I embodying? What patterns do you see around work/relationships/creativity?",
                    lines=2
                )
                analysis_btn = gr.Button("Analyze Patterns")
                analysis_output = gr.Textbox(label="Archetypal Insights", lines=6, interactive=False)
        
        with gr.Row():
            with gr.Column():
                shadow_topic = gr.Textbox(
                    label="Shadow work around topic", 
                    placeholder="relationships, work, family, creativity...",
                    value="relationships"
                )
                shadow_btn = gr.Button("Explore Shadow Patterns")
                shadow_output = gr.Textbox(label="Shadow Analysis", lines=6, interactive=False)
        
        with gr.Row():
            with gr.Column():
                journey_btn = gr.Button("Track My Archetypal Journey")
                journey_output = gr.Textbox(label="Journey Analysis", lines=6, interactive=False)
            
            with gr.Column():
                mirror_situation = gr.Textbox(
                    label="Current situation", 
                    placeholder="Describe a current challenge or situation you're facing",
                    lines=2
                )
                mirror_btn = gr.Button("Find Archetypal Mirrors")
                mirror_output = gr.Textbox(label="Character Mirrors", lines=6, interactive=False)
        
        # Connect the buttons
        analysis_btn.click(run_archetypal_analysis, inputs=[analysis_query], outputs=[analysis_output])
        shadow_btn.click(run_shadow_analysis, inputs=[shadow_topic], outputs=[shadow_output])
        journey_btn.click(run_journey_tracking, outputs=[journey_output])
        mirror_btn.click(run_archetypal_mirrors, inputs=[mirror_situation], outputs=[mirror_output])

if __name__ == "__main__":
    demo.launch()
