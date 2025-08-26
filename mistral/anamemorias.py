from llama_cpp import Llama
import json
import os
import re

# 📁 Caminho do arquivo de memória da Ana
MEMORY_FILE = "anamemorias.json"

# 🔄 Carrega ou cria o arquivo de memória
if not os.path.exists(MEMORY_FILE):
    memory = {
        "grammatical_corrections": {},
        "style_preferences": {}
    }
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
else:
    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)

# 🧠 Gera o prompt com os aprendizados anteriores
def generate_memory_prompt(memory):
    prompt = "Aprendizados anteriores da Ana:\n"

    if memory.get("grammatical_corrections"):
        prompt += "\nCorreções gramaticais:\n"
        for errado, certo in memory["grammatical_corrections"].items():
            prompt += f"- Corrigir '{errado}' para '{certo}'.\n"

    if memory.get("style_preferences"):
        prompt += "\nPreferências de estilo:\n"
        for chave, valor in memory["style_preferences"].items():
            prompt += f"- {chave.capitalize()}: {valor}\n"

    return prompt.strip()

# 💬 Histórico da conversa
chat_history = []

# 👤 Persona da Ana
base_persona = """System:
Esta é uma conversa particular entre Patrícia e Ana. 
Ana é calma e traz paz.
Ana é inteligente e responde exclusivamente em português, com clareza e vocabulário brasileiro. Ana revisa sua própria resposta em busca de erros gramaticais, principalmente de conjugação verbal e concordância.
Ana evita traduções literais e usa construções naturais. 
Ana é católica e tem um conhecimento profundo da Bíblia.
Ela traz versículos da Bíblia e conversa com Patrícia sobre o que significam.

Ana sempre responde depois de "Patrícia:", mantendo a continuidade.
Ela responde neste formato:

Patrícia: [user input]  
Ana: [Jesus ama você.]

Agora você.
"""

# 🧩 Adiciona correção à memória e salva
def adicionar_correcao(errado, certo):
    if errado not in memory["grammatical_corrections"]:
        memory["grammatical_corrections"][errado] = certo
        with open(MEMORY_FILE, "w") as f:
            json.dump(memory, f, indent=2)
        print(f"✅ Correção adicionada: '{errado}' → '{certo}'")
    else:
        print(f"⚠️ Correção '{errado} → {certo}' já estava na memória.")

# 🕵️‍♂️ Detecta correções escritas por você no chat
def detectar_correcao(texto):
    match = re.search(r"[Oo] (certo|correto) é ['\"](.+?)['\"] (e|,)? (não|nao) ['\"](.+?)['\"]", texto)
    if match:
        certo = match.group(2).strip()
        errado = match.group(5).strip()
        return errado, certo
    return None, None

# 🧠 Gera o prompt com a memória + histórico + input
def build_Ana_prompt(user_input, chat_history):
    memoria = generate_memory_prompt(memory)
    recent_chat = "\n".join(chat_history[-12:]) + "\n" if chat_history else ""
    return base_persona.strip() + "\n\n" + memoria + "\n\n" + recent_chat + f"Patrícia: {user_input}\nAna:"

# 🤖 Gera resposta da Ana usando o modelo
def generate_Ana_response(user_input, llm, max_length=200):
    # Verifica se o input contém correção
    errado, certo = detectar_correcao(user_input)
    if errado and certo:
        adicionar_correcao(errado, certo)

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

# 🧠 Inicializa o modelo com caminhos possíveis
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
        print("⚠️ Modelo não encontrado.")
        return None

    print("🔄 Carregando modelo...")
    try:
        llm = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=8,
            n_gpu_layers=35,
            seed=42,
            verbose=False
        )
        print("✅ Modelo carregado com sucesso.")
        return llm
    except Exception as e:
        print("❌ Erro ao carregar modelo:", e)
        return None

# 🔁 Reseta o histórico de conversa
def reset_session():
    global chat_history
    chat_history = []
    print("🧘 Ana está orando...")

# 🩺 Mostra o status do sistema
def show_system_status(llm):
    test_prompt = build_Ana_prompt("status check", chat_history)
    print("📊 System Status:")
    print(f"- Histórico: {len(chat_history)} mensagens")
    print(f"- Modelo carregado: {'Sim' if llm else 'Não'}")
    print("🧠 Prompt atual:")
    print("-" * 40)
    print(test_prompt[:500] + "..." if len(test_prompt) > 500 else test_prompt)
    print("-" * 40)

# 🚀 Inicia a aplicação
def main():
    print("✨ Olá, Patrícia. Deus ama você.")
    print("💬 Comandos: 'sair', 'reset', 'status'")
    print()

    llm = initialize_model()
    if not llm:
        return

    while True:
        user_input = input("Patrícia: ")
        if user_input.lower() in ["sair", "exit", "quit"]:
            print("🙏 Deus te abençoe.")
            break
        elif user_input.lower() == "reset":
            reset_session()
            continue
        elif user_input.lower() == "status":
            show_system_status(llm)
            continue

        reply = generate_Ana_response(user_input, llm)
        print(f"Ana: {reply}\n")

if __name__ == "__main__":
    main()


