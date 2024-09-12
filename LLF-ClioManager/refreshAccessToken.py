import json
import requests
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# DEPRICATED

# Load environment variables from .env file
load_dotenv()

TOKEN_FILE = 'tokens.json'

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def token_has_expired(expiry_time_str):
    """Check if the current token has expired."""
    if not expiry_time_str:
        return True  # If no expiry time is found, assume the token has expired.
    
    expiry_time = datetime.fromisoformat(expiry_time_str)
    current_time = datetime.now(timezone.utc)
    
    # If current time is past the expiry time, return True.
    return current_time >= expiry_time


def refresh_token():
    """Refresh the token if it has expired."""
    # Step 1: Read the existing tokens
    data = read_json(TOKEN_FILE)
    refresh_token = data.get('refresh_token')
    expiry_time = data.get('expiry_time')

    if not refresh_token:
        raise ValueError("Refresh token not found in JSON file.")

    # Step 2: Check if the current access token has expired
    if not token_has_expired(expiry_time):
        print("Token is still valid, no need to refresh.")
        return  # Exit the function if the token is still valid.

    print("Token has expired, refreshing...")

    token_url = 'https://app.clio.com/oauth/token'
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Step 3: Request a new access token using the refresh token
    response = requests.post(token_url, data=data, headers=headers)

    # Helpful response message upon error
    if response.status_code != 200:
        raise Exception(f"Failed to refresh access token: {response.text}")
    response.raise_for_status()  # Raise HTTPError for bad responses

    new_tokens = response.json()

    # Step 4: Update the JSON file with the new access token and expiry time
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
