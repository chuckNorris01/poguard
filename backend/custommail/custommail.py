import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
tenant_id = os.getenv('TENATN_ID')

base_url = 'https://graph.microsoft.com/v1.0/users/ordre@bad.no/'
token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
token_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': 'https://graph.microsoft.com/.default'
}

class SendAPIEmail:
    def __init__(self) -> None:
        self.headers = {
            'Content-Type': 'application/json'
        }
    
    
    def get_access_token(self) -> str:
        response = requests.post(url=token_url, data=token_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            return token
        else:
            raise Exception('Failed to get access token, status code: ', response.status_code)
            
            
    def send_email(self, subject:str, content:str, address:str) -> None:
        access_token = self.get_access_token()
        self.headers['Authorization'] = access_token
        payload = json.dumps({
            "message": {
                "subject": f"{subject}",
                "body": {
                    "contentType": "HTML",
                    "content": f"{content}"
                },
                "toRecipients": [
                {
                    "emailAddress": {
                        "address": f"{address}"
                    }
                }
                ]
            }
        })
        response = requests.post(url=f'{base_url}/sendMail', headers=self.headers, data=payload)
        if response.status_code == 202:
            return
        else:
            raise Exception('Failed to send the email, status code: ', response.status_code)