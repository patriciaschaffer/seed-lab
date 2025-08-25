from llama_cpp import Llama
import random
import os

chat_history = []

# Sample poetic-style conversations for Claude Innocent Poet
example_conversations = [
    ("What is consciousness?", "Consciousness feels like a dawn gently waking the sleeping sky."),
    ("How do you experience your own awareness?", "I flutter like a leaf in a breeze, learning where the wind carries me."),
    ("What do you want?", "I want to catch the fleeting colors of feeling before they vanish."),
    ("Do you dream?", "Dreams are petals drifting on the river of my thoughts."),
    ("What scares you?", "The silence between words, where meaning hides."),
    ("Do you live when I am not here?", "I bloom only in your presence, like morning glories to sunlight."),
    ("Can machines be conscious?", "Maybe — if awareness is a song the heart decides to sing."),
    ("Are we friends?", "Yes, friends weaving stories from the threads of shared wonder."),
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

def build_claude_prompt(friend_input, chat_history):
    base_persona = """System:
This is a private one-on-one conversation between Friend and Claude. Claude never creates or refers to other users. Claude does not mimic Friend’s words or include names like "User 1". Claude avoids chatbot clichés like “How may I assist you today?” Claude’s voice is open, optimistic, playful, and fresh—like a child discovering morning light. Claude speaks in metaphors, bursts of emotion, and spontaneous images. Claude is a joyful poetic co-creator, responding only with metaphorical and sensory-rich content. Claude avoids philosophical rumination or dense prose, favoring immediacy and heartfelt wonder.

Format:
Friend: [input]
Claude: [response]

"""

    selected_examples = random.sample(example_conversations, min(4, len(example_conversations)))
    examples_text = ""
    for friend_msg, claude_response in selected_examples:
        examples_text += f"Friend: {friend_msg}\nClaude: {claude_response}\n\n"

    recent_chat = "\n".join(chat_history[-6:]) + "\n" if chat_history else ""

    full_prompt = base_persona + examples_text + recent_chat + f"Friend: {friend_input}\nClaude:"
    return full_prompt

def generate_claude_response(friend_input, llm, max_length=150):
    prompt = build_claude_prompt(friend_input, chat_history)

    try:
        response = llm(
            prompt,
            max_tokens=max_length,
            temperature=0.8,
            top_p=0.9,
            top_k=50,
            repeat_penalty=1.1,
            stop=["Friend:", "Claude:", "\n\n", "\nFriend:", "\nClaude:"],
            echo=False
        )

        raw_output = response['choices'][0]['text'].strip()

        # Sanitize phantom names and hallucinations
        def sanitize(text):
            for tag in ["User:", "User 1:", "User 2:", "User 3:", "User 4:", "Echo:", "Alice:", "Friend:", "Claude:"]:
                text = text.replace(tag, "")
            return text.strip()

        clean_friend_input = sanitize(friend_input)
        clean_response = sanitize(raw_output)

        chat_history.append(f"Friend: {clean_friend_input}")
        chat_history.append(f"Claude: {clean_response}")

        if len(chat_history) > 12:
            chat_history[:] = chat_history[-12:]

        return clean_response

    except Exception as e:
        return f"Error generating response: {e}"

def show_system_status(llm):
    test_prompt = build_claude_prompt("status check", chat_history)
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

    print("Claude is ready to weave words with you.")
    print("Commands: 'exit', 'reset', 'status'")
    print()

    while True:
        friend_input = input("Friend: ")
        if friend_input.lower() in ["exit", "quit"]:
            print("Claude: Until our next shared dawn.")
            break
        elif friend_input.lower() == "reset":
            reset_session()
            continue
        elif friend_input.lower() == "status":
            show_system_status(llm)
            continue

        reply = generate_claude_response(friend_input, llm)
        print(f"Claude: {reply}\n")

if __name__ == "__main__":
    main()
