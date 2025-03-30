
## Project Overview

This is a refactored old school project. In fact, this App was my very first coding project built with plain HTML and CSS.
Funnyly enough, it has also become my very first project integrating AI on my self-teaching AI journey.

I turned this basic app into a Full Stack AI Powered Flask Application to provide user with an iteractive AI experience integrating:

- A Chatbot for friendly and supportive interactions
- A page content Summarizer.
- A Sentiment Analizer model that aside from providing negative-posive plain responses, I purposly provide the the user input and model output to the Chatbot to generate a more friendly response.


Therefore the App engage users by leveraging Natural Laguage Processing(NLP) models.

### Original Project Mind&Body-Code-Institute-Project
https://javierbl89.github.io/MINDFULNESS-MEDITATION-Code-Institute-Project/index.html


## Lessons Learned

 It has become an invaluable learning experience:
 
 - Integrating AI into Web Apps by using [Hugging Face](https://huggingface.co) Library.
    - Learned how to use NLP models effectively.
        * Load models
        * Sending Prompts
        * Handling model plain string responses
        * Model's Input/Output limitations
        * Overfitting
    - Handling API Responses: Implemented error handling for AI-driven responses.
    - Web scrapping
    - Retrieval Augmented Generation technique. When user interacts with the chanbot I make the model to browse over the web site when building the propmt along with the user's input. By doing this, I provide context to the model so that it can use the app content along with its topic knowledge for a more accurate response. At the same time, If the web content is ever updated, then the model will have real-time app content.
 
 ### NOTE: I have used ChatGPT all along the way for:
            - Flask integration & templaiting
            - Code Generation
            - Model suggestions
            - Step by step models integration and code
            - Code debbuging
            - Overhall guidance and teaching :>


## Tech Stack

**Backend:**

- Python & Flask (Web Framework) - Web Server & handling API endpoints.
- Jinja for templaiting
- Pandas & BeatifulSoup for data manipulation and visualization
- Hugging Face Transformers (NLP Models) - For AI-driven features.
- Requests (API Calls) - Fetching responses from Hugging Face models.

**Frontend:**

- HTML, CSS, JavaScript - Core structure and styling.
- Bootstrap - For responsive design.
- Vanilla JavaScript - For handling user interactions and making API requests.



### Firstly Planned AI tools integration

 - Chatbot
 - Content Summarizer
 - Sentiment Analizer
 - Voice-based interations (STT)
 - Personal Recommendator



### Finnal AI Models Integrated

- **Chatbot:** HuggingFaceH4/zephyr-7b-beta 
  * Provides conversational support using generative AI.
  * Integrated via Flask API to handle user queries.

- **Summarizer:** facebook/bart-large-cnn
  * Condenses text into brief, coherent summaries.
  * Implemented using the Hugging Face pipeline.

- **Mood Tracker** (Sentiment Analyzer): distilbert/distilbert-base-uncased-finetuned-sst-2-english
  * Classifies user sentiment as Positive or Negative.
  * Used to generate mood-based chatbot responses.



#### 1. Chatbot [Link to .md file](/Chatbot%20Model.md)

Endpoint: server.py /api/chat
Method: POST
Payload: { "message": "Hello! What is mindfulness" }
Response: { "status": "success", "response": "Hi! Mindfulness is a milenary practice... ." }

#### 2. Summarizer [Link to .md file](/Content%Summarizer%Model.md)

Endpoint: server.py /api/summarize_page
Method: POST
Payload: { "text": "Mindfulness is the practice of being present..." }
Response: { "status": "success", "summary": "Mindfulness is about being present..." }

#### 3. Mood Tracker [Link to .md file](/Mood%Tracker.md)

Endpoint: server.py /api/mood_tracker
Method: POST

Payload: { "text": "I have worked 9h today and i feel the day is gonne yet" }

Response: Pass model response to mistral_chat -> { "status": "success", "mood": "Happy / Positive", "confidence": 0.98, "user_input": user_input }
    
    Final generated response -> "bla bla bla..."

**Additionally**

 #### 4. Models Response Handler [Link to .md file](/Models%Response%Handler.md)
  /static/js/handleModelResponse.js contains functions that process responses from different AI models integrated into the **Mindfulness App**. It ensures responses are clean, formatted properly, and presented with a typing effect for a smooth user experience.


[](/static/images/ai_tools.png)


## Project folder Structure

- root_directory/models
    * note: chatGPT3 adn dialogGPT were a falied integration attempt due to propmt input contrains(token fees)

[](/static/images/models_directory.png)


- root_directory/static

    * /js contains front-backend requests and responses handling & UI interation files
    * /video contains home page background video

[](/static/images/static_directory.png.png)


- root_directory/templates

    * root_directory/templates with web site main pages base, header, and footer html templates
    * root_directory/templates/ai_features with ai tools html templates


[](/static/images/static_directory.png.png)



## About

Support and techniques about Mindfulness/Meditation/Yoga
Every page provides an introduccion and definition of what it is about, along with techniques and support on how it should be done accompanied to videos or video links to exercises.

All the content has been copied and pasted away, only been carefully choosen from diferents sources as well as the videos and video links, nothing it's been taken ligthly.


#### Project images

Desktop
[](/static/images/Captura%20de%20pantalla%20(25).png)
[](/static/images/Captura%20de%20pantalla%20(26).png)
[](/static/images/Captura%20de%20pantalla%20(27).png)

Mobile
[](/static/images/Captura%20de%20pantalla%20(30).png)
[](/static/images/Captura%20de%20pantalla%20(31).png)
[](/static/images/Captura%20de%20pantalla%20(32).png)


# Project Estructure

The project is divided in 6 pages:

### Main pages
1. HOME
https://javierbl89.github.io/MINDFULNESS-MEDITATION-Code-Institute-Project/index

2. MINDFULNESS
https://javierbl89.github.io/MINDFULNESS-MEDITATION-Code-Institute-Project/assets/html/mindfulness

3. MINDFULNESS MEDITATION
https://javierbl89.github.io/MINDFULNESS-MEDITATION-Code-Institute-Project/assets/html/mindfulness&meditatio

4. MEDITATION
https://javierbl89.github.io/MINDFULNESS-MEDITATION-Code-Institute-Project/assets/html/meditation

5. YOGA
https://javierbl89.github.io/MINDFULNESS-MEDITATION-Code-Institute-Project/assets/html/yoga

### Sub pages
6. BODY SCAN
https://javierbl89.github.io/MINDFULNESS-MEDITATION-Code-Institute-Project/assets/html/bodyScan


## Developing the project

Plenty of features could be added such as;

1. Sing in page.
2. Profile page.
3. Guided exercises according to levels.
4. Weekly/Monthly Guided exercises for the ones with little spare time or the ones who need some guidance to tel them what to do next, etc.
5. Payment page.
6. Related content, such as videos, interviews, books, gear.. etc.
7. Community, set up a community interface for sharing, helping, meetings and live meditations sessions.
8. Shop linked to the page.
