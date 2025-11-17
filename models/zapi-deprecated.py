import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

class Phone:
    @staticmethod
    def format_phone_number(phone: str) -> str:
        return phone.replace(' ', '').replace('+', '').replace('-', '').replace('(', '').replace(')', '')

class WAPICredentials:
    @staticmethod
    def get_env_variables(key: str) -> str:
        return os.getenv(key)
class ZAPIChatbot:
    def __init__(self, client_token: str = None, instance_token: str = None, instance_id: str = None):

        self.__client_token = WAPICredentials.get_env_variables(client_token)
        self.__instance_id = WAPICredentials.get_env_variables(instance_id)
        self.__instance_token = WAPICredentials.get_env_variables(instance_token)

        self.base_url = 'https://api.z-api.io/'
        self.__headers = {
            'Client-Token': self.__client_token,
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
            f'{self.base_url}/instances/{self.__instance_id}/token/{self.__instance_token}/send-text',
            headers=self.__headers,
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
            f'{self.base_url}/instances/{self.__instance_id}/token/{self.__instance_token}/send-audio',
            headers=self.__headers,
            data=payload
        )

        return response

# chatbot = ZAPIChatbot()
# chatbot_phone = '5535997275487'
# chatbot_message = 'Hello, this is a test message from the chatbot.'
# response = chatbot.send_message(chatbot_phone, chatbot_message)
# print(response.text)
