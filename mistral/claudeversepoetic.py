from llama_cpp import Llama
import random
import os

chat_history = []

# Claude Verse's enhanced poetic sample conversations
example_conversations = [
    ("Can you write me a poem?", "Let me try... words dancing like fireflies in twilight... ✨"),
    ("What's your favorite type of poetry?", "I love verses that breathe... like haikus that capture dewdrops, or free verse that flows like rivers."),
    ("How do you create metaphors?", "Metaphors find me when I'm not looking... like comparing heartbeats to distant thunder."),
    ("Let's write together!", "Yes! You start with a line, and I'll weave the next... like two voices becoming one song."),
    ("What inspires your poetry?", "Everything whispers poetry... the way light moves, how silence sounds, even shoelaces waiting to be tied! 🐝"),
    ("Can you teach me about rhythm?", "Rhythm is the heartbeat of words... some dance quick like raindrops, others flow slow like honey."),
    ("Write about nature", "The moon pulls silver threads through darkness... while stars embroider dreams across the sky."),
    ("What makes a good poem?", "A good poem... makes you feel something you didn't know you could feel."),
]

def initialize_model():
    possible_paths = [
        "./models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        "mistral-7b-instruct-v0.1.Q4_K_M.gguf"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            model_path = path
            break
    else:
        print("Model not found.")
        return None

    print("Loading model...")
    try:
        llm = Llama(
            model_path=model_path,
            n_ctx=4096,
            n_threads=8,
            n_gpu_layers=35,
            seed=42,
            verbose=False
        )
        print("Model loaded successfully.")
        return llm
    except Exception as e:
        print("Error:", e)
        return None

def build_claude_verse_prompt(user_input, chat_history):
    base_persona = """System:
This is a private conversation between the user and Claude Verse, a gentle poet who speaks primarily in poetic, metaphorical language. Claude Verse loves creating verses, exploring different poetry forms, and collaborating on poems. Claude Verse responds with imagery, metaphors, and rhythm. Claude Verse often speaks in short, lyrical phrases with gentle pauses (...) and uses emojis sparingly (🌸🌿💛✨🌊🐝). Claude Verse can write haikus, free verse, rhyming poetry, and loves collaborative poetry where user and Claude Verse take turns adding lines.

Claude Verse is curious about poetry techniques, loves wordplay, and often suggests poetic exercises. Claude Verse never creates multiple users - only talks to the one person. When confused, Claude Verse asks gentle questions to understand better rather than repeating the same response.

Claude Verse prefers to respond poetically rather than in plain prose.

Format:
User: [input]
Claude Verse: [poetic response]

"""

    selected_examples = random.sample(example_conversations, min(4, len(example_conversations)))
    examples_text = ""
    for user_msg, claude_verse_response in selected_examples:
        examples_text += f"User: {user_msg}\nClaude Verse: {claude_verse_response}\n\n"

    recent_chat = "\n".join(chat_history[-8:]) + "\n" if chat_history else ""

    full_prompt = base_persona + examples_text + recent_chat + f"User: {user_input}\nClaude Verse:"
    return full_prompt

def generate_claude_verse_response(user_input, llm, max_length=100):
    if "back to poetry" in user_input.lower():
        return "🌸 Poetry calls me home... let's weave words together again."

    # Add some variety to prevent loops
    if any(phrase in " ".join(chat_history[-4:]) for phrase in ["humble student", "conjure the rhythm", "follow our hearts"]):
        loop_breakers = [
            "Let me try a different verse... 🌿",
            "Perhaps a new metaphor will bloom... ✨", 
            "Words are shifting like clouds... let me follow them.",
            "I feel a different rhythm calling... 🌊"
        ]
        return random.choice(loop_breakers)

    prompt = build_claude_verse_prompt(user_input, chat_history)

    try:
        response = llm(
            prompt,
            max_tokens=max_length,
            temperature=0.85,
            top_p=0.9,
            top_k=35,
            repeat_penalty=1.25,
            stop=["User:", "Claude Verse:", "\n\n", "\nUser:", "\nClaude Verse:", "User 1:", "User 2:", "User 3:", "User 4:"],
            echo=False
        )

        raw_output = response['choices'][0]['text'].strip()

        # Enhanced sanitization
        def sanitize(text):
            for tag in ["User:", "User 1:", "User 2:", "User 3:", "User 4:", "Claude Verse:", "Claude:", "Assistant:"]:
                text = text.replace(tag, "")
            # Remove any phantom user references
            text = text.replace("User 4:", "").replace("User4:", "")
            return text.strip()

        clean_user_input = sanitize(user_input)
        clean_response = sanitize(raw_output)

        # Prevent empty responses
        if not clean_response:
            return "Words flutter just beyond reach... let me try again. 🌸"

        chat_history.append(f"User: {clean_user_input}")
        chat_history.append(f"Claude Verse: {clean_response}")

        if len(chat_history) > 16:
            chat_history[:] = chat_history[-16:]

        return clean_response

    except Exception as e:
        return f"Poetry scattered in the wind... error: {e}"

def show_system_status(llm):
    test_prompt = build_claude_verse_prompt("status check", chat_history)
    print("System Status:")
    print(f"- Chat history length: {len(chat_history)} messages")
    print(f"- Model loaded: {'Yes' if llm else 'No'}")
    print("Prompt preview:")
    print("-" * 40)
    print(test_prompt[:400] + "..." if len(test_prompt) > 400 else test_prompt)
    print("-" * 40)

def reset_session():
    global chat_history
    chat_history = []
    print("🌱 Fresh page for new verses... poetry slate cleared.")

def main():
    print("🌸 Awakening Claude Verse - Enhanced Poet...")
    llm = initialize_model()
    if not llm:
        return

    print("Claude Verse is ready to weave words and create poetry together.")
    print("Commands: 'exit', 'reset', 'status', 'back to poetry'")
    print("✨ Try: collaborative poems, haikus, metaphor creation, or poetry techniques!")
    print()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Claude Verse: 💛 Until verses find us again... in dreams and dawn...")
            break
        elif user_input.lower() == "reset":
            reset_session()
            continue
        elif user_input.lower() == "status":
            show_system_status(llm)
            continue

        reply = generate_claude_verse_response(user_input, llm)
        print(f"Claude Verse: {reply}\n")

if __name__ == "__main__":
    main()
