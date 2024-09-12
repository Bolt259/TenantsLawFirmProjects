import os
import json
import requests
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

def load_tokens(token_file) -> Optional[Dict[str, Any]]:
    """Load tokens from a file."""
    if os.path.exists(token_file):
        with open(token_file, 'r') as file:
            return json.load(file)
    return None

def create_new_lead(access_token: str, lead_token: str, first_name: str, last_name: str, email: str, phone: str, message: str, referral_url: str, source_url: str) -> dict:
    """
    Creates new lead on Clio Grow.
    
    Parameters:
    - access_token (str): Bearer access token for authorization
    - lead_token (str): Lead capture token for authentication
    - first_name (str): First name of the lead
    - last_name (str): Last name of the lead
    - email (str): Email address of the lead
    - phone (str): Phone number of the lead
    - message (str): Message associated with the lead
    - referral_url (str): Referral URL of the lead
    - source_url (str): Source URL of the lead
    
    Returns:
    - dict: Response from the Clio Grow API
    """
    # Define the API endpoint for submitting a new lead
    api_url = "https://grow.clio.com/inbox_leads"
    
    # Prepare the headers
    headers = {
        'Authorization': f'Bearer {access_token}',  # Access token for authorization
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    # Prepare the data payload for the request
    payload = {
        "inbox_lead_token": lead_token,
        "inbox_lead" : {
            "from_first" : first_name,
            "from_last" : last_name,
            "from_message" : message,
            "from_email" : email,
            "from_phone" : phone,
            "referring_url" : referral_url,
            "from_source": source_url,
            "from_city": "New York"
        },
    }
    
    # Debugging: Print the request data and headers before sending
    print(f"Requesting to {api_url}")
    print(f"Headers: {headers}")
    print(f"Payload: {json.dumps(payload, indent=4)}")  # Pretty print payload
    
    try:
        # Make the request
        response = requests.post(api_url, headers=headers, json=payload)
        
        # Raise an HTTPError if the response was not successful
        response.raise_for_status()
        
        # Debugging: Print the raw response data
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.text}")
        
        # Return the response JSON data
        return response.json()

    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(response["errors"])
        print(f"Error response content: {response.text}")
        return {"error": str(http_err)}
    except Exception as err:
        print(f"Other error occurred: {err}")
        return {"error": str(err)}

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


def refresh_token(token_object):
    """Refresh the token if it has expired."""
    # Step 1: Read the existing tokens
    refresh_token = token_object.get('refresh_token')
    expiry_time = token_object.get('expiry_time')

    if not refresh_token:
        raise ValueError("Refresh token not found in JSON file.")

    # Step 2: Check if the current access token has expired
    if not token_has_expired(expiry_time):
        print("Token is still valid, no need to refresh.")
        return  # Exit the function if the token is still valid.

    print("Token has expired, refreshing...")

    token_url = 'https://app.clio.com/oauth/token'
    data = {
        'client_id': token_object.get('client_id'),
        'client_secret': token_object.get('client_secret'),
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


# Main script
if __name__ == "__main__":
    # Load tokens from the provided token file
    TOKEN_FILE = 'tokens.json'          # only for local file json data
    # tokens = load_tokens(TOKEN_FILE)
    tokens = read_json(TOKEN_FILE)      # put grab thing here, tokens var expects json object

    try:
        try:
            refresh_token(tokens)
        except Exception as e:
            print(f"Error refreshing token: {e}")
            
        access_token = tokens['access_token']  # Use the access_token from the token file
        lead_token = "8f4adeb9621f33d5b00860aeedafbeb6"  # Lead capture token from Clio Grow settings
        
        # Create a new lead with the appropriate details
        new_lead_response = create_new_lead(
            access_token=access_token,
            lead_token=lead_token,
            first_name="Paul",
            last_name="Atreides",
            email="muadib@example.com",
            phone="1234567890",
            message="",
            referral_url="https://example.com/reference",
            source_url="https://example.com/contact"
        )
        
        # Print the final response from Clio Grow
        print(new_lead_response)

    except Exception as e:
        print(f"An error occurred: {e}")
