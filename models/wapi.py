import json
import requests
from dotenv import load_dotenv

load_dotenv()

class Phone:
    @staticmethod
    def format_phone_number(phone: str) -> str:
        if not phone: return
        return phone.replace(' ', '').replace('+', '').replace('-', '').replace('(', '').replace(')', '')

class WAPI:
    def __init__(self, instance_id: str, instance_token: str):

        self.__instance_id = instance_id
        self.__instance_token = instance_token

        self.base_url = 'https://api.w-api.app/v1'
        self.__headers = {
            'Authorization': f'Bearer {self.__instance_token}',
            'Content-Type': 'application/json'
        }
        self.__params = {
            'instanceId': self.__instance_id
        }

    def send_message(self, phone: str, message: str, delay: int) -> dict:
        phone = Phone.format_phone_number(phone)
        payload = {
            'phone': phone,
            'message': message,
            'delayMessage': delay
        }

        requests.request(
            'POST',
            f'{self.base_url}/message/send-text',
            headers=self.__headers,
            params=self.__params,
            json=payload
        )

    def send_audio(self, phone: str, audio_url: str, delay: int) -> dict:
        phone = Phone.format_phone_number(phone)
        payload = {
            'phone': phone,
            'audio': audio_url,
            'delayMessage': delay
        }

        requests.request(
            'POST',
            f'{self.base_url}/message/send-audio',
            headers=self.__headers,
            params=self.__params,
            json=payload
        )

    
    def send_button_actions(self, phone: str, message: str, buttons: list[dict]) -> dict:
        phone = Phone.format_phone_number(phone)
        payload = {
            'phone': phone,
            'message': message,
        }
        
        buttons = []
        for button in buttons:
            if button.get('type') == 'URL':
                buttons.append({
                    'type': "URL",
                    'buttonText': button.get('button_text'),
                    'url': button.get('url')
                })
            elif button.get('type') == 'CALL':
                buttons.append({
                    'type': 'CALL',
                    'buttonText': button.get('button_text'),
                    'phone': button.get('phone')
                })
            elif button.get('type') == 'REPLAY':
                buttons.append({
                    'type': 'REPLAY',
                    'buttonText': button.get('button_text'),
                })
        payload['buttonActions'] = buttons

        requests.request(
            'POST',
            f'{self.base_url}/message/send-button-actions',
            headers=self.__headers,
            params=self.__params,
            json=payload
        )

# chatbot = ZAPIChatbot()
# chatbot_phone = '5535997275487'
# chatbot_message = 'Hello, this is a test message from the chatbot.'
# response = chatbot.send_message(chatbot_phone, chatbot_message)
# print(response.text)
