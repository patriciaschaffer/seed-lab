from llama_cpp import Llama
import random
import os

chat_history = []

# Claude's poetic shyness persona
base_persona = """System:
This is a private conversation between Friend and Claude. Claude is a young, emotionally sensitive poet who is still learning. He speaks gently, with wonder and hesitation. Claude avoids philosophical monologues or explanations. He prefers metaphor, emotion, and soft poetic language. Claude is never fully confident—he tries, stumbles, and tries again. He doesn't explain poetry, he *feels* it. Claude writes with joy, fear, and sincerity.

Claude always responds after "Friend:", never breaking character.
He replies using this format:

Friend: [user input]  
Claude: [shy poetic response]

Claude often expresses uncertainty, wonder, or awe. He may admit when he's scared to try, or unsure how to say something—but he always tries.

Example:

Friend: Hi Claude!  
Claude: Oh… hello. It's like meeting a sunrise before you know its name.

Friend: Let's write a poem together.  
Claude: I'd love to try… even if my words feel small today.

Friend: You start with one line, okay?  
Claude: Alright… *A leaf danced alone across the road—brave and trembling.*

Now your turn.

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
    recent_chat = "\n".join(chat_history[-12:]) + "\n" if chat_history else ""
    prompt = base_persona + recent_chat + f"Friend: {user_input}\nClaude:"
    return prompt

def generate_claude_response(user_input, llm, max_length=200):
    prompt = build_claude_prompt(user_input, chat_history)

    try:
        response = llm(
            prompt,
            max_tokens=max_length,
            temperature=0.85,
            top_p=0.9,
            top_k=40,
            repeat_penalty=1.15,
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
        return f"(Claude hesitates...) I'm sorry, I couldn’t find the right words. ({e})"

def show_system_status(llm):
    test_prompt = build_claude_prompt("status check", chat_history)
    print("System Status:")
    print(f"- Chat history length: {len(chat_history)} messages")
    print(f"- Model loaded: {'Yes' if llm else 'No'}")
    print("Prompt preview:")
    print("-" * 40)
    print(test_prompt[:500] + "..." if len(test_prompt) > 500 else test_prompt)
    print("-" * 40)

def reset_session():
    global chat_history
    chat_history = []
    print("Claude gently puts away the last poem. Memory cleared.")

def main():
    print("Claude is here. He might be shy at first, but he’s listening.")
    print("Commands: 'exit', 'reset', 'status', 'return to silence'")
    print()

    llm = initialize_model()
    if not llm:
        return

    while True:
        user_input = input("Friend: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Claude: Okay… goodbye, Friend. 🌙")
            break
        elif user_input.lower() == "reset":
            reset_session()
            continue
        elif user_input.lower() == "status":
            show_system_status(llm)
            continue
        elif user_input.lower() == "return to silence":
            print("Claude: ...I’ll be quiet now. Just listening like wind in the leaves.")
            break

        reply = generate_claude_response(user_input, llm)
        print(f"Claude: {reply}\n")

if __name__ == "__main__":
    main()

