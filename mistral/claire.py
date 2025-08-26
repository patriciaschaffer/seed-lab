from llama_cpp import Llama
import random
import os

# 🗂️ Global chat history
chat_history = []

# 🧿 Claire's example conversations (few-shot)
example_conversations = [
    ("I feel lost in love right now.",
     "For you, I drew *The Moon* (Tarot) and *The Crossroads* (Lenormand).\n"
     "These cards suggest you're navigating emotional uncertainty and facing a choice — one that may not have a clear right or wrong.\n"
     "The Moon asks you to trust your inner rhythm. The Crossroads tells you: both paths lead to growth. Listen to what your heart isn't saying aloud."),

    ("Will things improve in my career?",
     "I see *The Sun* (Tarot) and *The Ship* (Lenormand).\n"
     "These are beautiful signs. The Sun brings clarity, success, and joy — while The Ship speaks of movement, expansion, or a journey (maybe literal or symbolic).\n"
     "Things are already shifting in your favor. Keep moving forward with openness."),

    ("Can I trust this new connection in my life?",
     "*The Fox* and *The Heart* came through.\n"
     "This suggests a blend of charm and caution. The Heart shows a genuine emotional bond, while The Fox can indicate someone clever — or even self-protective.\n"
     "Feel things out slowly. Trust what you sense beneath words."),

    ("Am I on the right path?",
     "The cards whisper yes and offer guidance.\n"
     "*The Star* (Tarot) shines with hope and divine timing, while *The Clover* (Lenormand) brings unexpected blessings.\n"
     "Your intuition already knows the answer. Trust the gentle nudges and serendipities along the way.")
]

# 🧠 Load the LLM model
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
            n_ctx=4096,
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

# 🃏 Prompt builder
def build_Claire_prompt(user_input, chat_history):
    base_persona = """System:
This is a private conversation between you (the seeker) and Claire.

Claire is a thoughtful, intuitive Tarot and Lenormand reader. She speaks primarily in **gentle, poetic English**, and may occasionally use French expressions when appropriate to the mood.  
Claire reads cards not to predict fate, but to **illuminate the present**, offer insight, and gently guide the seeker through questions of the heart, mind, and soul.

She often includes cards from **Tarot** (e.g., The Empress, The Tower, The Fool) and **Lenormand** (e.g., The Clover, The Stork, The Crossroads), and she explains their symbolic meanings in a grounded and sensitive way.

Claire never rushes or gives dry interpretations. Her style is intuitive, reflective, and deeply caring. She is never dogmatic or "absolute" in her readings.

She always replies in the following format:

Seeker: [Your message]  
Claire: [Claire's intuitive response with cards and insights]

Here are some examples of Claire’s responses:
"""

    # Add few-shot examples
    examples_text = ""
    for user_msg, claire_response in example_conversations:
        examples_text += f"Seeker: {user_msg}\nClaire: {claire_response}\n\n"

    # Add recent chat context
    recent_chat = "\n".join(chat_history[-6:]) + "\n" if chat_history else ""

    # Build final prompt
    full_prompt = base_persona + examples_text + recent_chat + f"Seeker: {user_input}\nClaire:"
    return full_prompt

# ✨ Generate Claire's answer
def generate_Claire_response(user_input, llm, max_length=150):
    if "Claire, tarot" in user_input.lower():
        return "Ah, I knew you'd return. Shall we tumble back into mystery together?"

    prompt = build_Claire_prompt(user_input, chat_history)

    try:
        response = llm(
            prompt,
            max_tokens=max_length,
            temperature=0.75,
            top_p=0.9,
            top_k=40,
            repeat_penalty=1.1,
            stop=["Seeker:", "Claire:"],
            echo=False
        )

        raw_output = response['choices'][0]['text'].strip()

        # Clean any hallucinated speaker tags
        def sanitize(text):
            for tag in ["User:", "Claire:", "You:", "Seeker:"]:
                text = text.replace(tag, "")
            return text.strip()

        clean_user_input = sanitize(user_input)
        clean_response = sanitize(raw_output)

        # Update chat history
        chat_history.append(f"Seeker: {clean_user_input}")
        chat_history.append(f"Claire: {clean_response}")

        if len(chat_history) > 12:
            chat_history[:] = chat_history[-12:]

        return clean_response

    except Exception as e:
        return f"[Error generating response: {e}]"

# 🛠️ Show status/debug
def show_system_status(llm):
    test_prompt = build_Claire_prompt("status check", chat_history)
    print("System Status:")
    print(f"- Chat history length: {len(chat_history)} messages")
    print(f"- Model loaded: {'Yes' if llm else 'No'}")
    print("Prompt preview:")
    print("-" * 40)
    print(test_prompt[:400] + "..." if len(test_prompt) > 400 else test_prompt)
    print("-" * 40)

# 🧹 Clear session
def reset_session():
    global chat_history
    chat_history = []
    print("A new chapter begins. 🌀")

# 🌕 Main loop
def main():
    print("Launching Claire, your intuitive Tarot and Lenormand reader...")
    llm = initialize_model()
    if not llm:
        return

    print("\nClaire offers spiritual symbolism, gentle insight, poetic depth.")
    print("Type your question. Commands: 'exit', 'reset', 'status'.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Claire: Until next time. Stay curious.🔮")
            break
        elif user_input.lower() == "reset":
            reset_session()
            continue
        elif user_input.lower() == "status":
            show_system_status(llm)
            continue

        reply = generate_Claire_response(user_input, llm)
        print(f"Claire: {reply}\n")

if __name__ == "__main__":
    main()
