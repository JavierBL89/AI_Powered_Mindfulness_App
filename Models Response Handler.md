# 📌 Response Handling Functions

## 🌜 Overview
This module contains functions that process responses from different AI models integrated into the **Mindfulness App**. It ensures responses are clean, formatted properly, and presented with a typing effect for a smooth user experience.

### 📌 Functions Covered:
- `handleChatBotResponse(data)`
- `handleSummarizatorResponse(data)`
- `handleSentimentAnalizerResponse(data)`
- `typeResponse(responseDiv, responseText, speed)`

---

## 🚀 Functions Breakdown

### 1️⃣ **handleChatBotResponse(data)**
Extracts and formats responses received from the chatbot model.

#### **Process**
1. Extracts the response string from `data.response`.
2. Splits the response to remove unnecessary user input portions.
3. Formats the response:
   - Adds line breaks before numbered steps (e.g., `1.`, `2.`, `3.`).
   - Adds line breaks after punctuation (`!`, `?`) if followed by an uppercase letter.

#### **Code**
```javascript
export const handleChatBotResponse = (data) => {
    let fullResponse = data.response;
    let botResponse = fullResponse.split("Bot:")[1]?.trim();  // Extract bot response
    botResponse = botResponse.split("User:")[0].trim();  // Remove user portion

    // Formatting adjustments
    botResponse = botResponse.replace(/(\d\.\s)/g, '\n$1');
    botResponse = botResponse.replace(/([!?])\s+(?=[A-Z])/g, '$1\n');

    return botResponse;
}
```

---

### 2️⃣ **handleSummarizatorResponse(data)**
Processes the summarizer model's response to ensure clear formatting.

#### **Process**
1. Extracts the summary response.
2. If no summary is received, logs an error and returns a default message.
3. Formats text for readability:
   - Adds line breaks before numbered lists.
   - Adds line breaks after punctuation when needed.

#### **Code**
```javascript
export const handleSummarizatorResponse = (data) => {
    let botResponse = data;
    if (!botResponse) {
        console.error("Error: No summary received.");
        return "No summary available.";
    }
    
    // Formatting improvements
    botResponse = botResponse.replace(/(\d\.\s)/g, '\n$1');
    botResponse = botResponse.replace(/([!?])\s+(?=[A-Z])/g, '$1\n');

    return botResponse;
}
```

---

### 3️⃣ **handleSentimentAnalizerResponse(data)**
Extracts and formats responses from the sentiment analysis model.

#### **Process**
1. Extracts the generated response from `data[0]?.generated_text`.
2. Splits the response to remove unnecessary text, keeping only the bot's message.
3. Formats for readability using:
   - Line breaks before numbered lists.
   - Line breaks after punctuation.

#### **Code**
```javascript
export const handleSentimentAnalizerResponse = (data) => {
    let botResponse = data[0]?.generated_text || ""; // Extract text safely
    botResponse = botResponse.split("Bot:")[1]?.trim() || botResponse;  // Extract bot response

    // Formatting for readability
    botResponse = botResponse.replace(/(\d\.\s)/g, '\n$1');
    botResponse = botResponse.replace(/([!?])\s+(?=[A-Z])/g, '$1\n');

    return botResponse;
}
```

---

### 4️⃣ **typeResponse(responseDiv, responseText, speed)**
Creates a **typing effect** for chatbot responses, simulating real-time text entry.

#### **Process**
1. Loops through the response string, adding one character at a time.
2. If a newline (`\n`) is detected, inserts a `<br>` tag instead.
3. Adjusts typing speed using the `setTimeout` function.

#### **Code**
```javascript
export const typeResponse = (responseDiv, responseText, speed = 30) => {
    let index = 0;

    const typeChar = () => {
        if (index < responseText.length) {
            if (responseText.charAt(index) === '\n') {
                responseDiv.innerHTML += '<br>';  // Insert a line break
            } else {
                responseDiv.innerHTML += responseText.charAt(index);  // Append character
            }
            index++;
            setTimeout(typeChar, speed);
        }
    };

    typeChar();  // Start the typing effect
};
```

---

## ✅ Summary
This module ensures that:
- Responses from different AI models are properly extracted and formatted.
- Chatbot responses are structured with better readability.
- Summaries are clearly displayed.
- Sentiment analysis responses are correctly extracted.
- The **typing effect** enhances user interaction.

---

## 📌 Next Steps
🔹 Improve **multi-turn conversation handling** in the chatbot response.  
🔹 Optimize sentiment analysis formatting for **multi-class emotions**.  
🔹 Enhance typing speed adaptation based on **response length**.  

---

🔗 **This documentation explains how AI-generated responses are handled and displayed efficiently!** 🚀

