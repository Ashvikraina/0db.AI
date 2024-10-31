from flask import Flask, render_template, request, redirect, url_for
import requests
import os
import time
from dotenv import load_dotenv

app_path = os.path.join(os.path.dirname(__file__), '.')
dotenv_path = os.path.join(app_path, '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SYMBL_API_URL"]=os.environ.get("SYMBL_API_URL")

# Symbl.ai API credentials
app_id = os.environ.get("APP_ID")
app_secret = os.environ.get("APP_SECRET")

# Generate Access Token
def get_access_token():
    auth_response = requests.post('https://api.symbl.ai/oauth2/token:generate', 
                                  json={'type': 'application', 'appId': app_id, 'appSecret': app_secret})
    access_token = auth_response.json().get('accessToken', None)
    return access_token

# Process audio with Symbl API
#hi
def process_audio(audio_file_path):
    access_token = get_access_token()
    if not access_token:
        return "Error generating access token"

    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'audio/mp3'}
    with open(audio_file_path, 'rb') as audio_file:
        response = requests.post(app.config["SYMBL_API_URL"], headers=headers, data=audio_file)
    
    if response.status_code == 201:
        info = response.json()
        return info
    else:
        return f"Error processing audio: {response.text}"

# Fetch conversation messages with sentiment
def get_conversation_messages(conversation_id):
    access_token = get_access_token()
    url = f'https://api.symbl.ai/v1/conversations/{conversation_id}/messages?sentiment=true'
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        messages = response.json()
        return messages
    else:
        return f"Error fetching messages: {response.text}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'audio_file' not in request.files:
            return "No file part"
        file = request.files['audio_file']
        if file.filename == '':
            return "No selected file"
        
        if file:
            # Save the uploaded file to the server
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            # Process the audio
            info = process_audio(filepath)
            if 'conversationId' in info:
                conversation_id = info['conversationId']
                time.sleep(4)  # Wait for Symbl.ai to process the audio
                
                # Fetch conversation messages
                messages = get_conversation_messages(conversation_id)
                return messages
            else:
                return "Error processing audio"
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=bool(os.environ.get("DEBUG",False)))
