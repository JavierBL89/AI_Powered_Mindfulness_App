ChatBot

1. Set Up Hugging Face API Access

Create an account on Hugging Face.
Go to Settings > Access Tokens and generate a new API token with "read" access.
Save the token securely.


2. Install Dependencies
Make sure you have the required Python libraries:

pip install transformers requests torch



PYTHON

Replace YOUR_HF_API_KEY with your actual Hugging Face API Key.
import requests

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
HEADERS = {"Authorization": Bearer YOUR_HF_API_KEY"}

def query_llama(prompt):
    data = {"inputs": prompt}
    response = requests.post(API_URL, headers=HEADERS, json=data)
    return response.json()

# Example question
prompt = "What is mindfulness?"
response = query_llama(prompt)
print(response)


5. Run Your Chatbot

Start your Flask server:

   python <file-name>.py
   
Then, send a POST request to test it:

curl -X POST http://127.0.0.1:5000/chat \
-H "Content-Type: application/json" \
-d '{"message": "What is mindfulness?"}'
