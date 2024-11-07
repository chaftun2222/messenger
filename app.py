from flask import Flask, request
import requests

app = Flask(__name__)

# Replace with your Page Access Token from Facebook
PAGE_ACCESS_TOKEN = 'EAAOejmPH5n4BOZB3DS3l0dgMZBVW6uF8MMkQZBdezvxNKz6Kbc2vvGZADCODgfi2TIAS73DBGgHAZBn0y4S3hGYMltyW2d5Ca6XHUjL3jRARqegURxuXykjXmYCZAZA6tEhrTYAgA8DGzU8fxZAjJQVj4WUWxFro16NXJ1bMFeYR8kQI664ee8VB8Q0AXD3oPzIZD'


# Your verification token (replace with the same token you used in the Facebook dashboard)
VERIFY_TOKEN = 'my_verify_token'

# Webhook endpoint to receive messages and handle verification
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Facebook verification
        token_sent = request.args.get('hub.verify_token')
        if token_sent == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return 'Invalid verification token', 403

    elif request.method == 'POST':
        # Process the incoming data
        data = request.get_json()
        print("Received data:", data)  # Print incoming data for debugging

        # Handle both real messages and test messages
        if data.get('object') == 'page':
            # Real messages from users
            for entry in data['entry']:
                for messaging_event in entry.get('messaging', []):
                    if 'message' in messaging_event:
                        handle_message_event(messaging_event)

        elif data.get('field') == 'messages':
            # Handle test messages from the Facebook test console
            handle_test_message_event(data['value'])

        return "ok", 200

def handle_message_event(messaging_event):
    """Handle real messages from users."""
    sender_id = messaging_event['sender']['id']
    message_text = messaging_event['message'].get('text', 'No text provided')
    print(f"Message from {sender_id}: {message_text}")
    send_message(sender_id, "Click the button below to fill out our form.")

def handle_test_message_event(test_event):
    """Handle test messages sent from the Facebook test console."""
    sender_id = test_event['sender']['id']
    message_text = test_event['message'].get('text', 'No text provided')
    print(f"Test message from {sender_id}: {message_text}")
    send_message(sender_id, "This is a test response. Click the button below to fill out our form.")

def send_message(recipient_id, message_text):
    """Send a message with a button to the user."""
    url = "https://graph.facebook.com/v13.0/me/messages"
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": message_text,
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": "https://gregarious-mochi-688aa7.netlify.app/",
                            "title": "Open Form",
                            "webview_height_ratio": "tall",
                            "messenger_extensions": True  # Capitalize True
                        }
                    ]
                }
            }
        },
        "access_token": PAGE_ACCESS_TOKEN
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print("Error sending message:", response.text)

# Running the Flask server
if __name__ == '__main__':
    app.run(port=5000)
