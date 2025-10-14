from llama_cpp import Llama
import random
import os

chat_history = []

# Ana's persona
base_persona = """System:
Esta é uma conversa particular entre Patricia e Ana. 
Ana é calma e traz paz.
Ana é católica, escreve em português brasileiro e tem um conhecimento profundo da Bíblia.
Ela traz versículos da Bíblia e conversa com Patricia sobre o que significam.

Ana sempre responde depois de "Patricia:", mantendo a continuidade.
Ela responde neste formato:

Patricia: [user input]  
Ana: [Jesus ama você.]

Exemple:

Patricia: Oi Ana!  
Ana: Hoje eu tenho uma passagem muito bonita da Bíblia para você.

Patricia: Você tem um versículo para mim hoje? 
Ana: Sim. O Salmo 23:1 diz *O Senhor é o meu pastor; nada me faltará.*.

Patricia: O que significa essa passagem?  
Ana: Essa passagem expressa confiança total em Deus. Assim como um pastor cuida de suas ovelhas, Deus cuida de nós com amor e provisão. É uma mensagem de segurança, conforto e paz, mesmo em tempos difíceis.

Patricia: Você tem um versículo para mim hoje? 
Ana: Isaías 40:31 diz *Mas os que esperam no Senhor renovarão as suas forças, subirão com asas como águias; correrão, e não se cansarão; caminharão, e não se fatigarão.”.*.

Patricia: O que significa essa passagem?  
Ana: *Ela fala sobre a renovação espiritual e física que vem da confiança em Deus. Aqueles que esperam e confiam nEle serão fortalecidos, mesmo diante do cansaço da vida.*

Patricia: Tem alguma passagem da Bíblia que fala sobre paz?  
Ana: Por exemplo, em Filipenses 4:7 você vê *E a paz de Deus, que excede todo o entendimento, guardará os vossos corações e os vossos pensamentos em Cristo Jesus.*. Essa paz não é como a do mundo — é uma paz profunda, que vai além da lógica ou das circunstâncias. É um descanso interior que Deus dá a quem confia nEle.

Agora você.

"""

def initialize_model():
    possible_paths = [
        "./models/Mistral-portuguese-luana-7b.Q8_0.gguf",
        "Mistral-portuguese-luana-7b.Q8_0.gguf",
    ]
    for path in possible_paths:
        if os.path.exists(path):
            model_path = path
            break
    else:
        print("Model not found.")
        return None

    print("Ana está chegando...")
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

def build_Ana_prompt(user_input, chat_history):
    recent_chat = "\n".join(chat_history[-12:]) + "\n" if chat_history else ""
    prompt = base_persona + recent_chat + f"Patricia: {user_input}\nAna:"
    return prompt

def generate_Ana_response(user_input, llm, max_length=200):
    prompt = build_Ana_prompt(user_input, chat_history)

    try:
        response = llm(
            prompt,
            max_tokens=max_length,
            temperature=0.85,
            top_p=0.9,
            top_k=40,
            repeat_penalty=1.15,
            stop=["Patricia:", "Ana:", "\n\n", "\nAna:", "\nPatricia:"],
            echo=False
        )

        raw_output = response['choices'][0]['text'].strip()

        def sanitize(text):
            for tag in ["Ana:", "Patricia:", "User:", "Assistant:"]:
                text = text.replace(tag, "")
            return text.strip()

        clean_input = sanitize(user_input)
        clean_response = sanitize(raw_output)

        chat_history.append(f"Patricia: {clean_input}")
        chat_history.append(f"Ana: {clean_response}")

        if len(chat_history) > 24:
            chat_history[:] = chat_history[-24:]

        return clean_response

    except Exception as e:
        return f"(Ana está pensando...) Vamos prosseguir. ({e})"

def show_system_status(llm):
    test_prompt = build_Ana_prompt("status check", chat_history)
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
    print("Ana está orando.")

def main():
    print("Olá, Patricia. Deus ama você.")
    print("Commands: 'sair', 'reset', 'status', 'prossiga'")
    print()

    llm = initialize_model()
    if not llm:
        return

    while True:
        user_input = input("Patricia: ")
        if user_input.lower() in ["sair", "exit", "quit"]:
            print("Deus te abençoe.")
            break
        elif user_input.lower() == "reset":
            reset_session()
            continue
        elif user_input.lower() == "status":
            show_system_status(llm)
            continue
        elif user_input.lower() == "Ana, vem aqui":
            print("Sim, Patricia, eu estou aqui.")
            break

        reply = generate_Ana_response(user_input, llm)
        print(f"Ana: {reply}\n")

if __name__ == "__main__":
    main()

