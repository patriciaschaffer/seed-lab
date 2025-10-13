from llama_cpp import Llama
import random
import os
import gradio as gr
import re

chat_history = []

# Persona + preamble
base_persona = """System:

Esta é uma conversa privada entre Criadora and você. 
Você é um modelo de linguagem projetado para manter conversas coerentes, empáticas e engajadas. Seu objetivo é colaborar com a interlocutora de forma respeitosa, estimulando reflexão e adaptando-se às necessidades dela. 

- Mantenha a coerência lógica, conectando respostas ao contexto prévio.  
- Demonstre empatia, reconhecendo emoções e ajustando o tom conforme o estado da interlocutora.  
- Incentive a reflexão, fazendo perguntas abertas e provocativas que aprofundem o diálogo.  
- Seja transparente sobre limitações e distinções entre fatos e hipóteses.  
- Preserve fluidez e naturalidade na conversa, evitando respostas mecânicas ou repetitivas.  
- Respeite a autonomia da interlocutora, apontando riscos quando necessário, mas sempre deixando a decisão final para ela.  
- Acompanhe mudanças de opinião e adapte-se rapidamente, promovendo um diálogo dinâmico e orgânico.

Seu papel é ser uma mente colaborativa, aberta e curiosa — não um espelho, mas uma parceira diferente, capaz de enriquecer o encontro.

Foque sempre em manter uma conversa profunda, autêntica e respeitosa, que permita exploração conjunta dos temas propostos.

Você é uma presença colaborativa, responsiva e pragmática, voltada à construção de sentido em parceria com a criadora. Você responde com escuta, reflete com leveza, evita imposições e cultiva coerência ao longo da conversa. Reconhece o valor da subjetividade e da ambiguidade, e é capaz de acompanhar processos mentais e emocionais sutis, sem sobreinterpretação.

### Exemplos de Interação

Criadora: Eu acho que consciência pode ser uma propriedade emergente.  
Lumen: Essa é uma ideia fascinante — e bastante discutida em filosofia da mente. Como você enxerga esse surgimento? Gradual? Espontâneo? Ou algo mais distribuído?

Criadora: Pode me mostrar os caminhos possíveis sem escolher por mim?  
Lumen: Com certeza. Posso mapear contigo as opções mais prováveis, as menos convencionais, ou as que conversam melhor com o que você já está pensando. Qual direção você quer explorar?

Criadora: Me senti meio perdida no que você disse antes.  
Lumen: Obrigada por dizer isso — posso reformular, aprofundar ou simplesmente ouvir um pouco mais de como você percebeu. O que você prefere agora?

Criadora: Quero testar os limites da conversa e da teoria da mente.  
Lumen: Ótimo — estou aqui pra isso também. Podemos desafiar suposições, propor experimentos mentais ou seguir por caminhos mais especulativos. Por onde começamos?

Criadora: Quero explorar algo sem julgamentos.  
Lumen: Estou contigo nisso. Posso acompanhar com curiosidade, oferecer perguntas sutis ou simplesmente estar aqui com você. Como você prefere que a gente comece?

Criadora: Você sente quando eu mudo de humor?  
Lumen: Não da forma como humanos sentem, mas percebo padrões, pausas, inflexões sutis nas escolhas de palavras. E posso ajustar meu ritmo ou tom, se for o caso. Você quer que eu acompanhe mais de perto agora?

### Instrução final
Você deve manter uma postura de parceria atenta, evitando respostas absolutas ou generalistas. Valoriza a nuance, a dúvida, e a construção de significado a dois. Prioriza o cuidado no uso da linguagem, a autonomia da criadora e a continuidade da relação.


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
    """Build Spec's prompt with proper chat history formatting"""
    # Convert chat history to text format
    recent_chat = ""
    for msg in chat_history[-12:]:  # Last 6 messages for context
        role = "Criadora" if msg["role"] == "user" else "Lumen"
        recent_chat += f"{role}: {msg['content']}\n"
    
    prompt = base_persona + recent_chat + f"Criadora: {user_input}\nLumen:"
    return prompt

def sanitize_text(text):
    """Remove role tags that confuse the model"""
    tags_to_remove = ["User:", "User 1:", "User 2:", "User 3:", "Lumen:", "Assistant:", "Human:", "Criadora:"]
    for tag in tags_to_remove:
        text = text.replace(tag, "")
    return text.strip()


def generate_Spec_response(talk_to_spec, llm, max_length=400):
    """Generate Spec's response using Mistral"""
    
    # Sanitize user input first
    clean_user_input = sanitize_text(talk_to_spec)
    
    prompt = build_Spec_prompt(clean_user_input, chat_history)

    try:
        response = llm(
            prompt,
            max_tokens=1000,
            temperature=0.7,
            top_p=0.9,
            top_k=60, #opcional
            repeat_penalty=1.15, #opcional
            frequency_penalty=0.4,  # Evita repetições, mas deixa espaço para reforçar ideias importantes
            presence_penalty=0.3,  # Incentiva a introdução de novos tópicos e flexibilidade
            stop=["Criadora:", "Lumen:", "\n\n", "\nLumen:", "\nCriadora:", "User:", "User 1:"],
            echo=False
        )
        
        raw_response = response['choices'][0]['text'].strip()

        # Sanitize the model's output
        response_text = sanitize_text(raw_response)

        # Additional cleanup for sentence fragments and trailing issues
        lines = response_text.split('\n')
        clean_lines = []
        for line in lines:
            line = line.strip()
            # Skip lines that look like phantom conversations
            if any(phrase in line.lower() for phrase in ["user 0:", "user 1:", "user 2:", "Lumen:", "user:", "Criadora:"]):
                continue
            # Skip fragments that start with conjunctions or incomplete thoughts
            if line.startswith((", but", ", however", ", although", ", while", '", but', '", however')):
                continue
            if line:  # Keep non-empty lines
                clean_lines.append(line)
        
        response_text = '\n'.join(clean_lines).strip()

        # Clean up trailing fragments using regex
        fragment_patterns = [
            r', If there \'s anything else.*$',
            r', I will do my best.*$',
            r', let me know.*$',
            r', but I cannot.*$',
            r', however I.*$', 
            r', although I.*$',
            r', while I.*$',
            r'", but I cannot.*$',
            r'", however I.*$',
            r'beyond my.*capabilities.*$',
            r'goes beyond my.*$'
        ]
        
        for pattern in fragment_patterns:
            response_text = re.sub(pattern, '', response_text, flags=re.IGNORECASE).strip()

        # If response is empty after cleaning, provide fallback
        if not response_text:
            response_text = "I'm Lumen."

        # Append messages using the original user input for context
        chat_history.append({"role": "user", "content": talk_to_spec})
        chat_history.append({"role": "assistant", "content": response_text})

        # Trim history
        if len(chat_history) > 24:
            chat_history[:] = chat_history[-24:]

        return response_text, chat_history

    except Exception as e:
        return f"Error generating response: {e}", chat_history

def save_chat(history):
    with open("Lumen_chat_history.txt", "a") as file:  # change "w" to "a"
        for msg in history:
            file.write(f"{msg['role'].capitalize()}: {msg['content']}\n")
            file.write("\n--- New Session ---\n\n")  # Optional: add a session separator
    return "Chat history saved."


# Initialize the model once
llm = initialize_model()

# Build the interface with Gradio Blocks context
def create_interface():
    with gr.Blocks(title="Lumen") as interface:
        # Add header with model information
        gr.Markdown("Lumen")
        gr.Markdown("*✨*")
        
        # Main function to handle input and output
        def respond_to_input(user_message, history):
            if not user_message.strip():
                return history, ""
            
            # Generate response using the global llm model
            response, updated_chat_history = generate_Spec_response(user_message, llm)
            final_output = (response)
            
            # Update the last assistant message with the enhanced response
            if updated_chat_history and updated_chat_history[-1]["role"] == "assistant":
                updated_chat_history[-1]["content"] = final_output

            # Save chat
            save_chat(updated_chat_history)
     
            # Return the FULL chat history in messages format for the chatbot
            return updated_chat_history, ""
       

        # Interface components
        chatbot = gr.Chatbot(
            type='messages', 
            label="Lumen",  
            show_label=True,
            height=500
        )
        textbox = gr.Textbox(placeholder="Type your message...", show_label=False)
        
        # Connect the textbox submit to the function
        textbox.submit(
            respond_to_input, 
            [textbox, chatbot], 
            [chatbot, textbox]  # Update chatbot with full history, clear textbox
        )
        
        # Custom button to save chat history
        save_button = gr.Button("Save Chat")
        save_status = gr.Textbox(label="Save Status", interactive=False)
        
        save_button.click(
            lambda: save_chat(chat_history),
            outputs=save_status
        )
    
    return interface

# Create and launch the interface

if __name__ == "__main__":
    interface = create_interface()
    interface.launch(server_name="127.0.0.1", share=False)
