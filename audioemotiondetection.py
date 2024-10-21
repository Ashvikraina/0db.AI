import requests
import time
# https://api.symbl.ai/v1/conversations/5529586802229248/messages
app_id = "664744707446626a374d793866674a3671687651537775434e3030726f505072"
app_secret = "644b62474a734d336d4c756561654148704f3737506c63446d43374676313437764b666235584b434c5341794173764c3359434762305238436f535345477579"
auth_response = requests.post( 'https://api.symbl.ai/oauth2/token:generate', json={'type': 'application', 'appId': app_id, 'appSecret': app_secret} )
access_token = auth_response.json()['accessToken']
headers = { 'Authorization': f'Bearer {access_token}', 'Content-Type': 'audio/mp3' }
audio_file_path = 'C:/Users/ashvi/machine learning/audioashvik.mp3'
with open(audio_file_path, 'rb') as audio_file:
    response = requests.post( 'https://api.symbl.ai/v1/process/audio', headers=headers, data=audio_file )
if response.status_code == 201:
    info = response.json()
    print(info)
else:
    print("Error",response.text)
conversation=info['conversationId']
time.sleep(4)
# print(conversation)
url = 'https://api.symbl.ai/v1/conversations/{}/messages?sentiment=true'.format(conversation)
headers = { 'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json' }
response = requests.get(url, headers=headers)
if response.status_code == 200:
    messages = response.json()
    print(messages)
else:
    print(response.text)