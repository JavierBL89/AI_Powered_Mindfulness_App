from flask import Flask, request, jsonify
import os
import requests
from transformers import AutoTokenizer  # ✅ use tokenizer locally

from dotenv import load_dotenv
load_dotenv()  # ⬅️ This loads your .env values

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

# Load tokenizer locally
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")


def truncate_text(text, max_tokens=1000):
    tokens = tokenizer.encode(text, truncation=True, max_length=max_tokens)
    return tokenizer.decode(tokens, skip_special_tokens=True)


def summarize_text(text_to_summarize):
    print("Processing summarization...")
    try:
        if not text_to_summarize:
            return jsonify({"status": "error", "message":"No text provided for summarization"})
        print("Performing summarization...")
        

        truncated_text = truncate_text(text_to_summarize)
        
        data = {
            "inputs": truncated_text,
            "parameters": {
                "min_length": 50,
                "max_length": 300,
                "do_sample": False,
                "max_new_tokens": 300,
            },
            "options": {
                "wait_for_model": True
            }
        }
        response = requests.post(API_URL, headers=HEADERS, json=data)
        if response.status_code != 200:
            print("API call failed:", response.status_code, response.text)
            return jsonify({
                "status": "error",
                "message": "Hugging Face API request failed.",
                "details": response.text
            }), response.status_code
        
        result = response.json()

        # Perform summarization
        if isinstance(result, list) and "summary_text" in result[0]:
            return jsonify({"status": "success", "summary": result[0]["summary_text"]})
        else:
            return jsonify({"status": "error", "message": "Failed to summarize", "raw": result}), 500


    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

app = Flask(__name__)


