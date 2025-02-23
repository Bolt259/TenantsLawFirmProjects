import os
import json
import requests
from typing import Any, List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_tokens() -> Optional[Dict[str, Any]]:
    """Load tokens from a file."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as file:
            return json.load(file)
    return None

TOKEN_FILE = 'tokens.json'
tokens = load_tokens()

# Clio API credentials
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
token_url = 'https://app.clio.com/oauth/token'
base_api_url = 'https://app.clio.com/api/v4'

'''# Function to list files
def list_files(access_token: str) -> List[Dict[str, Any]]:
    api_url = f'{base_api_url}/documents'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()  # Raise HTTPError for bad responses

    return response.json().get('data', [])
'''

# $$$
# #### HAVE GPT MAKE FRAMES FOR DIFFERENT FUNCTIONS GET POST PUT ETC THEIR FILES IN ORGANIZED WAYS #####
# $$$

# function to list all types of categories
def list_category(access_token: str, category: str) ->List[Dict[str, Any]]:
    api_url = f'{base_api_url}/{category}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()  # Raise HTTPError for bad responses

    return response.json().get('data', [])

def list_clients(access_token: str) -> List[Dict[str, Any]]:
    api_url = f'{base_api_url}/contacts'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()  # Raise HTTPError for bad responses

    clients = response.json().get('data', [])
    
    # Extract address information
    for client in clients:
        addresses = client.get('addresses', [])
        client['addresses'] = addresses

    return clients

# def address

def list_templates(access_token: str):
    api_url = "https://grow.clio.com/api/v1/templates/118918/download"  # Hypothetical URL
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()  # Raises an error for bad HTTP responses
    
    # Save the template as a file
    with open("template_output.txt", "wb") as file:
        file.write(response.content)

    templates = response.json().get('data', [])

    # Print each template's name
    for template in templates:
        print(f"Template Name: {template['name']}")


'''# Function to list matters
def list_matters(access_token: str) -> List[Dict[str, Any]]:
    api_url = f'{base_api_url}/matters'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()  # Raise HTTPError for bad responses
    
    return response.json().get('data', [])
'''
# Function to create a folder
def create_folder(access_token: str, name: str, parent_id: Optional[str] = None) -> Dict[str, Any]:
    api_url = f'{base_api_url}/folders'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    folder_data = {
        'name': name,
        'parent_id': parent_id
    }
    
    response = requests.post(api_url, headers=headers, json=folder_data)
    response.raise_for_status()  # Raise HTTPError for bad responses
    
    return response.json().get('data')

# Function to move file to folder
def move_file_to_folder(access_token: str, file_id: str, folder_id: str) -> None:
    api_url = f'{base_api_url}/files/{file_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    file_data = {
        'folder_id': folder_id
    }
    
    response = requests.put(api_url, headers=headers, json=file_data)
    response.raise_for_status()  # Raise HTTPError for bad responses

'''# Function to organize files by matter name
def organize_files_by_matter(access_token: str) -> None:
    files = list_files(access_token)
    matters = list_matters(access_token)
    
    # Create a dictionary of matter names and their corresponding folder IDs
    matter_folders = {}
    for matter in matters:
        matter_name = matter['display_number'] + ' - ' + matter['description']
        
        # Check if the folder already exists
        existing_folder = next((f for f in list_files(access_token) if f['name'] == matter_name and f['type'] == 'folder'), None)
        if existing_folder:
            matter_folders[matter_name] = existing_folder['id']
        else:
            # Create a new folder for the matter
            new_folder = create_folder(access_token, matter_name)
            matter_folders[matter_name] = new_folder['id']
    
    # Move files to their corresponding matter folders
    for file in files:
        matter_name = file['matter']['display_number'] + ' - ' + file['matter']['description']
        if matter_name in matter_folders:
            move_file_to_folder(access_token, file['id'], matter_folders[matter_name])'''

###
def get_custom_fields(access_token, matter_id):
    api_url = f"https://app.clio.com/api/v4/matters/{matter_id}/custom_fields"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()  # Check for errors

    custom_fields = response.json().get('data', [])
    for field in custom_fields:
        field_name = field.get('name')
        field_value = field.get('value')
        print(f"Custom Field: {field_name}, Value: {field_value}")

# Function to retrieve the list of all matters
def get_all_matters(access_token):
    api_url = "https://app.clio.com/api/v4/matters"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Fetching all matters
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    return response.json().get('data', [])

# Function to retrieve custom fields for a specific matter
def get_custom_fields_for_matter(access_token, matter_id):
    api_url = f"https://app.clio.com/api/v4/matters/{matter_id}/custom_fields"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        return response.json().get('data', [])

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"No custom fields found for Matter ID: {matter_id}")
        else:
            print(f"HTTP error occurred: {http_err}")
        return []
    except Exception as err:
        print(f"An error occurred: {err}")
        return []
    
    
# Main function to get the 'Subject Property Address' custom field for all matters
def get_subject_property_address_for_all_matters(access_token):
    matters = get_all_matters(access_token)

    for matter in matters:
        matter_id = matter.get('id')
        matter_name = matter.get('description')

        custom_fields = get_custom_fields_for_matter(access_token, matter_id)
        
        for field in custom_fields:
            field_name = field.get('name')
            # print(f"Field: {field_name}")
            if field_name == 'Subject Property Address':
                field_value = field.get('value')
                print(f"Matter: {matter_name} (ID: {matter_id}), Subject Property Address: {field_value}")
                break   # Stop checking after finding the desired field

# Main script
try:
    access_token = tokens['access_token']
    
    files = list_category(access_token, 'documents')
    matters = list_category(access_token, 'matters')
    contacts = list_clients(access_token)
    users = list_category(access_token, 'users')
    activities = list_category(access_token, 'activities')
    
    # custom_fields = get_custom_fields(access_token, '1327877119')
    get_subject_property_address_for_all_matters(access_token)
    
    # list_templates(access_token)
        
    # for contact in contacts:
    #     print(f"\nClient Name: {contact['name']}, Addresses: {contact['addresses']}")
        
    # for activity in activities:
    #     print("\nActivity Metadata:")
    #     for key, value in activity.items():
    #         print(f"{key}: {value}")
    #         print("-" * 40)  # Separator between files
        
    # for file in files:
    #     # print("\nFile Metadata:")
    #     for key, value in file.items():
    #         print(f"{key}: {value}")
    #     print("-" * 40)  # Separator between files
        
    # for matter in matters:
    #     print("\nMatter Metadata:")
    #     for key, value in matter.items():
    #         print(f"{key}: {value}")
    #     print("-" * 40)  # Separator between matters


    # organize_files_by_matter(access_token)
    # print("Files organized successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
