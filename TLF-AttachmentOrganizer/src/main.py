import os
import json
import requests
import base64
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TENANT_ID = os.getenv('TENANT_ID')
USER_ID = os.getenv('OUTLOOK_EMAIL')
OUTLOOK_PASSWORD = os.getenv('OUTLOOK_PASSWORD')

# Initialize the MSAL confidential client
app = ConfidentialClientApplication(
    CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{TENANT_ID}",
    client_credential=CLIENT_SECRET,
)

# Acquire an access token for the Graph API
result = app.acquire_token_for_client(
    scopes=["https://graph.microsoft.com/.default"])

if "access_token" in result:
    access_token = result["access_token"]
else:
    print(result.get("error"))
    print(result.get("error_description"))
    exit(1)

# Define the endpoint and headers
# endpoint = "https://graph.microsoft.com/v1.0/me/messages"
endpoint = f"https://graph.microsoft.com/v1.0/users/{USER_ID}/messages"
headers = {
    'Authorization': 'Bearer ' + access_token,
    'Content-Type': 'application/json'
}

# Define directory to store attachments
attachments_dir = "attachments"
os.makedirs(attachments_dir, exist_ok=True)

# Function to download and save attachments


def download_attachments(message_id):
    attachments_endpoint = f"{endpoint}/{message_id}/attachments"
    attachments_response = requests.get(attachments_endpoint, headers=headers)
    attachments = attachments_response.json().get('value', [])

    for attachment in attachments:
        if attachment['@odata.type'] == '#microsoft.graph.fileAttachment':
            file_name = attachment['name']
            file_content = attachment['contentBytes']
            local_path = os.path.join(attachments_dir, file_name)
            with open(local_path, 'wb') as file:
                file.write(base64.b64decode(file_content))
            print(f"Downloaded attachment: {file_name}")
###


# Get the messages from the inbox
response = requests.get(endpoint, headers=headers)
response.raise_for_status()  # Check for HTTP errors

messages = response.json().get('value', [])

# Debug: print the raw response and messages
print("Raw response JSON:", response.json())
print("Messages:", messages)

# Process the messages
for message in messages:
    print(f"Subject: {message['subject']}")
    if message['hasAttachments']:
        download_attachments(message['id'])
