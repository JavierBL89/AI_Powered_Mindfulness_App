

export const handleChatBotResponse = (data) => {
        
    // Extract response from API result
    let fullResponse = data.response;
    let botResponse = fullResponse.split("Bot:")[1]?.trim();  // Get text after 'Bot:'
    botResponse = botResponse.split("User:")[0].trim();  // Remove extra user part

    // Add line breaks before numbered steps (e.g., 1. 2. 3.)
    botResponse = botResponse.replace(/(\d\.\s)/g, '\n$1');
    // Add line breaks only after full sentences, avoiding abbreviations
    botResponse = botResponse.replace(/([!?])\s+(?=[A-Z])/g, '$1\n');

    return botResponse;
}


export const handleSummarizatorResponse = (data) => {
    // Extract response from API result
    let botResponse = data;
    if (!botResponse) {
        console.error("Error: No summary received.");
        return "No summary available.";
    }
    
    // Add line breaks before numbered steps (e.g., 1. 2. 3.)
    botResponse = botResponse.replace(/(\d\.\s)/g, '\n$1');
    // Add line breaks only after full sentences, avoiding abbreviations
    botResponse = botResponse.replace(/([!?])\s+(?=[A-Z])/g, '$1\n');

    return botResponse;
}



export const handleSentimentAnalizerResponse = (data) => {
        
    let botResponse = data[0]?.generated_text || ""; // Extract text safely
    // Split the response to get only what comes after "Bot:"
    botResponse = botResponse.split("Bot:")[1]?.trim() || botResponse;

    // Add line breaks before numbered steps (e.g., 1. 2. 3.)
    botResponse = botResponse.replace(/(\d\.\s)/g, '\n$1');
    // Add line breaks only after full sentences, avoiding abbreviations
    botResponse = botResponse.replace(/([!?])\s+(?=[A-Z])/g, '$1\n');

    return botResponse;
}


    /**
     * Typing effect for chatbot response
     * Function to Support Line Breaks
     */
    export const typeResponse = (responseDiv, responseText, speed = 30) => {
        let index = 0;

        const typeChar = () => {
            if (index < responseText.length) {
                // Handle new lines as <br> when a newline character is detected
                if (responseText.charAt(index) === '\n') {
                    responseDiv.innerHTML += '<br>';  // Add HTML line break
                } else {
                    responseDiv.innerHTML += responseText.charAt(index);  // Append character
                }
                index++;
                setTimeout(typeChar, speed);
            }
        };
    
        typeChar();  // Start typing
    };
