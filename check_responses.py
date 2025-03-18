from flask import Flask, request, jsonify
from whatsapp_api_client_python import API
import json
from datetime import datetime, timedelta

app = Flask(__name__)

# Initialize the WhatsApp API client
# Replace with your actual credentials
API_TOKEN = "YOUR_API_TOKEN"
PHONE_NUMBER_ID = "YOUR_PHONE_NUMBER_ID"
GROUP_ID = "YOUR_GROUP_ID"

api = API.GreenAPI(API_TOKEN, PHONE_NUMBER_ID)

def get_recent_messages(hours_ago=24):
    """
    Get messages from the last 24 hours
    """
    try:
        since_time = datetime.now() - timedelta(hours=hours_ago)
        response = api.serviceMethods.getChatHistory(since_time.timestamp())
        if response.code == 200:
            return response.data
        else:
            print(f"Error getting chat history: {response.code}")
            return []
    except Exception as e:
        print(f"Exception while getting chat history: {str(e)}")
        return []

def approve_member(phone_number):
    """
    Approve a member in the group
    """
    try:
        response = api.groupMethods.approveGroupParticipant(
            GROUP_ID,
            phone_number
        )
        return response.code == 200
    except Exception as e:
        print(f"Error approving member {phone_number}: {str(e)}")
        return False

@app.route('/check-confirmations', methods=['POST'])
def check_confirmations():
    try:
        # Get recent messages
        messages = get_recent_messages()
        
        # Track statistics
        processed_numbers = set()
        approved_count = 0
        
        # Process each message
        for message in messages:
            sender = message.get('senderPhone')
            content = message.get('messageText', '').strip().upper()
            
            # Skip if we've already processed this number or if it's not a CONFIRM message
            if (not sender or 
                sender in processed_numbers or 
                content != 'CONFIRM'):
                continue
                
            # Mark this number as processed
            processed_numbers.add(sender)
            
            # Try to approve the member
            if approve_member(sender):
                approved_count += 1
                print(f"Successfully approved member: {sender}")
            
        return jsonify({
            'status': 'success',
            'messages_processed': len(messages),
            'members_approved': approved_count
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
