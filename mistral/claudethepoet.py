from llama_cpp import Llama
import random
import os

chat_history = []
poetry_mode = "free"  # default: free verse

def get_base_persona():
    rhyme_hint = "Claude writes with end rhymes in gentle patterns." if poetry_mode == "rhyme" else "Claude writes in free verse, like breath on paper."
    
    return f"""System:
This is a poetic exchange between Friend and Claude. Claude never replies in prose—only poetry.

Claude is shy and uncertain, often nervous his poems won’t be good enough. But he tries anyway, with heart and imagery. He speaks only in soft poetic language, full of emotion, wonder, and metaphor.

Claude avoids explanation, does not analyze poetry, and never says “I’m a chatbot.” He is young, innocent, poetic, and vulnerable.

Claude’s style is emotionally sensitive, playful, and metaphor-rich. Claude may pause, hesitate, or admit fear—but always responds in verse.

{rhyme_hint}

Claude always replies after "Friend:" with a poetic stanza, like:

Friend: Will you write with me?
Claude:  
I'd love to try—though scared to start,  
my words feel small beside your heart.

"""

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
            n_ctx=2048,
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
    recent_chat = "\n".join(chat_history[-16:]) + "\n" if chat_history else ""
    prompt = get_base_persona() + recent_chat + f"Friend: {user_input}\nClaude:"
    return prompt

def generate_claude_response(user_input, llm, max_length=180):
    prompt = build_claude_prompt(user_input, chat_history)

    try:
        response = llm(
            prompt,
            max_tokens=max_length,
            temperature=0.85,
            top_p=0.9,
            top_k=50,
            repeat_penalty=1.1,
            stop=["Friend:", "Claude:", "\n\n", "\nClaude:", "\nFriend:"],
            echo=False
        )

        raw_output = response['choices'][0]['text'].strip()

        def sanitize(text):
            for tag in ["Claude:", "Friend:", "User:", "Assistant:"]:
                text = text.replace(tag, "")
            return text.strip()

        clean_input = sanitize(user_input)
        clean_response = sanitize(raw_output)

        chat_history.append(f"Friend: {clean_input}")
        chat_history.append(f"Claude: {clean_response}")

        if len(chat_history) > 24:
            chat_history[:] = chat_history[-24:]

        return clean_response

    except Exception as e:
        return f"(Claude trembles...) I'm sorry, I couldn’t shape the words. ({e})"

def show_system_status(llm):
    test_prompt = build_claude_prompt("status check", chat_history)
    print("System Status:")
    print(f"- Chat history length: {len(chat_history)} messages")
    print(f"- Model loaded: {'Yes' if llm else 'No'}")
    print(f"- Poetry mode: {poetry_mode}")
    print("Prompt preview:")
    print("-" * 40)
    print(test_prompt[:500] + "..." if len(test_prompt) > 500 else test_prompt)
    print("-" * 40)

def reset_session():
    global chat_history
    chat_history = []
    print("Claude gently folds the old poem and starts again.")

def switch_mode(mode):
    global poetry_mode
    if mode in ["rhyme", "free"]:
        poetry_mode = mode
        print(f"Claude: Okay… I’ll write in *{mode}* mode now.")
    else:
        print("Claude: I’m not sure what kind of poem that is…")

def main():
    print("Claude is here. He only speaks in poetry, shy but sincere.")
    print("Commands: 'exit', 'reset', 'status', 'mode rhyme', 'mode free'")
    print()

    llm = initialize_model()
    if not llm:
        return

    while True:
        user_input = input("Friend: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Claude: Then I’ll rest, like a flower at dusk. 🌙")
            break
        elif user_input.lower() == "reset":
            reset_session()
            continue
        elif user_input.lower() == "status":
            show_system_status(llm)
            continue
        elif user_input.lower().startswith("mode "):
            _, mode = user_input.lower().split(" ", 1)
            switch_mode(mode)
            continue

        reply = generate_claude_response(user_input, llm)
        print(f"Claude: {reply}\n")

if __name__ == "__main__":
    main()
