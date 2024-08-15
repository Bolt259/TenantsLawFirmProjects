import json
import requests
from trash.tokenRefresher import load_tokens


def refresh_access_token(refresh_token):
    token_url = 'https://app.clio.com/oauth/token'
    data = {
        'grant_type': 'refresh_token',
        'client_id': 'wTzciFxeZV4q4pepePje8TmDrx39G5tNxILiwp2U',
        'client_secret': 'mrD1Fh12QjWatMXCmcj6llBRfGDHLUBkv8pTef4Z',
        'refresh_token': refresh_token
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(token_url, data=data, headers=headers)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access_token')
        return access_token
    else:
        raise Exception(f"Failed to refresh access token: {response.text}")


# Example usage
refresh_token = 'S5IhXIiFjehFXm7gcaKa1frUNkRhzgg9857R09m2'
new_access_token = refresh_access_token(refresh_token)
print(f"New Access Token: {new_access_token}")
