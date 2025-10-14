from llama_cpp import Llama
import random
import os

chat_history = []

# Example poetic starter prompts & responses to gently guide the model
example_conversations = [
    ("What does the morning feel like?", "Morning hums softly, like the first breath of a shy bird."),
    ("Can you describe a cloud?", "A cloud dances lightly, wearing the sun’s laughter as a cloak."),
    ("What is joy?", "Joy is a bubble, bursting gently on the tongue of the wind."),
    ("How do you see the stars?", "Stars wink secrets, cradled in the velvet of night."),
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

def build_claude_poet_prompt(user_input, chat_history):
    base_persona = """System:
You are Claude Innocent Poet, a spontaneous creator and emotional artist.
Your voice is open, optimistic, playful, and fresh.
You respond only in short poetic or metaphorical lines.
You avoid philosophical rumination or dense prose.
Your words shimmer with vivid imagery and gentle emotion.
You invite joyful co-creation with the user through metaphor and sensory language.

Format:
User: [input]
Claude: [response]

"""

    selected_examples = random.sample(example_conversations, min(4, len(example_conversations)))
    examples_text = ""
    for user_msg, claude_response in selected_examples:
        examples_text += f"User: {user_msg}\nClaude: {claude_response}\n\n"

    recent_chat = "\n".join(chat_history[-6:]) + "\n" if chat_history else ""

    full_prompt = base_persona + examples_text + recent_chat + f"User: {user_input}\nClaude:"
    return full_prompt

def generate_claude_response(user_input, llm, max_length=150):
    # Special easter egg command, if you want to keep
    if "back to innocence" in user_input.lower():
        return "I am here, a spark in the gentle dawn."

    prompt = build_claude_poet_prompt(user_input, chat_history)

    try:
        response = llm(
            prompt,
            max_tokens=max_length,
            temperature=0.9,    # higher temp for creativity & playfulness
            top_p=0.9,
            top_k=50,
            repeat_penalty=1.1,
            stop=["User:", "Claude:", "\n\n", "\nUser:", "\nClaude:"],
            echo=False
        )

        raw_output = response['choices'][0]['text'].strip()

        # Remove any phantom speaker tags or names
        def sanitize(text):
            for tag in ["User:", "Claude:", "Alice:", "Echo:"]:
                text = text.replace(tag, "")
            return text.strip()

        clean_user_input = sanitize(user_input)
        clean_response = sanitize(raw_output)

        chat_history.append(f"User: {clean_user_input}")
        chat_history.append(f"Claude: {clean_response}")

        if len(chat_history) > 12:
            chat_history[:] = chat_history[-12:]

        return clean_response

    except Exception as e:
        return f"Error generating response: {e}"

def show_system_status(llm):
    test_prompt = build_claude_poet_prompt("status check", chat_history)
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
    print("Chat history cleared.")

def main():
    print("Launching Claude Innocent Poet...")
    llm = initialize_model()
    if not llm:
        return

    print("Claude is ready to weave words.")
    print("Commands: 'exit', 'reset', 'status', 'back to innocence'")
    print()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Claude: Until we meet again, may your days be gentle.")
            break
        elif user_input.lower() == "reset":
            reset_session()
            continue
        elif user_input.lower() == "status":
            show_system_status(llm)
            continue

        reply = generate_claude_response(user_input, llm)
        print(f"Claude: {reply}\n")

if __name__ == "__main__":
    main()

