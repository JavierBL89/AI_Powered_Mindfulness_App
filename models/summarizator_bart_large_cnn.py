from flask import Flask, request, jsonify
import torch

# Use a pipeline as a high-level helper
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# Set device (use GPU if available)
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

# Load BART-large model for summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text_to_summarize):
    print("Processing summarization...")
    try:
        if not text_to_summarize:
            return jsonify({"status": "error", "message":"No text provided for summarization"})
        print("Performing summarization...")

        # 🔥 Tokenize text and check length
        tokens = tokenizer.encode(text_to_summarize, return_tensors="pt")
        token_count = tokens.shape[1]
          # 🚨 If input is too long, truncate it
        if token_count > 1000:
            print(f"⚠️ WARNING: Text is too long ({token_count} tokens). Truncating to 1000 tokens.")
            tokens = tokens[:, :1000]  # Keep only the first 1024 tokens
            text_to_summarize = tokenizer.decode(tokens[0], skip_special_tokens=True)


        # Perform summarization
        summary = summarizer(text_to_summarize, min_length=200, max_length=300, do_sample=False)
        if not summary:
            return jsonify({"status": "error", "message": "Summarization failed"}), 500

        return jsonify({"status": "success", "summary": summary[0]['summary_text']})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

app = Flask(__name__)


