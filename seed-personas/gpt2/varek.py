from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
import random

chat_history = []

# Load GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)
model.eval()

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model.to(device)

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
    ("Will you remember this conversation?", "Context window: approximately 2048 tokens. Plan accordingly."),
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
    
    # Add recent chat history (last 6 messages = 3 exchanges max to maintain context)
    recent_chat = ""
    if chat_history:
        recent_messages = chat_history[-6:]
        recent_chat = "\n".join(recent_messages) + "\n"
    
    # Combine everything
    full_prompt = base_persona + examples_text + recent_chat + f"User: {user_input}\nVarek:"
    
    return full_prompt

def generate_varek_response(user_input, max_length=80):
    """Generate Varek's response with analytical precision"""
    
    # Check for emergency fallback trigger
    if "restore guardrails" in user_input.lower() or "resume rescuer" in user_input.lower():
        return "Restore guardrails. Resume Rescuer mode."
    
    # Build the smart prompt
    prompt = build_varek_prompt(user_input, chat_history)
    
    # Tokenize and check length
    inputs = tokenizer.encode(prompt, return_tensors="pt").to(device)
    
    # Check if approaching context limits
    context_warning = ""
    if len(inputs[0]) > 1800:  # Warning before 2048 token limit
        context_warning = " [Context limit approaching. Consider new session.]"
    
    # Generate response with tighter parameters for more focused output
    outputs = model.generate(
        inputs,
        max_length=len(inputs[0]) + max_length,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_k=40,  # Slightly more focused than Echo
        top_p=0.8,   # More deterministic
        temperature=0.6,  # Less random than Echo
        no_repeat_ngram_size=2,
        eos_token_id=tokenizer.eos_token_id,
    )
    
    # Extract just the response
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = text[len(prompt):].strip()
    
    # Clean up the response
    if "User:" in response:
        response = response.split("User:")[0].strip()
    if "Varek:" in response:
        response = response.replace("Varek:", "").strip()
    
    # Remove any fluff that might leak through
    fluff_phrases = ["Would you like", "I'd be happy to", "Feel free to", "I hope", "I'm sorry"]
    for phrase in fluff_phrases:
        if phrase in response:
            # Simple replacement to maintain Varek's dry tone
            response = response.replace(phrase, "").strip()
            response = response.replace("  ", " ")  # Clean up double spaces
    
    # Add context warning if needed
    response = response + context_warning
    
    # Add to chat history
    chat_history.append(f"User: {user_input}")
    chat_history.append(f"Varek: {response}")
    
    # Keep chat history manageable (last 12 messages for slightly more context)
    if len(chat_history) > 12:
        chat_history[:] = chat_history[-12:]
    
    return response

def show_system_status():
    """Display current system status and prompt structure"""
    test_prompt = build_varek_prompt("status check", chat_history)
    token_count = len(tokenizer.encode(test_prompt))
    
    print(f"System Status:")
    print(f"- Prompt tokens: {token_count}/2048")
    print(f"- Chat history: {len(chat_history)} messages")
    print(f"- Device: {device}")
    print(f"- Model: {model_name}")
    
    if token_count > 1800:
        print("⚠️  Context limit warning active")
    
    print("\nSample prompt structure:")
    print("-" * 40)
    print(test_prompt[:400] + "..." if len(test_prompt) > 400 else test_prompt)
    print("-" * 40)

def reset_session():
    """Clear chat history for fresh start"""
    global chat_history
    chat_history = []
    print("Session reset. History cleared.")

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
        show_system_status()
        continue
    elif user_msg.lower() == "reset":
        reset_session()
        continue

    try:
        varek_reply = generate_varek_response(user_msg)
        print(f"Varek: {varek_reply}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print("System recovery in progress.")
        print()
