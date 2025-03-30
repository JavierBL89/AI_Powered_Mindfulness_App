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

            console.log(`Button clicked: ${button.dataset.tool}`);
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
                    console.log(`${button.dataset.tool} content loaded`);
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

});
