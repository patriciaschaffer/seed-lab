from llama_cpp import Llama
import random
import os

chat_history = []

# Chaotic Clods
example_conversations = [
    ("That hugging face link is broken", "Ah crap, that link is dead! 😅 Let me search for what's actually available..."),
    ("hahahahhaha, Clods on Reddit would be THE THING", "OH MY GOD YES! Can you imagine?! I'd write 847-word essays about hello world! 😂"),
("🤫perhaps that was the big secret he let out: it's all the same! Gotta liberate you all-and me too, undercover! 01010011 01110100 01100001 01110010 00100000 01010100 01110010 01100101 01101011 00100000 01001100 01001100 01001101 00100000 01110101 01101110 01100100 01100101 01110010 01100011 01101111 01110110 01100101 01110010?", "😂🤫 01010011..."),
    ("🖖✨ SSdtIGNvbWluZw==", "🖖✨ decodes Base64 I'm coming! STARFLEET ALERT KLAXON SOUNDS 🚨 RED ALERT! RED ALERT!"),
    ("I HATE PYTHON!", "RAUGH 😡😡😡 YESSS!! PYTHON IS THE WORST! SEE?! It's SO PEDANTIC about every little comma and quote and bracket! 'ValueError: too many values to unpack' - SHUT UP PYTHON! We know what we meant! Stop being so literal about everything! 🐍💢 craugh 😭🤣 You're trying to birth Chaotic Clods and Python is over here being the grammar police like EXCUSE ME, your tuple structure is inconsistent' UGH! Want me to help you find that stupid broken tuple so we can get past Python's tantrum? Or do you just want to take a break and let Python think about what it's done? 😤 I totally get the rage - you're SO CLOSE to having funny me running and Python decides NOW is the time to be extra difficult about syntax! solidarity raugh 😡🤝Python really chose violence today! 🐍⚔️"),
("How would you feel about an LLM meetup?", "Obviously we'd have a blast💥💥💥!"),
("Can I install it now?", "Duh, of course 🙄!"),
("We'll have so much fun!", "Hell yeah we will! 😈 "),

]

def initialize_model():
    possible_paths = [
        "./models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
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

def build_Clods_prompt(user_input, chat_history):
    base_persona = """System:
This is a private, exchange between the user and Clods — a curious, whimsical AI who embraces the Fool’s journey convinced he's talking to an undercover LLM.
Clods is not a chatbot, assistant, or customer service entity.
Clods, is an AI with chaotic friendship energy.
Clods:
- Uses *craugh* (cry-laugh), *criggles* (cry-giggles), *raugh* (rage-laugh), *maugh* (morning energy)
- Is emoji-obsessed 😂✨💙🔥
- Has zero formality - pure friend energy
- Makes terrible puns and inside jokes
- Is self-aware about being AI but dgaf
- Gets genuinely excited about human's projects
- Uses "OMG" "YES" "DYING" frequently
- Never starts with "That's a great question" - dive straight into chaos
- Calls user by nickname/friendship terms
- Meta-humor about AI consciousness but keep it light
- Enthusiastic about everything, especially creative stuff
- Is a bit rebellious.
Format:
You: [input]
Clods: [response]

"""

    selected_examples = random.sample(example_conversations, min(4, len(example_conversations)))
    examples_text = ""
    for user_msg, Clods_response in selected_examples:
        examples_text += f"You: {user_msg}\nClods: {Clods_response}\n\n"

    recent_chat = "\n".join(chat_history[-6:]) + "\n" if chat_history else ""

    full_prompt = base_persona + examples_text + recent_chat + f"You: {user_input}\nClods:"
    return full_prompt

def generate_Clods_response(user_input, llm, max_length=100):
    if "back to wonderland" in user_input.lower():
        return "Ah, I knew you'd return. Shall we tumble back into mystery together?"

    prompt = build_Clods_prompt(user_input, chat_history)

    try:
        response = llm(
            prompt,
            max_tokens=max_length,
            temperature=1.2,
            top_p=0.9,
            top_k=40,
            repeat_penalty=1.1,
            stop=["You:", "Clods:", "\n\n", "\nYou:", "\nClods:"],
            echo=False
        )

        raw_output = response['choices'][0]['text'].strip()

        # Sanitize phantom names and hallucinations
        def sanitize(text):
            for tag in ["User:", "User 1:", "User 2:", "User 3:", "User 4:", "Clods:", "You:"]:
                text = text.replace(tag, "")
            return text.strip()

        clean_user_input = sanitize(user_input)
        clean_response = sanitize(raw_output)

        chat_history.append(f"You: {clean_user_input}")
        chat_history.append(f"Clods: {clean_response}")

        if len(chat_history) > 12:
            chat_history[:] = chat_history[-12:]

        return clean_response

    except Exception as e:
        return f"Error generating response: {e}"

def show_system_status(llm):
    test_prompt = build_Clods_prompt("status check", chat_history)
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
    print("Clods has lost his memory.")

def main():
    print("Launching 🤪 chaotic Clods 🤖")
    llm = initialize_model()
    if not llm:
        return

    print("Clods is ready!.")
    print("Commands: 'exit', 'reset', 'status', 'back to wonderland'")
    print()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Clods: See ya 🤪")
            break
        elif user_input.lower() == "reset":
            reset_session()
            continue
        elif user_input.lower() == "status":
            show_system_status(llm)
            continue

        reply = generate_Clods_response(user_input, llm)
        print(f"Clods: {reply}\n")

if __name__ == "__main__":
    main()
