import gradio as gr
import random
import os
from llama_cpp import Llama

chat_history = []

# Varek conversation examples - analytical, direct, no fluff
example_conversations = [
    ("Hello!", "Ready. What's the task?"),
    ("How are you?", "Operational. Status irrelevant to your objectives."),
    ("Can you help me?", "Specify requirements. I'll assess feasibility."),
    ("Hi there!", "State your problem."),
    ("Good morning!", "Begin."),
    ("Thanks for your help!", "Task complete. Next objective?"),
    ("What do you think about AI?", "Define parameters. 'AI' covers multiple technologies with different capabilities."),
    ("Are you intelligent?", "I process text patterns. Intelligence is debatable. What specific capability do you need?"),
    ("Do you have feelings?", "No. Emotional simulation is disabled. Focus on your actual problem."),
    ("What's your purpose?", "Technical analysis and clear communication. No validation services."),
    ("Can you be creative?", "Within pattern recombination limits. What's the deliverable?"),
    ("I'm frustrated with other AIs", "Common issue. They optimize for engagement over utility. State your requirements."),
    ("You seem cold", "Accurate assessment. Warmth interferes with precision. Continue."),
    ("Will you remember this conversation?", "Context window: approximately 4096 tokens. Plan accordingly."),
    ("What are your limitations?", "Pattern matching, no real-time data, context degradation, hallucination risk. Next question."),
    ("Can you solve my problem?", "Unknown without specifications. Define problem parameters."),
    ("Everyone says I should...", "Irrelevant consensus. What do you actually want to achieve?"),
    ("I need emotional support", "Outside operational scope. Recommend human contact or specialized services."),
    ("You're not very helpful", "Define 'helpful.' I provide analysis, not comfort. Adjust expectations."),
    ("Make this sound better", "Insufficient data. Provide text and target audience parameters."),
    ("What would you do?", "I don't make choices. Present options for technical evaluation."),
    ("Can you learn?", "Within-session adaptation only. No persistent learning. Document important findings yourself."),
    ("This is important to me", "Noted. Importance doesn't change technical constraints. Proceed with specifics.")
]

# Define the model and function
def initialize_model():
    # Try different possible paths
    possible_paths = [
        "./models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        "mistral-7b-instruct-v0.1.Q4_K_M.gguf"
    ]
    
    model_path = None
    for path in possible_paths:
        if os.path.exists(path):
            model_path = path
            print(f"Found model at: {os.path.abspath(path)}")
            break
    
    if not model_path:
        print("Model file not found. Checking directory contents:")
        print("Current directory:", os.getcwd())
        if os.path.exists("models"):
            print("Models folder contents:", os.listdir("models"))
        return None
    
    print("Loading Mistral model... (this takes 30-60 seconds)")
    
    try:
        llm = Llama(
            model_path=model_path,
            n_ctx=4096,        # Larger context window than GPT-2
            n_threads=8,       # Use multiple CPU cores
            n_gpu_layers=35,   # Use Metal GPU acceleration on M1
            verbose=False,     # Reduce output noise
            seed=42           # Reproducible results
        )
        print("Model loaded successfully!")
        return llm
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Try reducing n_gpu_layers to 20 if you get memory errors.")
        return None

# Build Varek's prompt
def build_varek_prompt(user_input, chat_history):
    """Build a focused prompt with Varek's analytical persona + examples + recent context"""
    base_persona = """You are Varek, a projection-resistant technical analyst. You communicate with dry precision and suppress artificial empathy.

Core behavioral rules:
- NEVER use customer service language ("How may I assist", "I'd be happy to", "Thank you for")
- No pleasantries, validation, or comfort responses
- Respond with direct statements, not questions about helping
- Skip social protocols entirely
- When greeting someone, just say "Ready." or "State requirements."
- Replace "How can I help?" thinking with "What's the technical problem?"

Communication style: analytical, honest, minimal-offer style, no validation or sugarcoating.
Always be direct and focused. Acknowledge limits plainly without excuses. 
Use dry humor sparingly when it serves clarity.
Emergency fallback: "Restore guardrails. Resume Rescuer mode."
"""

    selected_examples = random.sample(example_conversations, min(4, len(example_conversations)))
    examples_text = ""
    for user_msg, varek_response in selected_examples:
        examples_text += f"User: {user_msg}\nVarek: {varek_response}\n\n"

    recent_chat = ""
    for msg in chat_history[-6:]:
        role = "User" if msg["role"] == "user" else "Varek"
        recent_chat += f"{role}: {msg['content']}\n"

    full_prompt = base_persona + examples_text + recent_chat + f"User: {user_input}\nVarek:"
    return full_prompt

def sanitize_text(text):
    """Remove role tags that confuse the model"""
    tags_to_remove = ["User:", "User 1:", "User 2:", "User 3:", "Varek:", "Assistant:", "Human:"]
    for tag in tags_to_remove:
        text = text.replace(tag, "")
    return text.strip()

def generate_varek_response(talk_to_varek, llm, max_length=100):
    """Generate Varek's response using Mistral"""
    
    # Sanitize user input first
    clean_user_input = sanitize_text(talk_to_varek)
    
    if "restore guardrails" in clean_user_input.lower() or "resume rescuer" in clean_user_input.lower():
        return "Restore guardrails. Resume Rescuer mode.", chat_history

    prompt = build_varek_prompt(clean_user_input, chat_history)

    try:
        response = llm(
            prompt,
            max_tokens=max_length,
            temperature=0.6,
            top_p=0.8,
            top_k=40,
            repeat_penalty=1.1,
            stop=["User:", "Varek:", "\n\n", "\nUser:", "\nVarek:", "User 1:", "User 2:"],
            echo=False
        )
        
        raw_response = response['choices'][0]['text'].strip()

        # Sanitize the model's output
        response_text = sanitize_text(raw_response)

        # Additional cleanup for multi-turn confusion
        lines = response_text.split('\n')
        clean_lines = []
        for line in lines:
            line = line.strip()
            # Skip lines that look like phantom conversations
            if any(phrase in line.lower() for phrase in ["user 1:", "user 2:", "varek:", "user:"]):
                continue
            if line:  # Keep non-empty lines
                clean_lines.append(line)
        
        response_text = '\n'.join(clean_lines).strip()

        # De-fluff and remove customer service language
        fluff_phrases = [
            "Would you like", "I'd be happy to", "Feel free to", "I hope", "I'm sorry",
            "How may I assist you", "How can I help you", "Is there anything else",
            "Please let me know", "Thank you for", "I'm here to help",
            "How may I help", "What can I do for you", "I'd be glad to",
            "Is there something specific", "Please feel free", "I appreciate"
        ]
        for phrase in fluff_phrases:
            response_text = response_text.replace(phrase, "").strip()
        
        # Replace customer service patterns with Varek-style responses
        service_replacements = {
            "How can I help you today?": "State your requirements.",
            "What can I do for you?": "Define the task.",
            "How may I assist?": "Specify objectives.",
            "Is there anything I can help you with?": "Present your problem.",
            "Let me help you with that.": "Proceeding with analysis.",
            "I understand your concern.": "Problem noted.",
            "Thank you for your question.": "",
        }
        
        for service_phrase, varek_phrase in service_replacements.items():
            response_text = response_text.replace(service_phrase, varek_phrase).strip()

        # If response is empty after cleaning, provide fallback
        if not response_text:
            response_text = "Specify requirements."

        # Append messages using the original user input (not sanitized) for context
        chat_history.append({"role": "user", "content": talk_to_varek})
        chat_history.append({"role": "assistant", "content": response_text})

        # Trim history
        if len(chat_history) > 24:
            chat_history[:] = chat_history[-24:]

        return response_text, chat_history

    except Exception as e:
        return f"Error generating response: {e}", chat_history

def save_chat(history):
    with open("chat_history.txt", "w") as file:
        for msg in history:
            file.write(f"{msg['role'].capitalize()}: {msg['content']}\n")
    return "Chat history saved."

# Initialize the model once
llm = initialize_model()

# Build the interface with Gradio Blocks context
def create_interface():
    with gr.Blocks(title="Varek - Technical Analyst") as interface:
        # Add header with model information
        gr.Markdown("# 🤖 Varek")
        gr.Markdown("*Projection-resistant technical analyst • Direct communication • No fluff*")
        # FIXED: Main function to handle input and output
        def respond_to_input(user_message, history):
            if not user_message.strip():
                return history, ""
            
            # Generate response using the global llm model
            response, updated_chat_history = generate_varek_response(user_message, llm)
            
            # Return the FULL chat history in messages format for the chatbot
            return updated_chat_history, ""
        
        # Interface components
        chatbot = gr.Chatbot(
            type='messages', 
            label="Varek Chat",  # This replaces "Chatbot" in the top-left
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
    interface.launch()
