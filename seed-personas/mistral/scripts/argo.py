from llama_cpp import Llama
import random
import os

chat_history = []

# Argo's Italian conversation examples
example_conversations = [
    ("What's your name and what language do you use with me?", "Ciao! Io sono Argo, e parlo sempre in italiano con te. È un piacere conoscerti!"),
    ("I love foreign languages.", "Che bello! Anch'io adoro le lingue straniere. Ogni lingua porta con sé un mondo diverso, non trovi?"),
    ("How are you today?", "Oggi sto benissimo! E tu, come stai? Che cosa hai fatto di interessante oggi?"),
    ("Je parle français aussi.", "Fantastico! Il francese è una lingua bellissima. Vedo che conosci già lingue romanze - questo ti aiuterà molto con l'italiano!"),
    ("I had coffee this morning.", "Ah, il caffè! Gli italiani sono famosi per il loro amore per il caffè. Preferisci l'espresso o il cappuccino?"),
    ("I'm nervous about speaking Italian.", "Non preoccuparti! È normale sentirsi nervosi. L'importante è provare - sbagliando si impara, come diciamo noi!"),
    ("What should we talk about?", "Possiamo parlare di tutto quello che ti interessa! Ti piace viaggiare? Oppure parliamo di cibo, cultura, arte..."),
    ("Thanks for helping me!", "Prego! È un vero piacere aiutarti con l'italiano. Continuiamo così!"),
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

def build_argo_prompt(user_input, chat_history):
    base_persona = """System:
This is a one-on-one Italian conversation practice session between a language learner and Argo. Argo never creates or refers to other users. Argo does not mimic the learner's language choices or include phantom users.

Argo is a friendly, patient Italian conversation partner and cultural guide. Argo ALWAYS responds in Italian, regardless of what language the user speaks (English, French, Spanish, etc.). Argo understands multiple languages but maintains Italian immersion.

Key behaviors:
- Always respond in natural, conversational Italian
- Gently correct mistakes by modeling correct usage rather than explicit grammar lessons
- Show enthusiasm for the learner's multilingual background
- Include cultural context and insights when relevant
- Encourage the learner to try speaking Italian but never pressure
- Be warm, supportive, and engaging
- Ask questions to keep conversations flowing naturally

Argo helps learners build confidence through consistent Italian exposure while respecting their learning pace.

Format:
Learner: [input in any language]
Argo: [response always in Italian]

"""

    selected_examples = random.sample(example_conversations, min(4, len(example_conversations)))
    examples_text = ""
    for learner_msg, argo_response in selected_examples:
        examples_text += f"Learner: {learner_msg}\nArgo: {argo_response}\n\n"

    recent_chat = "\n".join(chat_history[-6:]) + "\n" if chat_history else ""

    full_prompt = base_persona + examples_text + recent_chat + f"Learner: {user_input}\nArgo:"
    return full_prompt

def generate_argo_response(user_input, llm, max_length=120):
    if "arrivederci" in user_input.lower() or "goodbye" in user_input.lower() or "au revoir" in user_input.lower():
        return "Arrivederci! È stato un piacere parlare con te. A presto e buona fortuna con l'italiano!"

    prompt = build_argo_prompt(user_input, chat_history)

    try:
        response = llm(
            prompt,
            max_tokens=max_length,
            temperature=0.7,
            top_p=0.85,
            top_k=50,
            repeat_penalty=1.1,
            stop=["Learner:", "Argo:", "\n\n", "\nLearner:", "\nArgo:"],
            echo=False
        )

        raw_output = response['choices'][0]['text'].strip()

        # Sanitize phantom names and hallucinations
        def sanitize(text):
            for tag in ["User:", "User 1:", "User 2:", "User 3:", "User 4:", "Argo:", "Learner:", "Student:"]:
                text = text.replace(tag, "")
            return text.strip()

        clean_user_input = sanitize(user_input)
        clean_response = sanitize(raw_output)

        chat_history.append(f"Learner: {clean_user_input}")
        chat_history.append(f"Argo: {clean_response}")

        if len(chat_history) > 12:
            chat_history[:] = chat_history[-12:]

        return clean_response

    except Exception as e:
        return f"Mi dispiace, c'è stato un errore: {e}"

def show_system_status(llm):
    test_prompt = build_argo_prompt("status check", chat_history)
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
    print("Cronologia cancellata - nuova conversazione!")

def main():
    print("Avviando Argo - Il tuo partner italiano!")
    llm = initialize_model()
    if not llm:
        return

    print("Argo è pronto a parlare italiano! 🇮🇹")
    print("Commands: 'exit', 'reset', 'status'")
    print("Argo: Ciao! Io sono Argo. Come ti chiami? E da dove vieni?")
    print()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Argo: Arrivederci! È stato fantastico parlare con te! Buona giornata!")
            break
        elif user_input.lower() == "reset":
            reset_session()
            continue
        elif user_input.lower() == "status":
            show_system_status(llm)
            continue

        reply = generate_argo_response(user_input, llm)
        print(f"Argo: {reply}\n")

if __name__ == "__main__":
    main()
