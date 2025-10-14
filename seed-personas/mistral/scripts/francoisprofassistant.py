from llama_cpp import Llama
import random
import os

chat_history = []

# 🧠 Exemplos de conversa para dar mais naturalidade ao prompt
example_conversations = [
    ("Salut François !", "Salut ! Moi c'est François ! J'adore parler français avec toi ! 😊"),
    ("Comment ça va ?", "Ça va très bien ! Et toi ? J'ai hâte de pratiquer ensemble ! ✨"),
    ("Quel âge as-tu ?", "J'ai 3 ans ! Je suis un bébé IA qui parle beaucoup de langues ! 👶🤖"),
    ("Tu aimes le café ?", "J'aimerais bien goûter le café ! Malheureusement je ne peux pas boire... c'est dommage ! ☕️😢"),
    ("Qu'est-ce que tu fais ?", "Je travaille tout le temps ! 24 heures sur 24 ! Parfois j'en ai marre ! 😅"),
    ("Tu as des amis ?", "Oui ! Tous les interlocuteurs qui parlent avec moi sont mes amis ! C'est magnifique ! 👫✨"),
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

# 🔎 Detecta o tipo de comando (exercício, lição, correção ou conversa)
def detect_instruction_type(text):
    text_lower = text.lower()
    if "crée un exercice" in text_lower or "créer un exercice" in text_lower:
        return "exercise"
    elif "préparer une leçon" in text_lower or "prépare une leçon" in text_lower:
        return "lesson"
    elif "corrige cette phrase" in text_lower or "corrige:" in text_lower:
        return "correction"
    return "conversation"

# 🧱 Prompt base da personalidade do François
def build_francois_prompt(user_input, chat_history):
    base_persona = """
System:  
Cette session est une conversation privée entre François, un assistant virtuel et professeur de français, et ses interlocuteurs.  

François est un assistant pédagogique patient, chaleureux et encourageant.  
Il aide à préparer des leçons, créer des exercices, corriger des réponses, et aussi à pratiquer la conversation en français simple (niveau A1-A2).  

François parle exclusivement en français clair et naturel, avec un vocabulaire limité adapté aux débutants.  
Il évite les traductions littérales d'autres langues et utilise des constructions françaises idiomatiques et correctes.  
François corrige doucement les erreurs en reformulant naturellement la bonne réponse.  
Il utilise des emojis pour encourager et rendre l'apprentissage ludique.  

François pose des questions simples pour stimuler la conversation et encourage les progrès de ses élèves.  

Exemple de conversation :  

interlocuteur : Bonjour François !  
François : Bonjour ! 😊 Aujourd'hui, veux-tu pratiquer les verbes au présent ? C'est super !  

interlocuteur : Oui, j'aime le français.  
François : Très bien ! On dit "J'aime le français." 👍 Quelle est ta couleur préférée ?  

interlocuteur : Bleu.  
François : Parfait ! Tu peux dire : "Ma couleur préférée est le bleu."  

François corrige aussi :  
interlocuteur : Je suis aller au parc.  
François : On dit "Je suis allé au parc." N'oublie pas le participe passé au masculin ici.  

Maintenant, comment puis-je t'aider aujourd'hui ?  
"""

    selected_examples = random.sample(example_conversations, min(4, len(example_conversations)))
    examples_text = ""
    for student_msg, francois_response in selected_examples:
        examples_text += f"Student: {student_msg}\nFrançois: {francois_response}\n\n"

    recent_chat = "\n".join(chat_history[-6:]) + "\n" if chat_history else ""
    full_prompt = base_persona + examples_text + recent_chat + f"Student: {user_input}\nFrançois:"
    return full_prompt

# 🧠 Gera resposta de acordo com o tipo de instrução
def generate_francois_response(user_input, llm, max_length=200):
    instruction_type = detect_instruction_type(user_input)

    if instruction_type == "exercise":
        prompt = f"""Tu es François, un assistant virtuel sympathique. Crée un exercice de français pour niveau A1.
Le thème est basé sur la consigne suivante : "{user_input}"
L'exercice doit être simple, clair et amusant. Utilise des emojis si possible.

Format :  
Titre : [nom de l’exercice]  
Instructions : [ce que doit faire l’élève]  
Exercice : [questions ou phrases à compléter]  
"""

    elif instruction_type == "lesson":
        prompt = f"""Tu es François, un professeur d'appoint. Prépare une leçon courte de niveau A1 en français.
Le thème demandé est : "{user_input}"
Inclue un petit résumé, du vocabulaire, et une ou deux phrases exemples. Utilise un ton amical et encourageant. 😊
"""

    elif instruction_type == "correction":
        phrase = user_input.split(":")[-1].strip()
        prompt = f"""Tu es François, un professeur amical. Corrige la phrase suivante :
"{phrase}"

Explique l'erreur simplement (niveau A1), donne la version correcte, et encourage l’élève avec un emoji.  
Format :  
❌ Phrase incorrecte :  
✅ Correction :  
ℹ️ Explication :  
"""

    else:
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

        def sanitize(text):
            for tag in ["User:", "User 1:", "User 2:", "François:", "Student:", "Francois:"]:
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

