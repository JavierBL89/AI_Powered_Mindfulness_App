from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
load_dotenv()  # ⬅️ This loads your .env values

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}


def summarize_text(text_to_summarize):
    print("Processing summarization...")
    try:
        if not text_to_summarize:
            return jsonify({"status": "error", "message":"No text provided for summarization"})
        print("Performing summarization...")
        
        if len(text_to_summarize.split()) > 1000:
            text_to_summarize = " ".join(text_to_summarize.split()[:1000])

        response = requests.post(API_URL, headers=HEADERS, json={"inputs": text_to_summarize})
        result = response.json()

        # Perform summarization
        if isinstance(result, list) and "summary_text" in result[0]:
            return jsonify({"status": "success", "summary": result[0]["summary_text"]})
        else:
            return jsonify({"status": "error", "message": "Failed to summarize", "raw": result}), 500


    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

app = Flask(__name__)


