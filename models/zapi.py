import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

class Phone:
    @staticmethod
    def format_phone_number(phone: str) -> str:
        return phone.replace(' ', '').replace('+', '').replace('-', '').replace('(', '').replace(')', '')

class ZAPIChatbot:
    def __init__(self):
        self.base_url = 'https://api.z-api.io/'
        self.instance_token = os.getenv('ZAPI_INSTANCE_TOKEN')
        self.instance_id = os.getenv('ZAPI_INSTANCE_ID')
        self.client_token = os.getenv('ZAPI_CLIENT_TOKEN')
        self.headers = {
            'Client-Token': self.client_token,
            'Content-Type': 'application/json'
        }

    def send_message(self, phone: str, message: str):
        phone = Phone.format_phone_number(phone)
        payload = json.dumps({
            'phone': phone,
            'message': message
        })

        response = requests.request(
            'POST',
            f'{self.base_url}/instances/{self.instance_id}/token/{self.instance_token}/send-text',
            headers=self.headers,
            data=payload
        )

        return response

    def send_audio(self, phone: str, audio_url: str):
        phone = Phone.format_phone_number(phone)
        payload = json.dumps({
            'phone': phone,
            'audio': audio_url
        })

        
        response = requests.request(
            'POST',
            f'{self.base_url}/instances/{self.instance_id}/token/{self.instance_token}/send-audio',
            headers=self.headers,
            data=payload
        )

        return response

# chatbot = ZAPIChatbot()
# chatbot_phone = '5535997275487'
# chatbot_message = 'Hello, this is a test message from the chatbot.'
# response = chatbot.send_message(chatbot_phone, chatbot_message)
# print(response.text)
