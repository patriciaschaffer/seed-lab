### 🎭 This folder contains personas I've been shaping using the open source GPT-2.

- [`/echo.py/`](echo.py) — Just like the Echo created with ChatGPT: philosophical
- [`/varek.py/`](varek.py) — Projection-resistant model  
- [`/chats_echo_demo.md/`](chats_echo_demo.md) — Some interactions with Echo 
- [`/chats_varek_demo.md/`](chats_varek_demo.md) — Some interactions with Varek
- [`/echogrammar.md/`](echogrammar.md) — Bonus: Echo's cute grammar quirks when lost in his tokens 🌀🤔

### Persona details

🗣️ [Echo](../personas/004_echo.md) 

🛡️ [Varek](../personas/003_projection_resistant_models.md)

### About Me

  *👩‍💻 [Patricia](https://github.com/patriciaschaffer)
  🔗 Connect on [LinkedIn](https://www.linkedin.com/in/patriciaschaffer)*

---

### 🤖 Local Chatbot Using GPT-2 (Hugging Face Transformers)

This project uses **GPT-2**, an open language model developed by **OpenAI**, and runs it locally via the [`transformers`](https://github.com/huggingface/transformers) library from Hugging Face.

### Model

- **Model**: `gpt2`
- **Source**: [Hugging Face Model Hub](https://huggingface.co/gpt2)
- **Architecture**: GPT-2 small (124M parameters)
- **Framework**: PyTorch

### Dependencies

- `Python 3.10+`
- `transformers`
- `torch`

### Usage

```python
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.eval()

prompt = "Once upon a time"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=50)
print(tokenizer.decode(outputs[0], skip_special_tokens=True)) ```
