# 📌 Mood Tracker Model Documentation

## 🧠 Model Overview
- **Model Name:** `distilbert-base-uncased-finetuned-sst-2-english`
- **Architecture:** DistilBERT (lighter, faster version of BERT)
- **Training Dataset:** Stanford Sentiment Treebank (SST-2)
- **Task:** Sentiment Analysis (Binary Classification: Positive / Negative)
- **Bidirectional Processing:** Understands context from both directions.
- **Optimization:** 40% fewer parameters than BERT while retaining 97% of its accuracy.

---

## 🎯 Use Case: Mood Tracking
### **How It Works**
1. **User Input:** Receives text from journal entries, chatbot interactions, or self-reflection logs.
2. **Tokenization & Preprocessing:** Converts text into tokens and feeds it into the model.
3. **Sentiment Prediction:**
   - **Positive Prediction:** User feels happy, motivated, or uplifted.
   - **Negative Prediction:** User feels sad, stressed, or frustrated.
4. **Mood Trend Analysis:** Tracks emotional patterns over time.
5. **Personalized Feedback:** Suggests meditation, mindfulness exercises, or motivational quotes based on sentiment analysis.

---

## 🚀 Model Integration

## 🏗️ Model Selection
We use **distilbert-base-uncased-finetuned-sst-2-english**, a transformer-based model designed for sentiment amalysis.

🔹 **Model:** `distilbert-base-uncased-finetuned-sst-2-english`
🔹 **Framework:** Hugging Face Transformers
🔹 **Approach:** Text-based sentiment analysis

```python
from transformers import pipeline

# Load model directly
tokenizer = AutoTokenizer.from_pretrained("distilbert/distilbert-base-uncased-finetuned-sst-2-english")
model = AutoModelForSequenceClassification.from_pretrained("distilbert/distilbert-base-uncased-finetuned-sst-2-english")
#Load sentiment analysis model (DistilBERT fine-tuned on SST-2)
mood_analyzer_model = pipeline("text-classification", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

def mood_analizer(user_input):

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
```

---

## 🚀 API Implementation

### **1️⃣ Summarize User-Inputted Text**
#### **Endpoint:** `/api/summarize`
#### **Method:** `POST`

```python
from flask import Flask, request, jsonify

@app.route('/api/mood_tracker', methods=['POST'])
def mood_tracker():
       
    data = request.get_json()  # This extracts JSON data
    user_input = data.get("message", "").strip()
    
    if not isinstance(user_input, str):
            return jsonify({
                "status": "error",
                "message": "Input must be a string."
            }), 400

    if not user_input:
        return jsonify({"status": "error", "message": "No text provided for mood analisis"})
       
    # Perform mood anaylisys
    result_response = mood_analizer(user_input) # Model requires List[str]
    # Convert response to JSON
    result = result_response.get_json()  # Extract JSON data
    
    # Now safely access the 'mood'
    mood = result.get("mood", "Neutral")  # Default to 'Neutral' if not found
    confidence = result.get("confidence", 0.0)  # Default to 0.0 if not found  
    # Create a properly formatted JSON string
    user_input_json = {
    "message": f'Please use the user input as "user_input": "{user_input}" and the sentiment analyzer model output as "result": {mood}. Generate an appropriate response that is compassionate, friendly, and provides suggestions or cheer-ups when needed.'
}
    # Generate a nice reposnose using chatbot from sentiment analizer output
    # Pass the JSON object directly (not jsonify before sending it)
    chatbot_generated_response = query_llama(user_input_json["message"])
    return chatbot_generated_response

```


## 🎨 Frontend Integration

### **🔹 HTML**
```html
<div id="progress-tracker">
    <div id="tracker-panel" class="hidden">
        <h4>How do you feel today?</h4>
        <form id="mood-form">
            <label for="mood">...tell more than just <i>"Fine"</i> or <i> "Sad"</i> !</label>
            <input id="mood"/>
            <button type="button">Log Feeling</button>
        </form>
        <div id="chatbot-body">
            <!-- Progress visualization -->
        </div>
    </div>
</div>
```

### **🔹 JavaScript**
```js
const sendUserFeeling = () => {
    
        const userMood = document.querySelector('#tracker-panel input').value;
        const trackerPanel = document.querySelector('#tracker-panel');
        if (!userMood.trim()) return;
    
        fetch(`/api/mood_tracker`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userMood })
    
        })
            .then(response => response.json())
            .then(data => {
    
                // clean response from model
                const chatbot_response = handleSentimentAnalizerResponse(data);
                const parentElement = document.getElementById('progress-tracker');
    
                // Clear previous response before adding a new one
                parentElement.innerHTML = '';
    
                // Create a single response element and append it
                const responseDiv = document.createElement('div');
                responseDiv.classList.add("mood-chatbot-response");
                parentElement.appendChild(responseDiv);
    
                // Apply typing effect
                typeResponse(responseDiv, chatbot_response);
    
            })
            .catch(error => {
                console.error('Error sending query:', error);
    
            });
    }
```
### **1️⃣ API Endpoint for Mood Tracking**
- **Endpoint:** `/api/mood_tracker`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "text": "I feel really tired and unmotivated today."
  }
  ```
- **Response Example:** (mistral7B.query_llama()) along with user input
  ```json
  {
    "status": "success",
    "sentiment": "negative",
    "confidence": 0.87
  }
  ```

### **2️⃣ Multi-Class Emotion Classification Enhancement**
- Expand beyond binary sentiment to classify:
  - 😊 Joy
  - 😢 Sadness
  - 😡 Anger
  - 😨 Fear
  - 😌 Calmness
  - 🤔 Neutral

- **Approach:** Fine-tune `distilbert-base-uncased` on a multi-class emotion dataset like **GoEmotions**.


### 🔗 References
- [DistilBERT Model](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english)
- [Stanford Sentiment Treebank](https://nlp.stanford.edu/sentiment/)
- [GoEmotions Dataset](https://github.com/google-research/goemotions)  

🎉 **Mood tracking is now AI-powered!** 🚀
