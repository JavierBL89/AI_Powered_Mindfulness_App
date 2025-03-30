from flask import Flask, render_template, jsonify, request,abort
import json
import torch
from models.mistral7B_chat import mistral_chat, query_llama
from models.summarizator_bart_large_cnn import summarize_text
from content_scraper.content_scraper import fetch_latest_content_and_return_python_temp_file
from models.mood_tracker import mood_analizer

# Initialize Flask app
app = Flask(__name__)
with app.app_context():
    app.jinja_env.cache = {}


# Home page endpoint
@app.route('/')
def home():
    return render_template('index.html')  # Replace with the actual HTML file name for the homepage

# About page endpoint
@app.route('/bodyScan')
def bodyScan():
    return render_template('bodyScan.html')  # Replace with the actual HTML file name for the About page

# Meditation Practices page endpoint
@app.route('/meditation')
def meditation():
    return render_template('meditation.html')  # Replace with the actual HTML file name for the Practices page

# Contact page endpoint
@app.route('/mindfulness')
def mindfulness():
    return render_template('mindfulness.html')  # Replace with the actual HTML file name for the Contact page

# Contact page endpoint
@app.route('/mindfulness_meditation')
def mindfulnessMeditation():
    return render_template('mindfulness_meditation.html')  # Replace with the actual HTML file name for the Contact page

# Contact page endpoint
@app.route('/yoga')
def yoga():
    return render_template('yoga.html')  # Replace with the actual HTML file name for the Contact page

# Contact page endpoint
@app.route('/aiFeaturesBaseTemplate')
def ai_features_view():
    return render_template('aiFeaturesBaseTemplate.html')  # Replace with the actual HTML file name for the Contact page


# ---------------------------------------------------------

@app.route("/load_tool_template/<tool_name>")
def load_tool_template(tool_name):
  
    templates = { 
        'chatbot': 'chatbot_template.html',
        'summarize_page': 'summarization_template.html',
        'recommendations': 'recommendations_template.html',
        'mood_tracker': 'moodTracker_template.html',
        'voice': 'voiceInteractor_template.html'
    }

    template_name = templates.get(tool_name)
    template_name = f'ai_features/{template_name}'
       
    print(template_name)
    if template_name:
        return render_template(template_name)
    else:
        abort(404)  # Return a 404 error if the tool doesn't exist

# API Endpoint for Chatbot
@app.route('/api/chat', methods=['POST'])
def chatbot():
    
    response = mistral_chat(request)
    return response

# API Endpoint for Content Summarization
@app.route('/api/summarize_page/<page_name>', methods=['POST'])
def summarize_page(page_name):
    try:
        # Fetch the content of the page
        page_content_file = fetch_latest_content_and_return_python_temp_file(f'{page_name}.html')
        page_content = page_content_file.read()
        page_content_file.close()

        # Debugging: Print the retrieved content
        print(f"Retrieved content for {page_name}: {page_content[:200]}...")  # Print only first 200 chars

        # Summarize the fetched content
        summarizator_response = summarize_text(page_content)
        return summarizator_response

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# API Endpoint for Mood Tracking
@app.route('/api/mood_tracker', methods=['POST'])
def mood_tracker():
       
    data = request.get_json()  # This correctly extracts JSON data
    user_input = data.get("message", "").strip()
    print(f"Received text: {user_input}")  # Debugging line
    
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


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)
