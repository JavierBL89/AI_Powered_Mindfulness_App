import { handleSentimentAnalizerResponse, typeResponse } from "./handleModelResponse.js";

document.addEventListener("DOMContentLoaded", () => {

    const send_query = document.getElementById("chatbot-send");


    /* Function is responsible for handling the user's input, 
     *   1- Sending it to the server via a POST request to `/api/mood_tracker`
     *   2- Receiving a responsea and processing the response using the `handleSentimentAnalizerResponse` function, 
     *   3- Displaying the response in the chatbot interface with a typing effect using the `typeResponse` function. 
     *      It also clears any previous responses before adding a new one. 
     * @returns METHOS TO BE ABOVE THE OBSERVER METHOD
     */
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

    // wait for the button to be available

    /* Creating a `MutationObserver` instance.
    * This observer is used to monitor changes in the DOM (Document Object Model) of the webpage. 
    * The purpose of this observer is to wait for a specific button element with the ID `mood-form button` to become
    * available in the document.
     */
    const observer = new MutationObserver((mutations, obs) => {

        const submitFeeling = document.querySelector('#mood-form button');

        if (submitFeeling) {
            submitFeeling.closest(addEventListener('click', (event) => {
                if (event.target.matches('#mood-form button')) {
                    sendUserFeeling();
                }
            }));
            obs.disconnect(); // Stop observing once found
        }
    });

    // Start observing the document
    observer.observe(document.body, { childList: true, subtree: true });
});
