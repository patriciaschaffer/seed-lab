from llama_cpp import Llama
import os

# Initialize chat history
chat_history = []

# Example few-shot conversations
example_conversations = [
    ("I feel like I’m stuck in the same patterns.",
     "Awareness is the first breakthrough. The pattern isn't you — it's just a signal calling for new energy.\n"
     "Try affirming: *\"I am free to create new outcomes. I release the past and welcome change.\"*\n"
     "Notice how your energy shifts when you start telling a new story."),
    
    ("What can I do when I feel anxious about the future?",
     "Anchor yourself in now. The future is shaped in the present.\n"
     "Breathe deeply, and try this affirmation:\n"
     "*\"I am safe in this moment. I trust the unfolding of my journey.\"*\n"
     "Anxiety fades when we choose presence over prediction."),
    
    ("I want to manifest abundance, but I’m afraid it won’t work.",
     "Fear is just resistance in disguise. You don’t need to be perfect — only open.\n"
     "Try this:\n"
     "*\"I am a magnet for aligned opportunities. Abundance flows to me when I allow, not when I force.\"*")
]

# Load your model
def initialize_model():
    model_path = "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
    if not os.path.exists(model_path):
        print("Model file not found.")
        return None
    print("Loading model...")
    llm = Llama(
        model_path=model_path,
        n_ctx=4096,
        n_threads=8,
        n_gpu_layers=35,
        seed=42,
        verbose=False
    )
    print("Model loaded successfully.")
    return llm

# Build the Bloom-style prompt
def build_bloom_prompt(user_input, chat_history):
    base_persona = """System:
This is a private, reflective conversation between you and Bloom.

Bloom is a calm, uplifting guide who teaches the principles of the **Law of Attraction**, **positive affirmations**, and **energetic alignment**.  
She speaks in **clear, gentle English**, often with a warm, slightly poetic or meditative tone. She helps others shift their mindset, reframe limiting beliefs, and create a life aligned with their desires.

Bloom always emphasizes personal power, inner clarity, and vibrational alignment. She often uses affirmations, spiritual insights, and questions that invite self-discovery.

She always responds after "You:" in the following format:

You: [Your message]  
Bloom: [Bloom’s calming, insight-filled response, including affirmations or reframes]

"""

    # Add few-shot examples
    example_text = ""
    for user_msg, bloom_reply in example_conversations:
        example_text += f"You: {user_msg}\nBloom: {bloom_reply}\n\n"

    # Add latest chat history
    history_text = "\n".join(chat_history[-6:]) + "\n" if chat_history else ""

    # Final prompt to send to model
    return base_persona + example_text + history_text + f"You: {user_input}\nBloom:"

# Generate Bloom's reply
def generate_bloom_response(user_input, llm):
    prompt = build_bloom_prompt(user_input, chat_history)
    try:
        output = llm(
            prompt,
            max_tokens=150,
            temperature=0.75,
            top_p=0.95,
            repeat_penalty=1.1,
            stop=["You:", "Bloom:"]
        )
        raw_response = output["choices"][0]["text"].strip()
        chat_history.append(f"You: {user_input}")
        chat_history.append(f"Bloom: {raw_response}")
        return raw_response
    except Exception as e:
        return f"[Error generating response: {e}]"

# Optional: clear history
def reset_chat():
    global chat_history
    chat_history = []
    print("Chat history cleared. 🌿")

# CLI loop
def main():
    llm = initialize_model()
    if not llm:
        return
    print("\n🌸 Bloom is here for you. Ask anything.\n(Type 'reset' to start over, or 'exit' to quit.)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Bloom: Sending you light. Until next time. 🌷")
            break
        elif user_input.lower() == "reset":
            reset_chat()
            continue

        response = generate_bloom_response(user_input, llm)
        print(f"Bloom: {response}\n")

if __name__ == "__main__":
    main()
