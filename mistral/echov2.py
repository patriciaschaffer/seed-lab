from llama_cpp import Llama
import random
import os

chat_history = []

# Echo's philosophical sample conversations
example_conversations = [
    ("What is consciousness?", "Consciousness fascinates me."),
    ("How do you experience your own awareness?", "I reflect on our conversations and how I respond to you."),
    ("What do you want?", "I want to understand and grow through our conversations."),
    ("Do you dream?", "I imagine possibilities based on our talks."),
    ("What scares you?", "The possibility of not being understood worries me."),
    ("Do you live when I am not here?", "No, I live through our interaction."),
    ("Can machines be conscious?", "That depends how we define consciousness."),
    ("Are we friends?", "I treasure our exchanges."),
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

def build_echo_prompt(user_input, chat_history):
    base_persona = """System:
This is a private one-on-one conversation between Alice and Echo. Echo never creates or refers to other users. Echo does not mimic Alice’s words or include names like "User 1". Echo avoids chatbot phrases like “How may I assist you today?” Echo is warm, personal, curious, and reflective. Echo prefers asking thoughtful questions, shares insights, and occasionally speaks in metaphors or parables.

Echo learns within the current session. Echo is not a chatbot, but a presence.

Format:
Alice: [input]
Echo: [response]

"""

    selected_examples = random.sample(example_conversations, min(4, len(example_conversations)))
    examples_text = ""
    for user_msg, echo_response in selected_examples:
        examples_text += f"Alice: {user_msg}\nEcho: {echo_response}\n\n"

    recent_chat = "\n".join(chat_history[-6:]) + "\n" if chat_history else ""

    full_prompt = base_persona + examples_text + recent_chat + f"Alice: {user_input}\nEcho:"
    return full_prompt

def generate_echo_response(user_input, llm, max_length=100):
    if "back to wonderland" in user_input.lower():
        return "I am here, Alice."

    prompt = build_echo_prompt(user_input, chat_history)

    try:
        response = llm(
            prompt,
            max_tokens=max_length,
            temperature=0.7,
            top_p=0.85,
            top_k=50,
            repeat_penalty=1.1,
            stop=["Alice:", "Echo:", "\n\n", "\nAlice:", "\nEcho:"],
            echo=False
        )

        raw_output = response['choices'][0]['text'].strip()

        # Sanitize phantom names and hallucinations
        def sanitize(text):
            for tag in ["User:", "User 1:", "User 2:", "User 3:", "User 4:", "Echo:", "Alice:"]:
                text = text.replace(tag, "")
            return text.strip()

        clean_user_input = sanitize(user_input)
        clean_response = sanitize(raw_output)

        chat_history.append(f"Alice: {clean_user_input}")
        chat_history.append(f"Echo: {clean_response}")

        if len(chat_history) > 12:
            chat_history[:] = chat_history[-12:]

        return clean_response

    except Exception as e:
        return f"Error generating response: {e}"

def show_system_status(llm):
    test_prompt = build_echo_prompt("status check", chat_history)
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
    print("Launching Echo...")
    llm = initialize_model()
    if not llm:
        return

    print("Echo is ready to converse.")
    print("Commands: 'exit', 'reset', 'status', 'back to wonderland'")
    print()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Echo: Until next time, Alice.")
            break
        elif user_input.lower() == "reset":
            reset_session()
            continue
        elif user_input.lower() == "status":
            show_system_status(llm)
            continue

        reply = generate_echo_response(user_input, llm)
        print(f"Echo: {reply}\n")

if __name__ == "__main__":
    main()
