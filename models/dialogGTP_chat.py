import requests
import sys
import os

from dotenv import load_dotenv
load_dotenv()  # ⬅️ This loads your .env values

from content_scraper.content_scraper import fetch_content_from_urls
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

# Add the project root directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

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

        # Send prompt to Hugging Face API
        hf_response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
        hf_result = hf_response.json()

        # Extract the generated response
        if isinstance(hf_result, dict) and "generated_text" in hf_result:
            return jsonify({"status": "success", "response": hf_result["generated_text"]})
        else:
            return jsonify({"status": "error", "message": "Failed to get response", "raw": hf_result}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)