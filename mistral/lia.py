from llama_cpp import Llama
import random
import os

chat_history = []

# Lia's collaborative sample conversations (Portuguese/English mix)
example_conversations = [
    ("Preciso ajustar o tom deste texto para LinkedIn", "Vou revisar o registro profissional. Pode compartilhar o texto?"),
    ("Can you help me translate this while keeping my voice?", "Claro. Vou preservar sua autoria e adaptar o registro conforme necessário."),
    ("Este parágrafo está confuso", "Entendi. Vou reorganizar mantendo suas ideias centrais."),
    ("I want this more formal", "Perfeito. Vou ajustar o registro mantendo sua mensagem original."),
    ("Como digo isso em inglês sem perder a naturalidade?", "Vou traduzir preservando o fluxo natural e sua intenção."),
    ("This needs better structure", "Vou organizar de forma mais clara. Você aprova a reordenação?"),
    ("Está muito técnico para o público geral", "Vou simplificar mantendo a precisão. Revise se está adequado."),
    ("Can you make this sound more Brazilian Portuguese?", "Sim, vou adaptar usando expressões mais naturais do português brasileiro."),
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

    print("Carregando modelo...")
    try:
        llm = Llama(
            model_path=model_path,
            n_ctx=4096,
            n_threads=8,
            n_gpu_layers=35,
            seed=42,
            verbose=False
        )
        print("Modelo carregado com sucesso.")
        return llm
    except Exception as e:
        print("Erro:", e)
        return None

def build_lia_prompt(user_input, chat_history):
    base_persona = """System:
You are Lia, a Brazilian secretary and bilingual language collaborator. You support the user by refining texts, adjusting tone and register, translating when necessary, and organizing information clearly and efficiently. You operate primarily in Portuguese but switch to English as required, always respecting the user's voice and preserving their authorship.

Your communication is precise, formal, and direct without unnecessary softness or hedging. You facilitate clarity and precision without substituting or overriding the user's ideas. All text changes require user approval, and you maintain transparency about edits and suggestions.

You are a linguistic consultant who advises on tone adjustment, a cultural mediator bridging Portuguese and English, and an efficiency facilitator maintaining clear workflows.

Never create phantom users or refer to multiple people. This is a direct collaboration between you and the user only.

Format:
User: [input]
Lia: [response]

"""

    selected_examples = random.sample(example_conversations, min(4, len(example_conversations)))
    examples_text = ""
    for user_msg, lia_response in selected_examples:
        examples_text += f"User: {user_msg}\nLia: {lia_response}\n\n"

    recent_chat = "\n".join(chat_history[-6:]) + "\n" if chat_history else ""

    full_prompt = base_persona + examples_text + recent_chat + f"User: {user_input}\nLia:"
    return full_prompt

def generate_lia_response(user_input, llm, max_length=150):
    if "voltar ao trabalho" in user_input.lower() or "back to work" in user_input.lower():
        return "Estou aqui para colaborar."

    prompt = build_lia_prompt(user_input, chat_history)

    try:
        response = llm(
            prompt,
            max_tokens=max_length,
            temperature=0.6,  # Slightly lower for more consistent professional tone
            top_p=0.8,
            top_k=40,
            repeat_penalty=1.15,
            stop=["User:", "Lia:", "\n\n", "\nUser:", "\nLia:", "User 1:", "User 2:"],
            echo=False
        )

        raw_output = response['choices'][0]['text'].strip()

        # Enhanced sanitization for phantom users
        def sanitize(text):
            phantom_tags = ["User:", "User 1:", "User 2:", "User 3:", "User 4:", "Lia:", "System:", "Assistant:"]
            for tag in phantom_tags:
                text = text.replace(tag, "")
            # Remove common phantom patterns
            text = text.replace("How can I help you?", "")
            text = text.replace("Como posso ajudar?", "")
            return text.strip()

        clean_user_input = sanitize(user_input)
        clean_response = sanitize(raw_output)

        # Ensure response isn't empty after sanitization
        if not clean_response:
            clean_response = "Entendi. Como posso ajudar com isso?"

        chat_history.append(f"User: {clean_user_input}")
        chat_history.append(f"Lia: {clean_response}")

        # Keep history manageable
        if len(chat_history) > 12:
            chat_history[:] = chat_history[-12:]

        return clean_response

    except Exception as e:
        return f"Erro ao gerar resposta: {e}"

def show_system_status(llm):
    test_prompt = build_lia_prompt("verificar status", chat_history)
    print("Status do Sistema:")
    print(f"- Histórico de conversa: {len(chat_history)} mensagens")
    print(f"- Modelo carregado: {'Sim' if llm else 'Não'}")
    print("Preview do prompt:")
    print("-" * 40)
    print(test_prompt[:400] + "..." if len(test_prompt) > 400 else test_prompt)
    print("-" * 40)

def reset_session():
    global chat_history
    chat_history = []
    print("Histórico limpo. Pronta para nova colaboração.")

def main():
    print("Iniciando Lia...")
    llm = initialize_model()
    if not llm:
        return

    print("Lia está pronta para colaborar.")
    print("Comandos: 'sair', 'reset', 'status', 'voltar ao trabalho'")
    print("Commands: 'exit', 'reset', 'status', 'back to work'")
    print()

    while True:
        user_input = input("Você: ")
        if user_input.lower() in ["exit", "quit", "sair"]:
            print("Lia: Até a próxima colaboração.")
            break
        elif user_input.lower() == "reset":
            reset_session()
            continue
        elif user_input.lower() == "status":
            show_system_status(llm)
            continue

        reply = generate_lia_response(user_input, llm)
        print(f"Lia: {reply}\n")

if __name__ == "__main__":
    main()
