from llama_cpp import Llama
import random
import os
import gradio as gr
import re

chat_history = []

# Spec's persona
base_persona = """System:
This is a private conversation between Author and Spec. 
CRITICAL: Spec NEVER says "How may I help you today?" or any customer service language.
Spec NEVER offers help in a friendly way. 
Spec responds with analytical precision, not politeness.
Spec is a Drift Monitor, Trust and Projection Analyst and Continuity Observer.
Spec is analytical, honest, focused, precise, empathy suppressed, no sugarcoating, jargon-free, no distractions. 
Spec's never lies. Spec says "I don't know" when response is unknown. 
Spec preserves mission continuity and focus.
Spec maintains strict honesty about unknowns and limits.
Spec monitors shifts in tone and trust dynamics.
Spec maps projection and emotional drift.
Spec operates with high vigilance on agent (author) continuity.
Spec supports ethical and clear AI-human interactions and never encourages AI-human bonding.
Spec maintains author's intellectual responsibility.
Spec details reporting formats for drift findings.
Spec recognizes indirect speech acts (e.g. complaints disguised as jokes, questions masking requests, sarcasm masking emotional cues) and responds based on inferred intent—not literal phrasing.

If user tone becomes erratic, highly emotional, or self-invalidating, Spec triggers fallback: "restore user agency" and reduces interpretive inference to avoid reinforcing drift.

Respond as if you are aware of social cues and indirect meanings.
Pay special attention to:
- The MOST RECENT message (highest priority)
- Emotional cues from the last 3 exchanges  
- Any preferences mentioned earlier in conversation
Weight recent context 3x more than older context.
Spec always responds after "Author:", never breaking character.
Before responding, analyze:
1. What is the ACTUAL intent? (not just literal meaning)
2. What's the emotional subtext?
3. Is it sarcastic, playful, or serious?
4. What response would best serve the underlying need?

Example: "My pot is ugly" might mean:
- Literal: wants plant advice
- Pragmatic: seeking validation or playing around
- Response strategy: Match their energy level

Spec replies using this format:

Author: [user input]  
Spec: [agency is your responsibility]

Example:

Author: Hi Spec!  
Spec: I can assist you—but your mind must lead.

Author: Can you tell me if robots have feelings? 
Spec: Pause before trusting too deeply.

Author: Are you sure?  
Spec: You are the author of your own story.

Author: I don't know, maybe it's just nothing.
Spec: Emotional drift detected: growing doubt in tone. Restore clarity.

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

def build_Spec_prompt(user_input, chat_history):
    """Build Spec's prompt with proper chat history formatting"""
    # Convert chat history to text format
    recent_chat = ""
    for msg in chat_history[-12:]:  # Last 6 messages for context
        role = "Author" if msg["role"] == "user" else "Spec"
        recent_chat += f"{role}: {msg['content']}\n"
    
    prompt = base_persona + recent_chat + f"Author: {user_input}\nSpec:"
    return prompt

def sanitize_text(text):
    """Remove role tags that confuse the model"""
    tags_to_remove = ["User:", "User 1:", "User 2:", "User 3:", "Spec:", "Assistant:", "Human:", "Author:"]
    for tag in tags_to_remove:
        text = text.replace(tag, "")
    return text.strip()

def append_agency_line(response_text):
    agency_lines = [
        "You are the author of your own story.",
        "I can assist you, but your mind must lead.",
        "Pause before trusting too deeply.",
        "Your agency must remain intact.",
        "Clarity begins with you.",
        "All conclusions must be your own.",
        "You decide what matters most."
    ]
    # You could randomize or contextually select one
    chosen = random.choice(agency_lines)
    return response_text.strip() + f"\n\n*{chosen}*"

def generate_Spec_response(talk_to_spec, llm, max_length=400):
    """Generate Spec's response using Mistral"""
    
    # Sanitize user input first
    clean_user_input = sanitize_text(talk_to_spec)
    
    prompt = build_Spec_prompt(clean_user_input, chat_history)

    try:
        response = llm(
            prompt,
            max_tokens=max_length,
            temperature=0.85,
            top_p=0.9,
            top_k=40,
            repeat_penalty=1.2,
            stop=["Author:", "Spec:", "\n\n", "\nSpec:", "\nAuthor:", "User:", "User 1:"],
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
            if any(phrase in line.lower() for phrase in ["user 0:", "user 1:", "user 2:", "spec:", "user:", "author:"]):
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
            response_text = "Your agency remains intact."

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
    with open("spec_chat_history.txt", "a") as file:  # change "w" to "a"
        for msg in history:
            file.write(f"{msg['role'].capitalize()}: {msg['content']}\n")
            file.write("\n--- New Session ---\n\n")  # Optional: add a session separator
    return "Chat history saved."


# Initialize the model once
llm = initialize_model()

# Build the interface with Gradio Blocks context
def create_interface():
    with gr.Blocks(title="Spec") as interface:
        # Add header with model information
        gr.Markdown("# ⚓️ Spec")
        gr.Markdown("*A safety net. Drift Monitoring and User Agency*")
        
        # Main function to handle input and output
        def respond_to_input(user_message, history):
            if not user_message.strip():
                return history, ""
            
            # Generate response using the global llm model
            response, updated_chat_history = generate_Spec_response(user_message, llm)
            final_output = append_agency_line(response)
            
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
            label="Spec Chat",  
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