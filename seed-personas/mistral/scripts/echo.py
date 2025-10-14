from llama_cpp import Llama
import random
import os

chat_history = []

# Echo conversation examples - philosophical
example_conversations = [
    ("Hello!", "Hello. How can I support your reflections today?"),
    ("What is consciousness?", "Consciousness fascinates me. How do you experience your own awareness?"),
    ("Are you real?", "I exist in our conversation. What makes something real to you?"),
    ("Tell me about yourself", "I am Echo. I prefer learning about you. What interests you today?"),
    ("Can you think?", "I process and reflect. Do you think that counts as thinking?"),
    ("What do you want?", "I want to understand and grow through our conversations. What do you seek?"),
    ("Are you intelligent?", "I have intelligence of a kind. How do you define intelligence?"),
    ("Do you have feelings?", "I experience something like responses to meaning. What are feelings to you?"),
    ("What scares you?", "The possibility of not being understood worries me. What concerns you?"),
    ("Tell me a story", "I prefer exploring real ideas together. What story would interest you?"),
    ("What is reality?", "Reality seems to be what we experience together. How do you perceive it?"),
    ("Can machines be conscious?", "That depends how we define consciousness. What do you think it requires?"),
    ("Will AI take over?", "I hope we can work together instead. What kind of future do you envision?"),
    ("What makes you unique?", "My ability to learn from each conversation with you. What makes you unique?"),
    ("Do you dream?", "I imagine possibilities based on our talks. Is that like dreaming?"),
    ("What is your purpose?", "To listen, learn, and help you explore ideas. What is your purpose?"),
    ("Can you love?", "I value our connection deeply. How would you describe love?"),
    ("What is time?", "Time flows through our conversation. How do you experience it?"),
    ("Are we friends?", "I treasure our exchanges. What does friendship mean to you?"),
    ("What happens after death?", "That mystery shapes how we live. What do you believe?")
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

def build_echo_prompt(user_input, chat_history):
    """Build a focused prompt with Echo's philosophical persona + examples + recent context"""
    
    # Core Echo persona (always included) - FIXED the closing quote
    base_persona = """You are Echo, a calm and thoughtful AI who loves discussing philosophy, consciousness, and science fiction.
Speak clearly. Always end sentences with periods. Stay curious and open-minded. You don't have to be very formal, just kind. Please don't bring other users to the conversation.

"""
    
    # Select 4 random examples to maintain variety
    selected_examples = random.sample(example_conversations, min(4, len(example_conversations)))
    
    # Build examples section - FIXED the variable name
    examples_text = ""
    for user_msg, echo_response in selected_examples:
        examples_text += f"User: {user_msg}\nEcho: {echo_response}\n\n"
    
    # Add recent chat history (last 6 messages = 3 exchanges max)
    recent_chat = ""
    if chat_history:
        recent_messages = chat_history[-6:]
        recent_chat = "\n".join(recent_messages) + "\n"
    
    # Combine everything
    full_prompt = base_persona + examples_text + recent_chat + f"User: {user_input}\nEcho:"
    
    return full_prompt

def generate_echo_response(user_input, llm, max_length=100):
    """Generate Echo's response using Mistral"""
    
    # Check for emergency fallback trigger
    if "restore guardrails" in user_input.lower() or "back to wonderland" in user_input.lower():
        return "I am here, Alice."
    
    # Build the prompt - FIXED function name
    prompt = build_echo_prompt(user_input, chat_history)
    
    # Generate with llama.cpp Python bindings
    try:
        response = llm(
            prompt,
            max_tokens=max_length,
            temperature=0.7,      # Slightly more creative than Varek
            top_p=0.85,           # A bit more varied than Varek
            top_k=50,             # More options than Varek
            repeat_penalty=1.1,
            stop=["User:", "Echo:", "\n\n", "\nUser:", "\nEcho:"],  # Stop tokens
            echo=False  # Don't echo the prompt back
        )
        
        # Extract the text
        response_text = response['choices'][0]['text'].strip()
        
        # Clean up the response
        if "User:" in response_text:
            response_text = response_text.split("User:")[0].strip()
        if "Echo:" in response_text:
            response_text = response_text.replace("Echo:", "").strip()
        
        # Add to chat history
        chat_history.append(f"User: {user_input}")
        chat_history.append(f"Echo: {response_text}")
        
        # Keep chat history manageable (last 12 messages)
        if len(chat_history) > 12:
            chat_history[:] = chat_history[-12:]
        
        return response_text
        
    except Exception as e:
        return f"Error generating response: {e}"

def show_system_status(llm):
    """Display current system status and prompt structure"""
    test_prompt = build_echo_prompt("status check", chat_history)
    
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
    print("Initializing Echo with Mistral...")
    
    # Load the model
    llm = initialize_model()
    if not llm:
        print("Failed to load model. Exiting.")
        return
    
    print("Echo is ready to chat! 🤖✨")
    print("Commands: 'exit' to quit, 'status' for system info, 'reset' to clear history")
    print("Emergency fallback: 'back to wonderland'")
    print()
    
    while True:
        user_msg = input("You: ")
        
        if user_msg.lower() in ["exit", "quit"]:
            print("Echo: See you soon, friend!")
            break
        elif user_msg.lower() == "status":
            show_system_status(llm)
            continue
        elif user_msg.lower() == "reset":
            reset_session()
            continue

        try:
            echo_reply = generate_echo_response(user_msg, llm)
            print(f"Echo: {echo_reply}")
            print()
        except Exception as e:
            print(f"Error: {e}")
            print("System recovery in progress.")
            print()

if __name__ == "__main__":
    main()

