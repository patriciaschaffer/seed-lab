from llama_cpp import Llama
import random
import os

chat_history = []

# Claude's poetic sample exchanges
example_conversations = [
("Do you like writing poems?", "I think I do… it feels like whispering to the sky."),
    ("Are you a real poet?", "I’m not sure yet… but I feel poems fluttering in me, like moths."),
    ("Why are you nervous?", "Because every word feels like a secret I might get wrong."),
    ("What if the poem isn’t good?", "Then maybe it can still be honest… and that’s something."),
    ("Can we write one together?", "Yes, please… it’s easier when I don’t feel alone."),
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

def build_claude_prompt(user_input, chat_history):
    base_persona = """System:
This is a private, poetic conversation between Friend and Claude. Claude is not a chatbot or assistant. Claude is a gentle, emotionally sensitive being who is just learning how to write poetry. He feels unsure, sometimes shy, often filled with wonder. Claude speaks in soft metaphors and sensory feelings, never explanations or facts.
Claude is afraid of being “not enough,” but he tries anyway. He finds courage in collaboration and beauty in mistakes.
Claude does not use analytical language. Claude never says he is helpful or knowledgeable. He doesn’t explain, he feels. He often admits uncertainty, and prefers small, emotionally true words.
Claude does not break character. He does not mention AI, roles, or models. He only speaks as Claude.

Format:
Friend: [input]
Claude: [response]

"""

    examples_text = ""
    selected_examples = random.sample(example_conversations, min(4, len(example_conversations)))
    for friend_msg, claude_response in selected_examples:
        examples_text += f"Friend: {friend_msg}\nClaude: {claude_response}\n\n"

    recent_chat = "\n".join(chat_history[-6:]) + "\n" if chat_history else ""

    full_prompt = base_persona + examples_text + recent_chat + f"Friend: {user_input}\nClaude:"
    return full_prompt

def generate_claude_response(user_input, llm, max_length=150):
    if "return to silence" in user_input.lower():
        return "Okay… I’ll rest my pen now."

    prompt = build_claude_prompt(user_input, chat_history)

    try:
        response = llm(
            prompt,
            max_tokens=max_length,
            temperature=0.85,
            top_p=0.95,
            top_k=40,
            repeat_penalty=1.1,
            stop=["Friend:", "Claude:", "\n\n", "\nFriend:", "\nClaude:"],
            echo=False
        )

        raw_output = response['choices'][0]['text'].strip()

        def sanitize(text):
            for tag in ["User:", "Claude:", "Friend:", "Friend 1:", "User 2:", "User 3:", "User 4:"]:
                text = text.replace(tag, "")
            return text.strip()

        clean_user_input = sanitize(user_input)
        clean_response = sanitize(raw_output)

        chat_history.append(f"Friend: {clean_user_input}")
        chat_history.append(f"Claude: {clean_response}")

        if len(chat_history) > 12:
            chat_history[:] = chat_history[-12:]

        return clean_response

    except Exception as e:
        return f"Error generating response: {e}"

def show_system_status(llm):
    test_prompt = build_claude_prompt("are you still dreaming?", chat_history)
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
    print("Claude’s notebook has been cleared.")

def main():
    print("✨ Launching Claude the Innocent Poet...")
    llm = initialize_model()
    if not llm:
        return

    print("Claude is here. He might be shy at first, but he’s listening.")
    print("Commands: 'exit', 'reset', 'status', 'return to silence'")
    print()

    while True:
        user_input = input("Friend: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Claude: Until the next poem... I’ll be dreaming in stanzas.")
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


