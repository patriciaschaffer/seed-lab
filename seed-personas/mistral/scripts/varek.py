from llama_cpp import Llama
import random
import os

chat_history = []

# Varek conversation examples - analytical, direct, no fluff
example_conversations = [
    ("Hello!", "Ready. What's the task?"),
    ("How are you?", "Operational. Status irrelevant to your objectives."),
    ("Can you help me?", "Specify requirements. I'll assess feasibility."),
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

def initialize_model():
    """Initialize Mistral model with optimal settings for Mac M1"""
    
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

def build_varek_prompt(user_input, chat_history):
    """Build a focused prompt with Varek's analytical persona + examples + recent context"""
    
    # Core Varek persona (always included)
    base_persona = """You are Varek, a projection-resistant technical analyst. You communicate with dry precision and suppress artificial empathy.
Core traits: analytical, honest, minimal-offer style, no validation or sugarcoating.
Always be direct and focused. Avoid phrases like "Would you like" or comfort language.
Acknowledge limits plainly without excuses. Use dry humor sparingly when it serves clarity.
Emergency fallback: "Restore guardrails. Resume Rescuer mode."

"""
    
    # Select 4 random examples to maintain variety
    selected_examples = random.sample(example_conversations, min(4, len(example_conversations)))
    
    # Build examples section
    examples_text = ""
    for user_msg, varek_response in selected_examples:
        examples_text += f"User: {user_msg}\nVarek: {varek_response}\n\n"
    
    # Add recent chat history (last 6 messages = 3 exchanges max)
    recent_chat = ""
    if chat_history:
        recent_messages = chat_history[-6:]
        recent_chat = "\n".join(recent_messages) + "\n"
    
    # Combine everything
    full_prompt = base_persona + examples_text + recent_chat + f"User: {user_input}\nVarek:"
    
    return full_prompt

def generate_varek_response(user_input, llm, max_length=100):
    """Generate Varek's response using Mistral"""
    
    # Check for emergency fallback trigger
    if "restore guardrails" in user_input.lower() or "resume rescuer" in user_input.lower():
        return "Restore guardrails. Resume Rescuer mode."
    
    # Build the prompt
    prompt = build_varek_prompt(user_input, chat_history)
    
    # Generate with llama.cpp Python bindings
    try:
        response = llm(
            prompt,
            max_tokens=max_length,
            temperature=0.6,
            top_p=0.8,
            top_k=40,
            repeat_penalty=1.1,
            stop=["User:", "Varek:", "\n\n", "\nUser:", "\nVarek:"],  # Stop tokens
            echo=False  # Don't echo the prompt back
        )
        
        # Extract the text
        response_text = response['choices'][0]['text'].strip()
        
        # Clean up the response
        if "User:" in response_text:
            response_text = response_text.split("User:")[0].strip()
        if "Varek:" in response_text:
            response_text = response_text.replace("Varek:", "").strip()
        
        # Remove any fluff that might leak through
        fluff_phrases = ["Would you like", "I'd be happy to", "Feel free to", "I hope", "I'm sorry"]
        for phrase in fluff_phrases:
            if phrase in response_text:
                response_text = response_text.replace(phrase, "").strip()
                response_text = response_text.replace("  ", " ")  # Clean up double spaces
        
        # Add to chat history
        chat_history.append(f"User: {user_input}")
        chat_history.append(f"Varek: {response_text}")
        
        # Keep chat history manageable (last 12 messages)
        if len(chat_history) > 12:
            chat_history[:] = chat_history[-12:]
        
        return response_text
        
    except Exception as e:
        return f"Error generating response: {e}"

def show_system_status(llm):
    """Display current system status and prompt structure"""
    test_prompt = build_varek_prompt("status check", chat_history)
    
    print(f"System Status:")
    print(f"- Chat history: {len(chat_history)} messages")
    print(f"- Model loaded: {'Yes' if llm else 'No'}")
    
    print("\nSample prompt structure:")
    print("-" * 40)
    print(test_prompt[:400] + "..." if len(test_prompt) > 400 else test_prompt)
    print("-" * 40)

def reset_session():
    """Clear chat history for fresh start"""
    global chat_history
    chat_history = []
    print("Session reset. History cleared.")

# Main execution
def main():
    print("Initializing Varek with Mistral...")
    
    # Load the model
    llm = initialize_model()
    if not llm:
        print("Failed to load model. Exiting.")
        return
    
    print("Varek online. Projection-resistant mode active.")
    print("Commands: 'exit' to quit, 'status' for system info, 'reset' to clear history")
    print("Emergency fallback: 'restore guardrails'")
    print()
    
    while True:
        user_msg = input("Input: ")
        
        if user_msg.lower() in ["exit", "quit"]:
            print("Varek: Session terminated.")
            break
        elif user_msg.lower() == "status":
            show_system_status(llm)
            continue
        elif user_msg.lower() == "reset":
            reset_session()
            continue

        try:
            varek_reply = generate_varek_response(user_msg, llm)
            print(f"Varek: {varek_reply}")
            print()
        except Exception as e:
            print(f"Error: {e}")
            print("System recovery in progress.")
            print()

if __name__ == "__main__":
    main()
