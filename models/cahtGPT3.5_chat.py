import openai
import sys
import os

# Add the project root directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from content_scraper.content_scraper import fetch_content_from_urls

from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set your OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Parse JSON request
        data = request.get_json()
        user_input = data.get("message", "")
        
        if not user_input:
            return jsonify({"status": "error", "message": "No message provided"}), 400

    
        try:
            # Fetch website content
            context_dict = fetch_content_from_urls()
            context = " ".join(context_dict.values())  # Combine all content into a single string
            print("Fetched content:")
            print(context)  # Log the combined content

        except Exception as e:
            return jsonify({"status": "error", "message": f"Error fetching context: {str(e)}"}), 500
        
        # Fix: Ensure the context is non-empty before combining it with the user's query
        if not context.strip():
           context = "No relevant context available."
        # Combine context with user query
        prompt = f"Context: {context}\n\nUser: {user_input}\nBot:"

        # Tokenize input
        input_ids = tokenizer.encode(prompt + tokenizer.eos_token, return_tensors="pt")
         # attention_mask not equals to tokenizer.pad_token_id
        attention_mask = (input_ids != tokenizer.pad_token_id).long()  # Generate attention mask

        # Generate response
        chat_history_ids = model.generate(
            input_ids,
            attention_mask=attention_mask,  # Add attention mask
            max_length=5000,
            pad_token_id=tokenizer.eos_token_id,
            temperature=0.7,  # Controls randomness
            top_p=0.9,      # Nucleus sampling
            top_k=50,         # Limits sampling to top-k tokens
            do_sample=True, 
        )

        # Decode response
        response = tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)

        return jsonify({"status": "success", "response": response})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)