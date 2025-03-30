import { handleChatBotResponse, typeResponse } from "./handleModelResponse.js";

export const useChatBot = () => {

    const sendMessage = () => {
        const send_query = document.getElementById("chatbot-send");

        if (send_query) {
            send_query.addEventListener('click', function() {
                const user_query = document.getElementById("chatbot-input").value;

                if (!user_query.trim()) return;

                fetch(`/api/chat`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: user_query })
                })
                .then(response => response.json())
                .then(data => {
                    
                    const chatbot_response = handleChatBotResponse(data);  // clean response from model

                    const chatbotBody = document.getElementById("chatbot-body");
                    // Clear previous response before adding a new one
                    chatbotBody.innerHTML = '';
                    // Clear input field after sending
                    document.getElementById("chatbot-input").value = '';

                    // Create a single response element and append it
                    const responseDiv = document.createElement('div');
                    responseDiv.classList.add("chatbot-response");
                    chatbotBody.appendChild(responseDiv);

                    // Apply typing effect
                    typeResponse(responseDiv, chatbot_response);

                })
                .catch(error => {
                    console.error('Error sending query:', error);
                });
            });
        } else {
            console.error("Button with ID 'chatbot-send' not found.");
        }
    };
    
    return { sendMessage };
};
