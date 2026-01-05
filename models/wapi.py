import requests
from enum import Enum
from models.flow import ButtonActionsActionOptions, CarouselCard

class ButtonActionType(Enum):
    CALL = 'CALL'
    URL = 'URL'
    REPLAY = 'REPLAY'

class Phone:
    @staticmethod
    def format_phone_number(phone: str) -> str:
        if not phone: return
        return (
            phone
            .replace(' ', '')
            .replace('+', '')
            .replace('-', '')
            .replace('(', '')
            .replace(')', '')
        )

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

        response = requests.request(
            'POST',
            f'{self.base_url}/message/send-text',
            headers=self.__headers,
            params=self.__params,
            json=payload
        )

        if response.status_code != 200:
            raise Exception('Error sending audio actions:', response.text)
        return response.json()

    def send_audio(self, phone: str, audio_url: str, delay: int) -> dict:
        phone = Phone.format_phone_number(phone)
        payload = {
            'phone': phone,
            'audio': audio_url,
            'delayMessage': delay
        }

        response = requests.request(
            'POST',
            f'{self.base_url}/message/send-audio',
            headers=self.__headers,
            params=self.__params,
            json=payload
        )

        if response.status_code != 200:
            raise Exception('Error sending audio actions:', response.text)
        return response.json()

    def send_video(self, phone: str, video_url: str, delay: int) -> dict:
        phone = Phone.format_phone_number(phone)
        payload = {
            'phone': phone,
            'video': video_url,
            'delayMessage': delay
        }

        response = requests.request(
            'POST',
            f'{self.base_url}/message/send-video',
            headers=self.__headers,
            params=self.__params,
            json=payload
        )

        if response.status_code != 200:
            raise Exception('Error sending video actions:', response.text)
        return response.json()

    def send_button_actions(self, phone: str, message: str, buttons: list[ButtonActionsActionOptions]) -> dict:
        phone = Phone.format_phone_number(phone)
        payload = {
            'phone': phone,
            'message': message,
        }

        buttons_actions = []
        for button in buttons:
            buttons_actions.append(self.__create_button_action(button))
        payload['buttonActions'] = buttons_actions

        response = requests.request(
            'POST',
            f'{self.base_url}/message/send-button-actions',
            headers=self.__headers,
            params=self.__params,
            json=payload
        )
        if response.status_code != 200:
            raise Exception('Error sending button actions:', response.text)
        return response

    def send_carousel(self, phone: str, message: str, cards: list[CarouselCard]) -> dict:
        phone = Phone.format_phone_number(phone)
        payload = {
            'phone': phone,
            'message': message,
        }

        cards_actions = []
        buttons_actions = []
        for card in cards:
            for button in card.buttons:
                buttons_actions.append(self.__create_button_action(button))
            cards_actions.append({
                'text': card.text,
                'image': card.image,
                'buttonActions': buttons_actions
            })
        payload['message'] = message
        payload['cards'] = cards_actions

        response = requests.request(
            'POST',
            f'{self.base_url}/message/send-carousel',
            headers=self.__headers,
            params=self.__params,
            json=payload
        )

        if response.status_code != 200:
            raise Exception('Error sending button actions:', response.text)
        return response

    def check_number_status(self, phone: str) -> dict:
        phone = Phone.format_phone_number(phone)
        response = requests.request(
            'GET',
            f'{self.base_url}/contacts/phone-exists',
            headers=self.__headers,
            params={
                'instanceId': self.__instance_id,
                'phoneNumber': phone
            }
        )
        if response.status_code != 200:
            raise Exception('Error checking number:', response.text)

        return response.json().get('exists')

    def __create_button_action(self, button: ButtonActionsActionOptions) -> dict:
        if button.type == ButtonActionType.URL.value:
            return {
                'type': 'URL',
                'buttonText': button.button_text,
                'url': button.url
            }
        elif button.type == ButtonActionType.CALL.value:
            return {
                'type': 'CALL',
                'buttonText': button.button_text,
                'phone': button.phone
            }
        elif button.type == ButtonActionType.REPLAY.value:
            return {
                'type': 'REPLAY',
                'buttonText': button.button_text,
            }
        else:
            raise Exception('Invalid button action type:', button.type)

# chatbot = WAPI(instance_id='', instance_token='')
# chatbot_phone = '35998723079'
# chatbot_message = 'Hello, this is a test message from the chatbot.'
# response = chatbot.check_number_status(chatbot_phone, chatbot_message)
# print(response.text)
