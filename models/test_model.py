from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the fine-tuned model
model_name_or_path = "trainers/fine_tuned_model"  # Replace with your model path
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
model = AutoModelForCausalLM.from_pretrained(model_name_or_path)

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
