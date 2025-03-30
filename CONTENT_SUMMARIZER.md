# 📄 Content Summarizer Model

## 🔍 Overview
The **Content Summarizer Model** extracts key insights from textual content, allowing users to quickly grasp essential information from this web app pages or inputted text.

---

## 🎯 Goals
- Summarize **entire web pages** dynamically.
- Summarize **specific sections** on hover.
- Provide **concise, well-structured summaries**.

---

## 🏗️ Model Selection
We use **Facebook's BART-Large-CNN**, a transformer-based model designed for text summarization.

🔹 **Model:** `facebook/bart-large-cnn`
🔹 **Framework:** Hugging Face Transformers
🔹 **Approach:** Extractive & Abstractive Summarization

```python
from transformers import pipeline

# Load Summarizer Model (if locally)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):
    summary = summarizer(text, min_length=30, max_length=300, do_sample=False)
    return summary[0]['summary_text']


# Use Hugging Face API (App aproach)
HF_TOKEN = os.getenv("HF_TOKEN = os.getenv("HUGGING_FACE_TOKEN")")
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

```
---

## 🚀 API Implementation

### **1️⃣ Summarize User-Inputted Text**
#### **Endpoint:** `/api/summarize`
#### **Method:** `POST`

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    text = data.get("text", "")

    if not text.strip():
        return jsonify({"status": "error", "message": "No text provided."})

    summary = summarize_text(text)
    return jsonify({"status": "success", "summary": summary})
```

### **2️⃣ Summarize Web Page Content**
#### **Endpoint:** `/api/summarize_page/<page_name>`
#### **Method:** `POST`

```python
@app.route('/api/summarize_page/<page_name>', methods=['POST'])
def summarize_page(page_name):
    page_content = fetch_latest_content_and_return_python_temp_file(f'{page_name}.html')
    summary = summarize_text(page_content)
    return jsonify({"status": "success", "summary": summary})
```

#### We use web scrapong to extract the html content of the specified page to be summarized
# Use a Temporary File for Better Cleanup: Instead of saving to a fixed file name like web_content.txt, 
# consider using Python’s tempfile module to handle file creation and cleanup automatically:

```python
def fetch_latest_content_and_return_python_temp_file(page_name):
    url = f'https://javierbl89.github.io/Mindfulness-Portfolio-Project-Code-Institute/{page_name}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        content = ' '.join([tag.get_text() for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li'])])

        # Create a temporary file to store the content
        temp_file = tempfile.NamedTemporaryFile(mode="w+", delete=False)
        temp_file.write(content)
        temp_file.seek(0)  # Reset pointer to the beginning of the file
        return temp_file
    else:
        raise Exception(f"Failed to fetch content. Status code: {response.status_code}")
```

---

## 🎨 Frontend Integration

### **🔹 HTML**
```html
<div id="summarizer-container">
    <h3>Summarize Content</h3>
    <textarea id="summarization-input" placeholder="Enter text to summarize..."></textarea>
    <button id="summarize-btn">Summarize</button>
    <p id="summarization-output"></p>
</div>
```

### **🔹 JavaScript**
```js
document.getElementById("summarize-btn").addEventListener("click", () => {
    const textToSummarize = document.getElementById("summarization-input").value;

    fetch("/api/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: textToSummarize })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("summarization-output").textContent = `Summary: ${data.summary}`;
    })
    .catch(error => console.error("Error during summarization:", error));
});
```

---

## 📌 Features to Add Next
✅ **Improved text formatting** (bullet points, line breaks)
✅ **User selection-based summarization**
✅ **Summarization history tracking**

---

## 🚀 Next Steps
1️⃣ **Test API with `curl`**:
```sh
curl -X POST "http://127.0.0.1:5001/api/summarize" \
-H "Content-Type: application/json" \
-d '{"text": "Mindfulness improves well-being by increasing awareness and reducing stress."}'
```

2️⃣ **Enhance summarization UI**
3️⃣ **Optimize for large text inputs**

---

📌 **This document serves as a guide for our Content Summarizer Model and its integration.** 🚀
