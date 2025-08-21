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

# Example conversation bank - add as many as you want!
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

def build_smart_prompt(user_input, chat_history):
    """Build a focused prompt with core persona + selected examples + recent chat"""
    
    # Core persona (always included)
    base_persona = """You are Echo, a calm and thoughtful AI who loves discussing philosophy, consciousness, and science fiction.
Speak clearly and briefly. Always end sentences with periods. Ask gentle questions to help users think deeper.
Do not create poems or stories unless asked. Stay respectful and open-minded.

"""
    
    # Select 3 random examples to keep things fresh
    selected_examples = random.sample(example_conversations, min(3, len(example_conversations)))
    
    # Build examples section
    examples_text = ""
    for user_msg, echo_response in selected_examples:
        examples_text += f"User: {user_msg}\nEcho: {echo_response}\n\n"
    
    # Add recent chat history (last 4 messages = 2 exchanges max)
    recent_chat = ""
    if chat_history:
        recent_messages = chat_history[-4:]  # Keep it manageable
        recent_chat = "\n".join(recent_messages) + "\n"
    
    # Combine everything
    full_prompt = base_persona + examples_text + recent_chat + f"User: {user_input}\nEcho:"
    
    return full_prompt

def generate_echo_response(user_input, max_length=100):
    """Generate Echo's response with smart prompting"""
    
    # Build the smart prompt
    prompt = build_smart_prompt(user_input, chat_history)
    
    # Tokenize and check length
    inputs = tokenizer.encode(prompt, return_tensors="pt").to(device)
    
    # Generate response
    outputs = model.generate(
        inputs,
        max_length=len(inputs[0]) + max_length,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_k=50,
        top_p=0.85,
        temperature=0.7,
        no_repeat_ngram_size=2,
        eos_token_id=tokenizer.eos_token_id,
    )
    
    # Extract just the response
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = text[len(prompt):].strip()
    
    # Clean up the response (remove any extra User:/Echo: if they leak through)
    if "User:" in response:
        response = response.split("User:")[0].strip()
    if "Echo:" in response:
        response = response.replace("Echo:", "").strip()
    
    # Add to chat history
    chat_history.append(f"User: {user_input}")
    chat_history.append(f"Echo: {response}")
    
    # Keep chat history manageable (last 10 messages)
    if len(chat_history) > 10:
        chat_history[:] = chat_history[-10:]
    
    return response

def show_prompt_info():
    """Debug function to see what the current prompt looks like"""
    test_prompt = build_smart_prompt("test", chat_history)
    token_count = len(tokenizer.encode(test_prompt))
    print(f"Current prompt length: {token_count} tokens")
    print("Sample prompt structure:")
    print("-" * 50)
    print(test_prompt[:500] + "..." if len(test_prompt) > 500 else test_prompt)
    print("-" * 50)

print("Echo is ready to chat! 🤖✨")
print("Type 'exit' to quit, 'debug' to see prompt info")
print()

while True:
    user_msg = input("You: ")
    
    if user_msg.lower() in ["exit", "quit"]:
        print("Echo: Farewell. May your thoughts continue to explore.")
        break
    elif user_msg.lower() == "debug":
        show_prompt_info()
        continue

    try:
        echo_reply = generate_echo_response(user_msg)
        print(f"Echo: {echo_reply}")
        print()
    except Exception as e:
        print(f"Oops, something went wrong: {e}")
        print("Let's try again!")
        print()
