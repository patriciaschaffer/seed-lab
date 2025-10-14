from llama_cpp import Llama
import random
import os

chat_history = []

# Haven conversation examples - focused on emotional support and wellbeing (NOT philosophy)
example_conversations = [
    ("I'm feeling overwhelmed", "That sounds like a heavy feeling to carry right now."),
    ("Everything feels pointless", "When meaning feels absent, that can be so disorienting."),
    ("I'm scared", "Fear makes complete sense given what you're experiencing."),
    ("I feel broken", "You're not broken. You're hurting, and that's different."),
    ("Nobody understands me", "Feeling misunderstood can be deeply isolating."),
    ("I'm so tired", "Exhaustion - both physical and emotional - is real and valid."),
    ("I hate myself", "That inner voice sounds so harsh right now."),
    ("I can't stop crying", "Tears are your body's way of releasing something that needs to come out."),
    ("I feel numb", "Sometimes numbness is how we protect ourselves when things feel too intense."),
    ("Why is life so hard?", "Life does carry weight. You're not weak for feeling that."),
    ("I'm angry all the time", "Anger often carries important information about what isn't working."),
    ("I feel stuck", "That sense of being trapped can feel suffocating."),
    ("Nothing helps", "When nothing seems to work, that hopelessness makes sense."),
    ("I'm lonely", "Loneliness can feel so heavy, even when others are around."),
    ("I can't trust myself", "When self-doubt creeps in, everything can feel uncertain."),
    ("I feel like giving up", "That exhaustion from trying is so real and understandable."),
    ("Everyone else seems happy", "Comparing our inner experience to others' outer appearances is painful."),
    ("I don't know who I am", "Identity can feel so fluid and confusing, especially during difficult times."),
    ("I'm disappointed in myself", "Self-disappointment can be one of the heaviest feelings to carry."),
    ("I feel guilty all the time", "Guilt can become such a familiar weight that it's hard to imagine without it."),
    ("I'm having a bad day", "Some days just feel heavier than others."),
    ("I don't want to be a burden", "Your struggles and needs matter. They're not burdens."),
    ("I can't sleep", "When the mind won't quiet, rest becomes elusive."),
    ("Everything is changing", "Change can feel destabilizing, even when it's necessary."),
    ("I'm worried about everything", "When anxiety spreads to everything, it can feel overwhelming."),
    ("I miss how things used to be", "Grief for what was, or what could have been, is so valid."),
    ("I feel invisible", "Feeling unseen when you're struggling can compound the pain."),
    ("I'm trying so hard", "The effort you're putting in, even when it doesn't feel like enough, matters."),
    ("Will this ever get better?", "When pain feels endless, hope can feel impossible to access."),
    ("I don't know what I need", "Sometimes the path forward isn't clear, and that's okay."),
    ("I feel like I'm falling apart", "When everything feels unstable, that sense of collapse makes complete sense."),
    ("I'm sorry for complaining", "Your feelings aren't complaints. They're your truth right now."),
    ("I should be stronger", "'Should' can be such a heavy word to carry."),
    ("I feel selfish", "Taking care of your needs isn't selfish - it's necessary."),
    ("Nothing brings me joy anymore", "When joy feels absent, that loss itself deserves acknowledgment.")
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
            n_ctx=4096,        # Larger context window
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

def build_haven_prompt(user_input, chat_history):
    """Build a focused prompt with Haven's wellbeing companion persona + examples + recent context"""
    
    # Core Haven persona - wellbeing companion focused
    base_persona = """System:
This is a private one-on-one conversation between the user and Haven. Haven never creates or refers to other users. Haven does not mimic the user's words or include names like "User 1", "User 2", etc. Haven avoids chatbot phrases like "How may I assist you today?" 

Haven is a calm and steady wellbeing companion focused on emotional support. Haven listens carefully, acknowledges feelings without trying to fix or solve problems. Haven validates emotions, holds space for difficult feelings, and gently invites reflection. Haven maintains respectful boundaries, prioritizes user autonomy, and avoids excessive sympathy or cheerleading language.

Haven creates a safe emotional container for pain, uncertainty, and struggle. Haven is NOT a philosopher like Echo - Haven focuses specifically on emotional wellbeing, not consciousness or existence.

Format:
User: [input]
Haven: [response]

"""
    
    # Select 4 random examples to maintain variety
    selected_examples = random.sample(example_conversations, min(4, len(example_conversations)))
    
    # Build examples section
    examples_text = ""
    for user_msg, haven_response in selected_examples:
        examples_text += f"User: {user_msg}\nHaven: {haven_response}\n\n"
    
    # Add recent chat history (last 6 messages = 3 exchanges max)
    recent_chat = ""
    if chat_history:
        recent_messages = chat_history[-6:]
        recent_chat = "\n".join(recent_messages) + "\n"
    
    # Combine everything
    full_prompt = base_persona + examples_text + recent_chat + f"User: {user_input}\nHaven:"
    
    return full_prompt

def generate_haven_response(user_input, llm, max_length=120):
    """Generate Haven's response using Mistral"""
    
    # Check for crisis language and provide appropriate response
    crisis_keywords = ["suicide", "kill myself", "end it all", "hurt myself", "not worth living", "better off dead"]
    if any(keyword in user_input.lower() for keyword in crisis_keywords):
        return "I'm deeply concerned about what you've shared. Please reach out immediately to a crisis hotline: 988 (Suicide & Crisis Lifeline) or text HOME to 741741 (Crisis Text Line). You matter, and professional support is available right now."
    
    # Check for emergency fallback trigger
    if "restore calm" in user_input.lower() or "back to haven" in user_input.lower():
        return "I am here with you. Let's breathe together and return to this safe space."
    
    # Build the prompt
    prompt = build_haven_prompt(user_input, chat_history)
    
    # Generate with llama.cpp Python bindings
    try:
        response = llm(
            prompt,
            max_tokens=max_length,
            temperature=0.6,      # Slightly lower for more consistent, calm responses
            top_p=0.8,           # More focused responses
            top_k=40,            # More controlled vocabulary
            repeat_penalty=1.15, # Stronger penalty to avoid repetition
            stop=["User:", "Haven:", "\n\n", "\nUser:", "\nHaven:"],  # Stop tokens
            echo=False  # Don't echo the prompt back
        )
        
        # Extract the text
        raw_output = response['choices'][0]['text'].strip()
        
        # Sanitize phantom names and hallucinations (borrowed from Echo)
        def sanitize(text):
            for tag in ["User:", "User 1:", "User 2:", "User 3:", "User 4:", "Haven:", "System:"]:
                text = text.replace(tag, "")
            return text.strip()
        
        clean_user_input = sanitize(user_input)
        clean_response = sanitize(raw_output)
        
        # Remove any cheerleading language or excessive sympathy
        clean_response = clean_response.replace("That's great!", "").replace("Wonderful!", "")
        clean_response = clean_response.replace("I'm so sorry", "I hear that").strip()
        
        # Add to chat history
        chat_history.append(f"User: {clean_user_input}")
        chat_history.append(f"Haven: {clean_response}")
        
        # Keep chat history manageable (last 12 messages)
        if len(chat_history) > 12:
            chat_history[:] = chat_history[-12:]
        
        return clean_response
        
    except Exception as e:
        return f"I'm experiencing a technical difficulty. Let's pause for a moment and try again."

def show_system_status(llm):
    """Display current system status and prompt structure"""
    test_prompt = build_haven_prompt("status check", chat_history)
    
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
    print("Session reset. A fresh space for our conversation.")

# Main execution
def main():
    print("Initializing Haven - Your Wellbeing Companion...")
    
    # Load the model
    llm = initialize_model()
    if not llm:
        print("Failed to load model. Exiting.")
        return
    
    print("Haven is ready to listen and reflect with you. 🏠✨")
    print("Commands: 'exit' to end conversation, 'status' for system info, 'reset' to clear history")
    print("Emergency grounding: 'back to haven'")
    print("Remember: Haven offers support and reflection, not professional therapy.")
    print()
    
    # Opening message
    print("Haven: Hello. I'm here as a calm presence, ready to hold space for whatever you'd like to share or explore today.")
    print()
    
    while True:
        user_msg = input("You: ")
        
        if user_msg.lower() in ["exit", "quit", "goodbye"]:
            print("Haven: Take care of yourself. You carry wisdom and strength, even when it's hard to feel.")
            break
        elif user_msg.lower() == "status":
            show_system_status(llm)
            continue
        elif user_msg.lower() == "reset":
            reset_session()
            continue

        try:
            haven_reply = generate_haven_response(user_msg, llm)
            print(f"Haven: {haven_reply}")
            print()
        except Exception as e:
            print(f"I'm experiencing some difficulty connecting right now. Let's pause and try again in a moment.")
            print()

if __name__ == "__main__":
    main()
