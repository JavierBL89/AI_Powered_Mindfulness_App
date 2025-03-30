// main.js (or wherever you need to use it)
import { useChatBot } from './chatbot.js';
import { useSummarizator } from './summarizator.js';

// ADD EventListeners to AI Tool Button
document.addEventListener('DOMContentLoaded', function () {
    // AI tools buttons
    const aiToolsBtn = document.getElementById('ai-tools-main-btn');
    const aiToolsContainer = document.getElementById('ai-tools-container');
    aiToolsBtn.addEventListener('click', () => {
        aiToolsContainer.classList.toggle('expanded');
    });

    // Add event listeners to all AI tool buttons
    const toolButtons = document.querySelectorAll('.ai-tool-btn');
    const interactionContainer = document.getElementById('ai-interaction-container');

    toolButtons.forEach(button => {
        button.addEventListener('click', function () {

            aiToolsContainer.classList.toggle('expanded'); // close 'ai-tools-container

            interactionContainer.classList.remove('ai-interaction-container-hidden'); // open tool interaction container

            fetch(`/load_tool_template/${button.dataset.tool}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.text();
                })
                .then(html => {
                    interactionContainer.innerHTML = html;
                    if (button.dataset.tool === "chatbot") {
                        // Scroll to top when clicking the button
                        scrollUp();
                        useChatBot().sendMessage();
                    }
                    if (button.dataset.tool === "summarize_page") {
                        useSummarizator().summarizePageContent();
                    }
                })
                .catch(error => {
                    console.error('Error loading template:', error);
                });


        });
    });


    // Scroll to top when clicking the button
    const scrollUp = ()=>{
            window.scrollTo({
                top: 0,
                behavior: 'smooth' // Smooth scrolling effect
            });
        };


       /**
        * The function `setupEnterKeyListener` sets up an event listener for the Enter key on a
        * specified input field and triggers a callback function when Enter is pressed.
        * @param inputId - The `inputId` parameter is the id of the input field to which you want to
        * attach the Enter key listener.
        * @param callback - The `callback` parameter in the `setupEnterKeyListener` function is a
        * function that will be triggered when the Enter key is pressed in the input field. You can
        * pass any function as the `callback` parameter, and it will be executed when the Enter key is
        * pressed.
        * @param [allowMultiline=false] - The `allowMultiline` parameter in the `setupEnterKeyListener`
        * function is a boolean flag that determines whether the Enter key should create a new line in
        * the input field when pressed along with the Shift key. If `allowMultiline` is set to `true`,
        * pressing Enter with Shift will create
        * @returns ⚠️ Input field with id="inputId" not found
        */
        function setupEnterKeyListener(inputId, callback, allowMultiline = false) {
            const inputField = document.getElementById(inputId);
            if (!inputField) {
                console.warn(`⚠️ Input field with id="${inputId}" not found`);
                return;
            }
        
            inputField.addEventListener('keypress', function (event) {
                if (event.key === 'Enter') {
                    if (allowMultiline && event.shiftKey) {
                        // Allow new line
                        return;
                    }
                    event.preventDefault();
                    callback(); // Trigger the function passed
                }
            });
        }
});
