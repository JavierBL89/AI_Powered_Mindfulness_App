from flask import jsonify
# Use a pipeline as a high-level helper
from transformers import pipeline

from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load model directly
tokenizer = AutoTokenizer.from_pretrained("distilbert/distilbert-base-uncased-finetuned-sst-2-english")
model = AutoModelForSequenceClassification.from_pretrained("distilbert/distilbert-base-uncased-finetuned-sst-2-english")

 #Load sentiment analysis model (DistilBERT fine-tuned on SST-2)
mood_analyzer_model = pipeline("text-classification", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")


def mood_analizer(user_input):
    try:
        if not isinstance(user_input, str) or not user_input:
                return jsonify({
                    "status": "error",
                    "message": "Input must be a non-empty string."
                }), 400

        result = mood_analyzer_model(user_input)  

        # **Ensure output format is correct**
        if isinstance(result, list):  # Some Hugging Face pipelines return a list
            result = result[0]  

            mood_label = result.get('label', 'Unknown')
            confidence = round(result.get('score', 4), 4)  # Round confidence score

            # Map to a more user-friendly mood classification
            mood_mapping = {
                "POSITIVE": "Happy / Positive",
                "NEGATIVE": "Sad / Negative"
            }
            mood = mood_mapping.get(mood_label, "Neutral")

            return jsonify({
                "status": "success",
                "mood": mood,
                "confidence": confidence
            })

    except Exception as e:
        print(f"Error: {e}")  # Debugging line
        return jsonify({"status": "error", "message": str(e)}), 500