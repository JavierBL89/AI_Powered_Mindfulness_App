import { handleSummarizatorResponse, typeResponse } from "./handleModelResponse.js";

export const useSummarizator = () => {

    const sendMessage = () => {
        const summarizeButton = document.getElementById('summarize-btn');
        summarizeButton.addEventListener('click', function () {
            const textToSummarize = document.getElementById('summarization-input').value;

            fetch('/api/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: textToSummarize })
            })
                .then(response => response.json())
                .then(data => {

                    // Clear input field after sending
                    const chatbotBody = document.getElementById("chatbot-input").value = '';
                    // Clear previous response before adding a new one
                    chatbotBody.innerHTML = '';


                    const chatbot_response = handleChatBotResponse(data.summary);  // clean response from model

                    // Create a single response element and append it
                    const responseDiv = document.createElement('div');
                    responseDiv.classList.add("chatbot-response");
                    chatbotBody.appendChild(responseDiv);

                    // Apply typing effect
                    typeResponse(responseDiv, chatbot_response);
                })
                .catch(error => {
                    console.error('Error during summarization:', error);
                });
        });
    }


    const summarizePageContent = () => {

        const currentUrl = window.location.href;  // Get the current page URL
        const currentPage = currentUrl.split('/').pop(); // Get last part of the URL

        // Clear input field after sending
        const summarizatorBody = document.getElementById("summarizator-body");
        // Clear previous response before adding a new one
        summarizatorBody.innerHTML = '';

        // Create a single response element and append it
        const loadingDiv = document.createElement('div');
        loadingDiv.classList.add("summarizer-response");
        loadingDiv.innerHTML = `<p class="summarizer-loading-text text-center"> Just a few secons while I prepare the text ...</p>`
        summarizatorBody.appendChild(loadingDiv);

        console.log("Current page:", currentPage);  // Debugging

        fetch(`/api/summarize_page/${currentPage}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        })
            .then(response => response.json())
            .then(data => {

                // Ensure the summary exists before processing
                if (!data.summary) {
                    throw new Error("Summary data is missing from the response.");
                }

                // Create a single response element and append it
                summarizatorBody.removeChild(loadingDiv);

                const summarizer_response = handleSummarizatorResponse(data.summary);  // clean response from model

                const responseDiv = document.createElement('div');
                responseDiv.classList.add("summarizer-response");
                // responseDiv.innerHTML = summarizer_response;  // Insert the processed text
                summarizatorBody.appendChild(responseDiv);


                // Apply typing effect
                typeResponse(responseDiv, summarizer_response);
            })
            .catch(error => {
                // If there's an error, remove loading div and show error message
                summarizatorBody.removeChild(loadingDiv);
                summarizatorBody.innerHTML = `<p class="summarizer-error text-center">Oops! Something went wrong. Please try again.</p>`;

                console.error('Error during summarization:', error);
            });
    };

    return { summarizePageContent };
}