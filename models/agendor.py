import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

class FilterPerson:
    @staticmethod
    def apply_filter(person: dict, filters: str) -> list:
        for key, value in filters.items():
            if person.get(key) != value: return False
        return True

class AgendorAPI:
    def __init__(self):
        self.token = os.getenv('AGENDOR_TOKEN')
        self.base_url = 'https://api.agendor.com.br/v3'
        self.__headers = {
            'Authorization': f'Token {self.token}',
            'Content-Type': 'application/json'
        }

    def get_people_stream(self, since: str, filters: dict=None) -> list:
        people=[]
        url=f'{self.base_url}/people/stream?since={since}'
        params = {
            'since': since,
            'per_page': 50
        }
        while True:
            response = requests.get(
                url,
                headers=self.__headers,
                params=params
            ).json()

            for person in response['data']:
                person_data = {
                    'id': person.get('id'),
                    'cpf': person.get('cpf'),
                    'category': person.get('category').get('name'),
                    'name': person.get('name'),
                    'first_name': person.get('name').split(' ')[0],
                    'phone': person.get('contact').get('whatsapp'),
                    'owner_id': person.get('ownerUser').get('id')
                }
                if FilterPerson.apply_filter(person_data, filters): people.append(person_data)

            if 'next' in response['links']:
                url = response.get('links').get('next')
            else: break

        return people

    def custom_execution(self, url: str, payload: dict | None = None) -> dict:
        response = requests.post(
            url=url,
            headers=self.__headers,
            json=json.loads(payload)
        )
        return response


# agendor_api = AgendorAPI()
# people_data = agendor_api.get_people_stream(since=args.datetime, category=args.category)
# print(people_data)