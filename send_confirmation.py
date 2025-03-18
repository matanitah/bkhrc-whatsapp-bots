from whatsapp_api_client_python import API
import json
import os
from datetime import datetime

# Initialize the WhatsApp API client
# Replace with your actual credentials
API_TOKEN = "YOUR_API_TOKEN"
PHONE_NUMBER_ID = "YOUR_PHONE_NUMBER_ID"
API_VERSION = "v17.0"  # Use the latest API version

api = API.GreenAPI(API_TOKEN, PHONE_NUMBER_ID)

def get_unapproved_members(group_id):
    """
    Get list of unapproved members in a WhatsApp group
    """
    try:
        response = api.serviceMethods.getGroupMembers(group_id)
        if response.code == 200:
            members = response.data
            return [member for member in members if not member.get('isApproved', False)]
        else:
            print(f"Error getting group members: {response.code}")
            return []
    except Exception as e:
        print(f"Exception while getting group members: {str(e)}")
        return []

def send_confirmation_message(phone_number):
    """
    Send a confirmation message to a specific phone number
    """
    message = (
        "👋 Hello! This is an automated message from the BK Heights Run Club WhatsApp group.\n\n"
        "To ensure the security and quality of our community, we need to confirm that you are a real person.\n\n"
        "Please respond with 'CONFIRM' to verify your membership.\n\n"
        "If you don't respond within 72 hours, you will be removed from the group.\n\n"
        "Thank you for your understanding! 🙏"
    )
    
    try:
        response = api.sending.sendMessage(phone_number, message)
        if response.code == 200:
            print(f"Confirmation message sent to {phone_number}")
            return True
        else:
            print(f"Error sending message to {phone_number}: {response.code}")
            return False
    except Exception as e:
        print(f"Exception while sending message to {phone_number}: {str(e)}")
        return False

def main():
    # Replace with your actual group ID
    GROUP_ID = "YOUR_GROUP_ID"
    
    print("Starting confirmation message process...")
    
    # Get unapproved members
    unapproved_members = get_unapproved_members(GROUP_ID)
    
    if not unapproved_members:
        print("No unapproved members found.")
        return
    
    print(f"Found {len(unapproved_members)} unapproved members.")
    
    # Send confirmation messages
    success_count = 0
    for member in unapproved_members:
        phone_number = member.get('phoneNumber')
        if phone_number:
            if send_confirmation_message(phone_number):
                success_count += 1
    
    print(f"\nProcess completed!")
    print(f"Successfully sent {success_count} out of {len(unapproved_members)} confirmation messages.")

if __name__ == "__main__":
    main()
