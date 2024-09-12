import os
import json
import requests
from typing import Any, List, Dict, Optional

def load_tokens(token_file) -> Optional[Dict[str, Any]]:
    """Load tokens from a file."""
    if os.path.exists(token_file):
        with open(token_file, 'r') as file:
            return json.load(file)
    return None

def create_new_lead(access_token: str, lead_token: str, first_name: str, last_name: str, email: str, phone: str, message: str, source_url: str) -> dict:
    """_summary_
    Creates new lead on Clio Grow

    Parameters:
    - lead_token (str): lead capture token for authentication
    - first_name (str): First name of the lead
    - last_name (str): Last name of the lead
    - email (str): Email address of the lead
    - phone (str): Phone number of the lead
    - message (str): Message associated with the lead
    - source_url (str): Source URL of the lead

    Returns:
    - dict: Response from the Clio Grow API
    """
    # Define the API endpoint for submitting a new lead
    api_url = "https://grow.clio.com/inbox_leads"
    
    # Prepare the headers and data payload for the request
    headers = {
        'Authorization': f'Bearer {access_token}',  # Authorization added
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }    
    # Data for the new lead
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "message": message,
        "source_url": source_url,
        "inbox_lead_token": lead_token
    }
    
    # Make the POST request to submit the lead
    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for any non-2xx status codes
        return response.json()  # Return the JSON response if successful
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return {"error": str(http_err)}
    except Exception as err:
        print(f"An error occurred: {err}")
        return {"error": str(err)}


token_file = 'tokens.json'
tokens = load_tokens(token_file)

# Main script
try:
    access_token = tokens['access_token']
    lead_token = "8f4adeb9621f33d5b00860aeedafbeb6"      # lead capture token found in Clio Grow Settings > Integrations > Discover > Lead Capture
    new_lead_response = create_new_lead(
        access_token=access_token,
        lead_token=lead_token,
        first_name="Paul",
        last_name="Atreides",
        email="muadib@example.com",
        phone="1234567890",
        message="I need legal advice regarding a land dispute, my landlord Baron Vladimir Harkonnen is assaulting my people and my planet.",
        source_url="https://example.com/contact"
    )
    print(new_lead_response)

except Exception as e:
    print(f"An error occurred: {e}")
