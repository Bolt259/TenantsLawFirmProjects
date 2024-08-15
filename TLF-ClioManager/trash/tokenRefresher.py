# import json
# import os
# import requests
# import time
# from typing import Any, Dict, Optional

# TOKEN_FILE = 'tokens.json'

# def load_tokens() -> Optional[Dict[str, Any]]:
#     """Load tokens from a file."""
#     if os.path.exists(TOKEN_FILE):
#         with open(TOKEN_FILE, 'r') as file:
#             return json.load(file)
#     return None

# def save_tokens(tokens: Dict[str, Any]) -> None:
#     """Save tokens to a file."""
#     with open(TOKEN_FILE, 'w') as file:
#         json.dump(tokens, file)

# def get_tokens():
#     tokens = load_tokens()
#     if tokens and time.time() < tokens['expires_at']:
#         return tokens['access']
#     else:
#         return refresh_access_token(tokens['refresh'])

# def refresh_access_token(refresh_token: str) -> str:
#     """Refresh the access token using the refresh token."""
#     token_url = 'https://app.clio.com/oauth/token'
#     data = {
#         'grant_type': 'refresh_token',
#         'client_id': 'wTzciFxeZV4q4pepePje8TmDrx39G5tNxILiwp2U',
#         'client_secret' : 'mrD1Fh12QjWatMXCmcj6llBRfGDHLUBkv8pTef4Z',
#         'refresh_token': refresh_token
#     }
#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded'
#     }

#     response = requests.post(token_url, data=data, headers=headers)
    
#     if response.status_code == 200:
#         token_data = response.json()
#         access_token = token_data.get('access_token')
#         refresh_token = token_data.get('refresh_token')
#         expires_in = token_data.get('expires_in')
#         expires_at = time.time() + expires_in

#         new_tokens = {
#             'access_token': access_token,
#             'refresh_token': refresh_token,
#             'expires_at': expires_at
#         }
#         save_tokens(new_tokens)
#         return access_token
#     else:
#         raise Exception(f"Failed to refresh access token: {response.text}")
    
# # Example usage
# access_token = get_tokens()
# print(f"Access Token: {access_token}")
