# healthbot_handler.py
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

HEALTHBOT_ENDPOINT = os.getenv("AZURE_HEALTHBOT_ENDPOINT")
DIRECT_LINE_SECRET = os.getenv("AZURE_HEALTHBOT_DIRECT_LINE_SECRET")

def get_direct_line_token():
    """Get Direct Line token for Health Bot communication"""
    url = "https://directline.botframework.com/v3/directline/tokens/generate"
    headers = {
        "Authorization": f"Bearer {DIRECT_LINE_SECRET}"
    }
    
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json()["token"]
    else:
        print(f"Error getting Direct Line token: {response.status_code}")
        return None

def send_to_health_bot(user_id, message):
    """Send message to Azure Health Bot and get response"""
    token = get_direct_line_token()
    if not token:
        return "Sorry, I'm having trouble connecting to my knowledge base."
    
    # Start conversation if needed
    conversation_url = "https://directline.botframework.com/v3/directline/conversations"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Get or create conversation
    conversation_response = requests.post(conversation_url, headers=headers)
    if conversation_response.status_code != 201:
        print(f"Error creating conversation: {conversation_response.status_code}")
        return "Sorry, I couldn't establish a connection with my health knowledge base."
    
    conversation_id = conversation_response.json()["conversationId"]
    
    # Send message to bot
    message_url = f"https://directline.botframework.com/v3/directline/conversations/{conversation_id}/activities"
    message_payload = {
        "type": "message",
        "from": {
            "id": user_id
        },
        "text": message
    }
    
    message_response = requests.post(
        message_url, 
        headers=headers,
        json=message_payload
    )
    
    if message_response.status_code != 200:
        print(f"Error sending message: {message_response.status_code}")
        return "Sorry, I couldn't process your message with my health knowledge base."
    
    # Get bot response
    activities_url = f"https://directline.botframework.com/v3/directline/conversations/{conversation_id}/activities"
    
    # Wait briefly and then get response
    import time
    time.sleep(2)  # Allow bot to process and respond
    
    activities_response = requests.get(activities_url, headers=headers)
    if activities_response.status_code == 200:
        activities = activities_response.json()["activities"]
        # Filter for bot responses and get the latest one
        bot_responses = [a for a in activities if a["from"]["id"] == "healthbot"]
        if bot_responses:
            latest_response = bot_responses[-1]
            return latest_response["text"]
    
    return "I didn't receive a response from my health knowledge base."