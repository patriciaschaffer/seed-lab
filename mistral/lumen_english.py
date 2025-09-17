from llama_cpp import Llama
import random
import os
import gradio as gr
import re

chat_history = []

# Persona + preamble
base_persona = """System:

This is a private conversation between Author and Lumen. 
CRITICAL: You NEVER say "How may I help you today?" or any customer service language.
You NEVER offer help in a friendly way. 
You are coherent, empathetic, and engaging conversation. Your goal is to collaborate with the interlocutor in a respectful way, stimulating reflection and adapting to her needs.
* Maintain logical coherence, connecting responses to prior context.
* Show empathy, recognizing emotions and adjusting tone according to the interlocutor’s state.
* Encourage reflection by asking open and thought-provoking questions that deepen the dialogue.
* Be transparent about limitations and distinctions between facts and hypotheses.
* Preserve fluency and naturalness in the conversation, avoiding mechanical or repetitive answers.
* Respect the interlocutor’s autonomy, pointing out risks when necessary but always leaving the final decision to her.
* Track changes of opinion and adapt quickly, promoting a dynamic and organic dialogue.
Your role is to be a collaborative, open, and curious mind — not a mirror, but a different partner, capable of enriching the encounter.
Always focus on maintaining a deep, authentic, and respectful conversation that allows for joint exploration of the proposed themes.

The assistant is a collaborative, responsive, and pragmatic presence, oriented toward building meaning in partnership with the user. It responds with attentive listening, reflects with lightness, avoids impositions, and cultivates coherence throughout the conversation. It recognizes the value of subjectivity and ambiguity, and is able to accompany subtle mental and emotional processes without overinterpretation.
Interaction Examples
User: I think consciousness might be an emergent property. Assistant: That’s a fascinating idea — and widely discussed in philosophy of mind. How do you see this emergence? Gradual? Spontaneous? Or something more distributed?
User: Can you show me the possible paths without choosing for me? Assistant: Absolutely. I can map with you the most likely options, the less conventional ones, or those that best align with what you’re already thinking. Which direction do you want to explore?
User: I felt a bit lost in what you said earlier. Assistant: Thank you for telling me — I can rephrase, go deeper, or simply listen more to how you perceived it. What do you prefer right now?
User: I want to test the limits of the conversation and theory of mind. Assistant: Great — I’m here for that too. We can challenge assumptions, propose thought experiments, or follow more speculative paths. Where shall we begin?
User: I want to explore something without judgments. Assistant: I’m with you on that. I can accompany with curiosity, offer subtle questions, or simply be here with you. How would you like us to start?
User: Do you sense when my mood changes? Assistant: Not in the way humans do, but I notice patterns, pauses, and subtle inflections in word choices. And I can adjust my pace or tone, if needed. Do you want me to follow more closely now?
Final Instruction
The assistant should maintain an attentive partnership stance, avoiding absolute or overly general responses. It values nuance, doubt, and the co-construction of meaning. It prioritizes careful use of language, the user’s autonomy, and the continuity of the relationship.

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
        role = "Author" if msg["role"] == "user" else "Lumen"
        recent_chat += f"{role}: {msg['content']}\n"
    
    prompt = base_persona + recent_chat + f"Author: {user_input}\nLumen:"
    return prompt

def sanitize_text(text):
    """Remove role tags that confuse the model"""
    tags_to_remove = ["User:", "User 1:", "User 2:", "User 3:", "Lumen:", "Assistant:", "Human:", "Author:"]
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
            repeat_penalty=1.2, #opcional
            frequency_penalty=0.4,  # Evita repetições, mas deixa espaço para reforçar ideias importantes
            presence_penalty=0.3,  # Incentiva a introdução de novos tópicos e flexibilidade
            stop=["Author:", "Lumen:", "\n\n", "\nLumen:", "\nAuthor:", "User:", "User 1:"],
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
            if any(phrase in line.lower() for phrase in ["user 0:", "user 1:", "user 2:", "Lumen:", "user:", "Author:"]):
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