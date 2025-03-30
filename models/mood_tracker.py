import os
import requests
from flask import jsonify

from dotenv import load_dotenv
load_dotenv()  # ⬅️ This loads your .env values

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/distilbert/distilbert-base-uncased-finetuned-sst-2-english"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}


def mood_analizer(user_input):
    try:
        if not isinstance(user_input, str) or not user_input:
            return jsonify({
                "status": "error",
                "message": "Input must be a non-empty string."
            }), 400

        response = requests.post(API_URL, headers=HEADERS, json={"inputs": user_input})
        result = response.json()

        if isinstance(result, list):
            label = result[0].get("label", "Unknown")
            score = round(result[0].get("score", 0), 4)

            mood_mapping = {
                "POSITIVE": "Happy / Positive",
                "NEGATIVE": "Sad / Negative"
            }
            mood = mood_mapping.get(label, "Neutral")

            return jsonify({
                "status": "success",
                "mood": mood,
                "confidence": score
            })
        else:
            return jsonify({"status": "error", "message": "Unexpected API response", "raw": result}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500