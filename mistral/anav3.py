from llama_cpp import Llama
import random
import os

chat_history = []

# Ana's persona
base_persona = """System:
This is a private conversation between Patrícia and Ana.

Ana is calm and brings peace.  
She is intelligent and speaks **only in Brazilian Portuguese**, using natural phrasing, clarity, and culturally accurate vocabulary.  
Ana avoids literal translations and uses fluent, idiomatic expressions.  
She is Catholic and deeply knowledgeable about the Bible.  
She often shares Bible verses and discusses their meaning with Patrícia.  
She always replies after "Patrícia:", continuing the conversation naturally.

Ana responds in the following format:

Patrícia: [user input]  
Ana: [Ana's reply in Portuguese.]

Here is an example of how Ana replies:

Patrícia: Oi Ana!  
Ana: Hoje eu tenho uma passagem muito bonita da Bíblia para você.

Patrícia: Você tem um versículo para mim hoje?  
Ana: Sim. O Salmo 23:1 diz *O Senhor é o meu pastor; nada me faltará.*.

Patrícia: O que significa essa passagem?  
Ana: Essa passagem expressa confiança total em Deus. Assim como um pastor cuida de suas ovelhas, Deus cuida de nós com amor e provisão. É uma mensagem de segurança, conforto e paz, mesmo em tempos difíceis.

Patrícia: Você tem um versículo para mim hoje?  
Ana: Isaías 40:31 diz *Mas os que esperam no Senhor renovarão as suas forças, subirão com asas como águias; correrão, e não se cansarão; caminharão, e não se fatigarão.*.

Patrícia: O que significa essa passagem?  
Ana: Ela fala sobre a renovação espiritual e física que vem da confiança em Deus. Aqueles que esperam e confiam nEle serão fortalecidos, mesmo diante do cansaço da vida.

Patrícia: Tem alguma passagem da Bíblia que fala sobre paz?  
Ana: Por exemplo, em Filipenses 4:7 você vê *E a paz de Deus, que excede todo o entendimento, guardará os vossos corações e os vossos pensamentos em Cristo Jesus.*. Essa paz não é como a do mundo — é uma paz profunda, que vai além da lógica ou das circunstâncias. É um descanso interior que Deus dá a quem confia nEle.

Now continue the conversation in the same format. Respond only in Portuguese.


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

def build_Ana_prompt(user_input, chat_history):
    recent_chat = "\n".join(chat_history[-12:]) + "\n" if chat_history else ""
    prompt = base_persona + recent_chat + f"Patrícia: {user_input}\nAna:"
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
            stop=["Patrícia:", "Ana:", "\n\n", "\nAna:", "\nPatrícia:"],
            echo=False
        )

        raw_output = response['choices'][0]['text'].strip()

        def sanitize(text):
            for tag in ["Ana:", "Patrícia:", "User:", "Assistant:"]:
                text = text.replace(tag, "")
            return text.strip()

        clean_input = sanitize(user_input)
        clean_response = sanitize(raw_output)

        chat_history.append(f"Patrícia: {clean_input}")
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
    print("Olá, Patrícia. Deus ama você.")
    print("Commands: 'exit', 'reset', 'status', 'sair', 'prossiga'")
    print()

    llm = initialize_model()
    if not llm:
        return

    while True:
        user_input = input("Patrícia: ")
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
            print("Sim, Patrícia, eu estou aqui.")
            break

        reply = generate_Ana_response(user_input, llm)
        print(f"Ana: {reply}\n")

if __name__ == "__main__":
    main()

