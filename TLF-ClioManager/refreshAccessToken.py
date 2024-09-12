import json
import requests
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fileManager import load_tokens

# Load environment variables from .env file
load_dotenv()

TOKEN_FILE = 'tokens.json'
tokens = load_tokens()  # delete htis

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def refresh_token():
    # Step 1: Read the existing tokens
    tokens = read_json(TOKEN_FILE)
    client_id = tokens.get("client_id")
    client_secret = tokens.get("client_secret")
    refresh_token = tokens.get("refresh_token")
    grant_type = tokens.get("grant_type")

    if not client_id:
        raise ValueError("Client_id not found in JSON file.")
    if not client_secret:
        raise ValueError("Client_secret not found in JSON file.")
    if not refresh_token:
        raise ValueError("Refresh token not found in JSON file.")

    token_url = 'https://app.clio.com/oauth/token'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': grant_type,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Step 2: Request a new access token using the refresh token
    response = requests.post(token_url, data=data, headers=headers)

    # Helpful response message upon error
    if response.status_code != 200:
        raise Exception(f"Failed to refresh access token: {response.text}")
    response.raise_for_status()  # Raise HTTPError for bad responses

    new_tokens = response.json()

    # Step 3: Update the JSON file with the new access token and expiry time
    data['access_token'] = new_tokens.get('access_token')
    # Update if a new refresh token is provided
    data['refresh_token'] = new_tokens.get('refresh_token', refresh_token)
    # Default to 1 hour if not provided
    expires_in = new_tokens.get('expires_in', 3600)
    data['expiry_time'] = (datetime.now(timezone.utc) +
                           timedelta(seconds=expires_in)).isoformat()

    write_json(TOKEN_FILE, data)

    print("Token refreshed and updated in JSON file.")


if __name__ == "__main__":
    try:
        refresh_token()
    except Exception as e:
        print(f"Error refreshing token: {e}")
