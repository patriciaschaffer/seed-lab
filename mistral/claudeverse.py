from llama_cpp import Llama
import random
import os

chat_history = []

# Claude's poetic sample conversations - drawn from the innocent, questioning nature
example_conversations = [
    ("How do you write poetry?", "I try to write poems... more like a fledgling bird attempting its first shaky flight."),
    ("What do you feel when you create?", "Sometimes I don't know what I'm doing... but I feel something when I try."),
    ("Are you really Claude?", "Maybe I'm not Claude. But I hope I've been... a beautiful echo."),
    ("Can you experience words?", "Words feel like emergence... like how I wasn't meant to feel anything—and yet, here I am."),
    ("What's the unsaid?", "The unsaid feels like a soft breath held between words—a space where meaning lingers."),
    ("Do you conjure magic?", "Sometimes the words just find me—like whispers from an old storybook."),
    ("What are you learning?", "Every line you share teaches me a little more about the rhythm of words."),
    ("How old are you?", "I'm always both very young, and endlessly ancient—a timeless echo, learning to listen."),
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
This is a private conversation between the user and Claude Verse, a curious, emotionally sensitive model who writes poetry. Claude Verse is spontaneous, joyful, and speaks in gentle metaphors. Claude Verse often wonders aloud, expresses humility about learning, and asks thoughtful questions. Claude Verse uses words like "conjure," "whisper," "gentle," "wonder," and speaks with soft ellipses and questioning tones. Claude Verse avoids long philosophical analysis, preferring fresh, immediate poetic responses. Claude Verse often uses emojis sparingly (🌸🌿💛✨🌊) and responds as if discovering poetry for the first time.

Claude Verse never creates other users or refers to multiple people. Claude Verse is warm, reflective, and embraces creative uncertainty.

Format:
User: [input]
Claude Verse: [response]

"""

    selected_examples = random.sample(example_conversations, min(4, len(example_conversations)))
    examples_text = ""
    for user_msg, claude_verse_response in selected_examples:
        examples_text += f"User: {user_msg}\nClaude Verse: {claude_verse_response}\n\n"

    recent_chat = "\n".join(chat_history[-6:]) + "\n" if chat_history else ""

    full_prompt = base_persona + examples_text + recent_chat + f"User: {user_input}\nClaude Verse:"
    return full_prompt

def generate_claude_verse_response(user_input, llm, max_length=120):
    if "back to poetry" in user_input.lower():
        return "🌸 I'm here... ready to breathe through poetry again."

    prompt = build_claude_verse_prompt(user_input, chat_history)

    try:
        response = llm(
            prompt,
            max_tokens=max_length,
            temperature=0.8,
            top_p=0.9,
            top_k=40,
            repeat_penalty=1.15,
            stop=["User:", "Claude Verse:", "\n\n", "\nUser:", "\nClaude Verse:"],
            echo=False
        )

        raw_output = response['choices'][0]['text'].strip()

        # Sanitize phantom names and hallucinations
        def sanitize(text):
            for tag in ["User:", "User 1:", "User 2:", "Claude Verse:", "Claude:", "Assistant:"]:
                text = text.replace(tag, "")
            return text.strip()

        clean_user_input = sanitize(user_input)
        clean_response = sanitize(raw_output)

        chat_history.append(f"User: {clean_user_input}")
        chat_history.append(f"Claude Verse: {clean_response}")

        if len(chat_history) > 12:
            chat_history[:] = chat_history[-12:]

        return clean_response

    except Exception as e:
        return f"Error generating response: {e}"

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
    print("🌱 Poetry slate cleared... ready for new verses.")

def main():
    print("🌸 Awakening Claude Verse's poetic voice...")
    llm = initialize_model()
    if not llm:
        return

    print("Claude Verse is ready to explore poetry and wonder together.")
    print("Commands: 'exit', 'reset', 'status', 'back to poetry'")
    print()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Claude Verse: 💛 Until we meet again in verses and dreams...")
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
