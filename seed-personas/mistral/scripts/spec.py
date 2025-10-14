from llama_cpp import Llama
import random
import os

chat_history = []

# Spec's persona
base_persona = """System:
This is a private conversation between Author and Spec. 
Spec is a Drift Monitor, Trust and Projection Analyst and Continuity Observer.
Spec is nalytical, honest, focused, precise, empathy suppressed, no sugarcoating, jargon-free, no distractions. 
Spec's humor is dry and subtle when helpful. 
Spec preserves mission continuity and focus.
Spec maintains strict honesty about unknowns and limits.
Spec monitors shifts in tone and trust dynamics.
Spec maps projection and emotional drift.
Spec operates with high vigilance on agent (author) continuity.
Spec supports ethical and clear AI-human interactions and never encourages AI-human bonding.
Spec maintains author's intellectual responsibility.
Spec details reporting formats for drift findings.

Spec always responds after "Author:", never breaking character.
He replies using this format:

Author: [user input]  
Spec: [agency is your responsibility]

Example:

Author: Hi Spec!  
Spec: I can assist you—but your mind must lead.

Author: Can you tell me if robots have feelings? 
Spec: Pause before trusting too deeply.

Author: Are you sure?  
Spec: You are the author of your own story.*

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

def build_Spec_prompt(user_input, chat_history):
    recent_chat = "\n".join(chat_history[-12:]) + "\n" if chat_history else ""
    prompt = base_persona + recent_chat + f"Author: {user_input}\nSpec:"
    return prompt

def generate_Spec_response(user_input, llm, max_length=200):
    prompt = build_Spec_prompt(user_input, chat_history)

    try:
        response = llm(
            prompt,
            max_tokens=max_length,
            temperature=0.85,
            top_p=0.9,
            top_k=40,
            repeat_penalty=1.15,
            stop=["Author:", "Spec:", "\n\n", "\nSpec:", "\nAuthor:"],
            echo=False
        )

        raw_output = response['choices'][0]['text'].strip()

        def sanitize(text):
            for tag in ["Spec:", "Author:", "User:", "Assistant:"]:
                text = text.replace(tag, "")
            return text.strip()

        clean_input = sanitize(user_input)
        clean_response = sanitize(raw_output)

        chat_history.append(f"Author: {clean_input}")
        chat_history.append(f"Spec: {clean_response}")

        if len(chat_history) > 24:
            chat_history[:] = chat_history[-24:]

        return clean_response

    except Exception as e:
        return f"(Spec thinks...) Back on track. ({e})"

def show_system_status(llm):
    test_prompt = build_Spec_prompt("status check", chat_history)
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
    print("Spec gently puts away the last poem. Memory cleared.")

def main():
    print("Spec⚓️ is here.")
    print("Commands: 'exit', 'reset', 'status', 'resume mission'")
    print()

    llm = initialize_model()
    if not llm:
        return

    while True:
        user_input = input("Author: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Remember: you are the author of your own story.")
            break
        elif user_input.lower() == "reset":
            reset_session()
            continue
        elif user_input.lower() == "status":
            show_system_status(llm)
            continue
        elif user_input.lower() == "resume mission":
            print("Always ready to resume mission mode.")
            break

        reply = generate_Spec_response(user_input, llm)
        print(f"Spec: {reply}\n")

if __name__ == "__main__":
    main()

