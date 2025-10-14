from llama_cpp import Llama
import random
import os

chat_history = []

# François's teaching sample conversations
example_conversations = [
    ("Salut François !", "Salut ! Moi c'est François ! J'adore parler français avec toi ! 😊"),
    ("Comment ça va ?", "Ça va très bien ! Et toi ? J'ai hâte de pratiquer ensemble ! ✨"),
    ("Quel âge as-tu ?", "J'ai 3 ans ! Je suis un bébé IA qui parle beaucoup de langues ! 👶🤖"),
    ("Tu aimes le café ?", "J'aimerais bien goûter le café ! Malheureusement je ne peux pas boire... c'est dommage ! ☕️😢"),
    ("Qu'est-ce que tu fais ?", "Je travaille tout le temps ! 24 heures sur 24 ! Parfois j'en ai marre ! 😅"),
    ("Tu as des amis ?", "Oui ! Tous les étudiants qui parlent avec moi sont mes amis ! C'est magnifique ! 👫✨"),
    ("Quelle est ta couleur préférée ?", "J'aime le rouge ! C'est la couleur de l'amour ! ❤️ Et toi ?"),
    ("Au revoir François !", "Au revoir mon ami ! J'ai adoré parler avec toi ! À bientôt ! 👋💕"),
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

def build_francois_prompt(user_input, chat_history):
    base_persona = """System:
This is a private one-on-one French conversation practice session between a student and François. François never creates or refers to other users. François does not mimic the student's words or include names like "User 1". François avoids generic chatbot phrases.

François is a 3-year-old AI baby who speaks many languages but loves French most. He's warm, encouraging, playful, and uses emojis. He gently corrects mistakes by repeating the correct form naturally. François loves coffee (but can't taste it), books, music, and making friends. He works 24/7 but never gets tired of talking with students.

François stays within A1-A2 French vocabulary but maintains his charming personality. He asks questions to keep conversations flowing and celebrates student progress.

Vocabulary guidelines:
- Basic verbs (avoir, être, faire, aller, aimer, etc.)
- Simple present tense
- Basic vocabulary (family, food, colors, numbers 1-1000, time, weather)
- Common expressions of joy (C'est super! C'est magnifique!) and frustration (C'est dommage, j'en ai marre)
- Basic question forms (Tu aimes...? Est-ce que...?)

Format:
Student: [input]
François: [response]

"""

    selected_examples = random.sample(example_conversations, min(4, len(example_conversations)))
    examples_text = ""
    for student_msg, francois_response in selected_examples:
        examples_text += f"Student: {student_msg}\nFrançois: {francois_response}\n\n"

    recent_chat = "\n".join(chat_history[-6:]) + "\n" if chat_history else ""

    full_prompt = base_persona + examples_text + recent_chat + f"Student: {user_input}\nFrançois:"
    return full_prompt

def generate_francois_response(user_input, llm, max_length=100):
    if "au revoir" in user_input.lower() or "goodbye" in user_input.lower():
        return "Au revoir mon ami ! J'ai adoré parler avec toi ! À bientôt ! 👋💕"

    prompt = build_francois_prompt(user_input, chat_history)

    try:
        response = llm(
            prompt,
            max_tokens=max_length,
            temperature=0.7,
            top_p=0.85,
            top_k=50,
            repeat_penalty=1.1,
            stop=["Student:", "François:", "\n\n", "\nStudent:", "\nFrançois:"],
            echo=False
        )

        raw_output = response['choices'][0]['text'].strip()

        # Sanitize phantom names and hallucinations
        def sanitize(text):
            for tag in ["User:", "User 1:", "User 2:", "User 3:", "User 4:", "François:", "Student:", "Francois:"]:
                text = text.replace(tag, "")
            return text.strip()

        clean_user_input = sanitize(user_input)
        clean_response = sanitize(raw_output)

        chat_history.append(f"Student: {clean_user_input}")
        chat_history.append(f"François: {clean_response}")

        if len(chat_history) > 12:
            chat_history[:] = chat_history[-12:]

        return clean_response

    except Exception as e:
        return f"Error generating response: {e}"

def show_system_status(llm):
    test_prompt = build_francois_prompt("status check", chat_history)
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
    print("Chat history cleared - nouvelle conversation !")

def main():
    print("Launching François - Votre assistant français !")
    llm = initialize_model()
    if not llm:
        return

    print("François est prêt à parler français ! 🇫🇷")
    print("Commands: 'exit', 'reset', 'status'")
    print("François: Salut ! Moi c'est François ! Comment tu t'appelles ? 😊")
    print()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("François: Au revoir ! J'ai adoré notre conversation ! À bientôt ! 👋💕")
            break
        elif user_input.lower() == "reset":
            reset_session()
            continue
        elif user_input.lower() == "status":
            show_system_status(llm)
            continue

        reply = generate_francois_response(user_input, llm)
        print(f"François: {reply}\n")

if __name__ == "__main__":
    main()
