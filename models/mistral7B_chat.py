
from flask import Flask, request, jsonify
import requests
import os

from dotenv import load_dotenv
load_dotenv()  # ⬅️ This loads your .env values

HUGGING_FACE_TOKEN = os.getenv("HF_TOKEN")

if HUGGING_FACE_TOKEN is None:
    raise ValueError("Missing HF_TOKEN environment variable. Set it before running the app.")

API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
HEADERS = {"Authorization": f"Bearer {HUGGING_FACE_TOKEN}"}

def query_llama(prompt):
    
    #To enhance relevance, consider providing better prompts,
    prompt = f"Answer concisely and factually. Only respond as the bot.:\n\nUser: {prompt}\nBot:"

    data = {"inputs": prompt}
    response = requests.post(API_URL, headers=HEADERS, json=data)
    return response.json()

app = Flask(__name__)


def mistral_chat(request):

    try:
        data = request.get_json()
        user_input = data.get("message", "")

        if not user_input:
            return jsonify({"status": "error", "message": "No message provided"}), 400

        # Get response from LLaMA
        llama_response = query_llama(user_input)
        
        # Extract and format response
        if isinstance(llama_response, list) and len(llama_response) > 0:
            response_text = llama_response[0]["generated_text"]
        else:
            response_text = "I'm not sure what you mean."
        return jsonify({"status": "success", "response": response_text})
    

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
