

# **Guide to Testing AI Models in the Command Line**

This guide explains how to test a fine-tuned model in the command line using a Python script.

---

## **1. Prerequisites**

### **Install Required Libraries**
Ensure you have the necessary libraries installed in your environment:
```bash
pip install torch transformers datasets
```

### **Prepare the Fine-Tuned Model**
Ensure the model has been fine-tuned and saved. The saved model directory (e.g., `./fine_tuned_model`) should include:
- `pytorch_model.bin` (or equivalent for TensorFlow/Flax).
- `config.json`.
- Tokenizer files (`tokenizer_config.json`, `vocab.json`, `merges.txt`, etc.).

---

## **2. Create a Python Script**

### **File: `test_model.py`**

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the fine-tuned model and tokenizer
model_path = "./fine_tuned_model"  # Replace with your model directory
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

def chat_with_model():
    print("Chatbot is ready! Type 'exit' to quit.")

    # Initialize chat history (optional for continuity)
    chat_history_ids = None

    while True:
        # Get user input
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Tokenize input
        input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")

        # Generate response
        chat_history_ids = model.generate(
            input_ids=input_ids,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id
        )

        # Decode and print response
        bot_response = tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        print(f"Bot: {bot_response}")

if __name__ == "__main__":
    chat_with_model()
```

---

## **3. Run the Script**

Execute the script in the terminal to interact with the model:
```bash
python test_model.py
```

---

## **4. Chat with the Model**

### Example Interaction:
```plaintext
Chatbot is ready! Type 'exit' to quit.
You: What is mindfulness?
Bot: Mindfulness is the ability to be fully present and aware of your surroundings without judgment.
You: Tell me more.
Bot: Mindfulness helps improve focus, reduce stress, and enhance emotional well-being.
You: exit
Goodbye!
```

---

## **5. Troubleshooting**

### **Common Issues**
1. **Model Not Found**:
   - Ensure the `model_path` points to the correct directory containing the saved model files.

2. **Library Not Installed**:
   - Install required dependencies:
     ```bash
     pip install torch transformers
     ```

3. **Python Version Compatibility**:
   - Ensure you're using Python 3.8, 3.9, 3.10, or 3.11.

### **Verify Model Directory Structure**
The `fine_tuned_model` directory should look like this:
```
fine_tuned_model/
    ├── config.json
    ├── pytorch_model.bin
    ├── tokenizer_config.json
    ├── vocab.json
    ├── merges.txt
```

---

## **6. Customize the Script**

### Add Chat History (Optional)
To maintain continuity between questions:
```python
chat_history_ids = model.generate(
    input_ids=input_ids,
    max_length=1000,
    pad_token_id=tokenizer.eos_token_id,
    past_key_values=chat_history_ids
)
```

### Use Pretrained Models
If no fine-tuned model is available, test with a pretrained model:
```python
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
```

---

## **7. FAQ**

### **How to Fine-Tune a Model?**
- Use a script like `topicTrainer.py` to fine-tune and save your model in a directory.

### **Can I Use This for Non-Chatbot Models?**
- Yes! Modify the input/output logic depending on your model type (e.g., text classification, summarization).



curl -X POST http://127.0.0.1:5000/<train-model-endpoint>
