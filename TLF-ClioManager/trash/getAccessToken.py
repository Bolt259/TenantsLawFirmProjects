import requests

def get_tokens(auth_code):
    token_url = 'https://app.clio.com/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': 'wTzciFxeZV4q4pepePje8TmDrx39G5tNxILiwp2U',
        'client_secret' : 'mrD1Fh12QjWatMXCmcj6llBRfGDHLUBkv8pTef4Z',
        'redirect_uri': 'https://localhost',
        'code': auth_code
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(token_url, data=data, headers=headers)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access_token')
        refresh_token = token_data.get('refresh_token')
        return access_token, refresh_token
    else:
        raise Exception(f"Failed to get tokens: {response.text}")

# Example usage
auth_code = 'OESVsncelW1y6gSPK1AW'
access_token, refresh_token = get_tokens(auth_code)
print(f"Access Token: {access_token}")
print(f"Refresh Token: {refresh_token}")
