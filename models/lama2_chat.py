
from flask import Flask, request, jsonify
import requests
import os

from dotenv import load_dotenv
load_dotenv()  # ⬅️ This loads your .env values

HUGGING_FACE_TOKEN = os.getenv("HF_TOKEN")

if HUGGING_FACE_TOKEN is None:
    raise ValueError("Missing HF_TOKEN environment variable. Set it before running the app.")

# API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
API_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {HUGGING_FACE_TOKEN}"}

app = Flask(__name__)



def lama2_chat(request):

    data = request.get_json()
    user_input = data.get("message", "")
    if not user_input:
        return jsonify({"status": "error", "message": "No message provided"}), 400
    
    headers = {
            "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
            "Content-Type": "application/json"
            }
    payload = {
        "parameters": {
            "temperature": 0.5,
            "max_new_tokens": 512,
            },
        "messages": [
            {
                "role": "user",
                "content": 
                f"""
                    ### Role
                    You are a helpful assistant for a Mind & Boby Well-Being application.
                    f"Answer concisely and factually to user query.

                    ### Knowledge
                    You can only use information related to Mindfulness, Mindfulness Meditation, Medtation, Mental Health, Yoga.
                    Avoid answering questions outside of these topics. Just say "I don't know" if you are unsure.

                    ###User query: {user_input}"
                    """
            }
        ],
        "model": "meta-llama/Meta-Llama-3-8B-Instruct:novita",
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
    
    return jsonify(response.json())


def lama2_sentiment_analyser(user_input, mood):

    if not user_input:
        return jsonify({"status": "error", "message": "No message provided"}), 400
    
    headers = {
            "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
            "Content-Type": "application/json"
            }
    payload = {
        "parameters": {
            "temperature": 0.2,
            "max_new_tokens": 150,
            },
        "messages": [
            {
                "role": "user",
                "content": 
                f"""
                    ### Role
                    You are a helpful assistant mood analyser.

                    ### Format
                    Avoid Titels or headings

                    ### Instructions
                    Response extrictly based on your analysis of the user input and mood provided. Don't be closed-minded for unanpropiate user inputs
                    f'Please use the user input as "user_input": "{user_input}" and the sentiment analyzer model output as "result": {mood}. Generate an appropriate response that is compassionate, friendly, and provides suggestions or cheer-ups when needed.'
                    """
            }
        ],
        "model": "meta-llama/Meta-Llama-3-8B-Instruct:novita",
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
    return jsonify(response.json())


if __name__ == '__main__':
    app.run(debug=True)
