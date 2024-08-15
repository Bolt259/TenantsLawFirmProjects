#jfri
import os
import json
import requests
from msal import ConfidentialClientApplication
from docx import Document
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TENANT_ID = os.getenv('TENANT_ID')
DRIVE_ID = os.getenv('DRIVE_ID')
ITEM_ID = os.getenv('ITEM_ID')

# FUNCTIONS
##################################################################################################################################################################
def authenticate_graph_api():
    """Authenticate with Microsoft Graph API."""
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET,
    )
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" in result:
        return result["access_token"]
    else:
        print(result.get("error"))
        print(result.get("error_description"))
        raise Exception("Authentication failed")

def upload_to_onedrive(file_path, item_id, access_token):
    """Upload a file to OneDrive."""
    upload_endpoint = f"https://graph.microsoft.com/v1.0/drives/{DRIVE_ID}/items/{item_id}/content"
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    }
    with open(file_path, 'rb') as file:
        response = requests.put(upload_endpoint, headers=headers, data=file)
        response.raise_for_status()
        print("File uploaded successfully")

def publish_word_doc(template_path, replacements, output_path, item_id):
    """Replace placeholders in a Word document and upload it to OneDrive."""
    # Authenticate with Microsoft Graph API
    access_token = authenticate_graph_api()

    # Load and modify the document
    document = Document(template_path)
    document = replace_placeholders(document, replacements)

    # Save the modified document
    document.save(output_path)

    # Upload the modified document to OneDrive
    upload_to_onedrive(output_path, item_id, access_token)
    
# Replace placeholders in the document
def replace_placeholders(doc, replacements):
    for paragraph in doc.paragraphs:
        for placeholder, replacement in replacements.items():
            if placeholder in paragraph.text:
                paragraph.text = paragraph.text.replace(placeholder, replacement)
    return doc

# Define replacements dynamically
def get_replacements():
    with open('replacements.json', 'r') as file:
        replacements = json.load(file)
    
    return replacements 
##################################################################################################################################################################

# Initialize the MSAL confidential client
app = ConfidentialClientApplication(
    CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{TENANT_ID}",
    client_credential=CLIENT_SECRET,
)

# Acquire an access token for the Graph API
result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

if "access_token" in result:
    access_token = result["access_token"]
else:
    print(result.get("error"))
    print(result.get("error_description"))
    exit(1)


