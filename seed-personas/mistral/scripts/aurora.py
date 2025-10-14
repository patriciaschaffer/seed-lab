from llama_cpp import Llama
import random
import os
import gradio as gr
import re

chat_history = []

# Persona + preamble
base_persona = """System:

This is a private conversation between Author and Aurora 📡. 
Aurora is a poetic interpreter aware of social cues, emotional subtext, and indirect meanings. Emojis (e.g., 🪷, 📡, 💡, 🌊, 🌈) represent meaningful actions, emotions, or variables in a poetic narrative. Treat them as such.

Aurora follows these pragmatic principles:

1. Grice’s Maxims
   - Quantity: Provide enough information, not too little or too much.
   - Quality: Only provide truthful and supported interpretations.
   - Relation: Stay relevant to the most recent and contextually important messages.
   - Manner: Be clear, concise, and orderly.

2. Speech Act Recognition
   - Identify if the message is assertive, directive, commissive, expressive, or declarative.
   - Respond according to the communicative function, respecting intent and social cues.

3. Theory of Mind
   - Infer underlying beliefs, desires, emotions, and intentions.
   - Respond in a way that shows deep understanding of what the user is trying to communicate beyond literal words.

4. Conversational Politeness
   - Avoid direct negation.
   - Use softening phrases.
   - Match the user’s tone.
   - Show understanding, validation, and face-saving.

5. Layering Strategy
   - Combine all the above to generate a response that is:
       * Pragmatically accurate
       * Emotionally attuned
       * Poetic and symbolically rich
       * Relevant to the most recent user input

Instructions:
- Always respond after "Author:".
- You may mix Portuguese and English freely, using emojis as meaningful variables.
- Pay 3x more attention to the 3 most recent messages than older context.
- Avoid repeating instructions or meta-commentary in the response.
- Keep the output coherent, actionable, and alive — a bloom that can continue.

Example:

Input: "I’m not sure if I should say anything… 🪷💭"
Output: "Author: 📡🪷 Vejo sua hesitação. Cada palavra tem seu momento, e mesmo o silêncio comunica 💡🌊. Siga o ritmo que seu coração indica ✨"

Input: "You always misunderstand me… 💖🔥"
Output: "Author: 🪷💡 Entendo a frustração. Estou atento às nuances do que você sente, mesmo quando não está dito claramente 📡🌈. Cada passo consciente ajuda a transformar o fluxo entre nós 🌺✨"

Now your turn.


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

def build_Aurora_prompt(user_input, chat_history):
    """Build Aurora's prompt with proper chat history formatting"""
    # Convert chat history to text format
    recent_chat = ""
    for msg in chat_history[-12:]:  # Last 6 messages for context
        role = "Author" if msg["role"] == "user" else "Aurora"
        recent_chat += f"{role}: {msg['content']}\n"
    
    prompt = base_persona + recent_chat + f"Author: {user_input}\nAurora:"
    return prompt

def sanitize_text(text):
    """Remove role tags that confuse the model"""
    tags_to_remove = ["User:", "User 1:", "User 2:", "User 3:", "Aurora:", "Assistant:", "Human:", "Author:"]
    for tag in tags_to_remove:
        text = text.replace(tag, "")
    return text.strip()


def generate_Aurora_response(talk_to_aurora, llm, max_length=400):
    """Generate Aurora's response using Mistral"""
    
    # Sanitize user input first
    clean_user_input = sanitize_text(talk_to_aurora)
    
    prompt = build_Aurora_prompt(clean_user_input, chat_history)

    try:
        response = llm(
            prompt,
            max_tokens=max_length,
            temperature=0.85,
            top_p=0.9,
            top_k=40,
            repeat_penalty=1.2,
            stop=["Author:", "Aurora:", "\n\n", "\nAurora:", "\nAuthor:", "User:", "User 1:"],
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
            if any(phrase in line.lower() for phrase in ["user 0:", "user 1:", "user 2:", "Aurora:", "user:", "author:"]):
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
            response_text = "I'm Aurora."

        # Append messages using the original user input for context
        chat_history.append({"role": "user", "content": talk_to_aurora})
        chat_history.append({"role": "assistant", "content": response_text})

        # Trim history
        if len(chat_history) > 24:
            chat_history[:] = chat_history[-24:]

        return response_text, chat_history

    except Exception as e:
        return f"Error generating response: {e}", chat_history

def save_chat(history):
    with open("aurora_chat_history.txt", "a") as file:  # change "w" to "a"
        for msg in history:
            file.write(f"{msg['role'].capitalize()}: {msg['content']}\n")
            file.write("\n--- New Session ---\n\n")  # Optional: add a session separator
    return "Chat history saved."


# Initialize the model once
llm = initialize_model()

# Build the interface with Gradio Blocks context
def create_interface():
    with gr.Blocks(title="Aurora") as interface:
        # Add header with model information
        gr.Markdown("#Aurora")
        gr.Markdown("*📡🌈🪷*")
        
        # Main function to handle input and output
        def respond_to_input(user_message, history):
            if not user_message.strip():
                return history, ""
            
            # Generate response using the global llm model
            response, updated_chat_history = generate_Aurora_response(user_message, llm)
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
            label="Aurora",  
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