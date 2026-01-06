import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

class AgendorAPI:
    def __init__(self):
        self.token = os.getenv('AGENDOR_TOKEN')
        self.base_url = 'https://api.agendor.com.br/v3'
        self.__headers = {
            'Authorization': f'Token {self.token}',
            'Content-Type': 'application/json'
        }

    def get_people_stream(self, since: str, agent: str, category: int, limit: int, payroll: str) -> list:
        params = {
            'per_page': 50,
            'category': self.__get_category_id(category=category),
            'userOwner': self.__get_owner_id(owner=agent),
            'withCustomFields': 'true'
        }

        if since:
            url=f'{self.base_url}/people/stream'
            params['since'] = since
        else:
            url = f'{self.base_url}/people'

        people=[]
        while True:
            response = requests.get(
                url,
                headers=self.__headers,
                params=params
            ).json()

            for person in response['data']:
                person_data = self.__format_person_data(person)
                if payroll:
                    if person_data.get('payroll') == payroll:
                        people.append(person_data)
                else:
                    people.append(person_data)
                if len(people) == limit: return people
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

    def __get_category_id(self, category: str) -> int:
        response = requests.get(
            'https://api.agendor.com.br/v3/categories',
            headers=self.__headers
        ).json()
        for cat in response['data']:
            if cat.get('name') == category: return cat.get('id')
        raise ValueError(f"Category '{category}' was not found")

    def __get_owner_id(self, owner: str) -> int:   
        response = requests.get(
            'https://api.agendor.com.br/v3/users',
            headers=self.__headers
        ).json()
        for usr in response['data']:
            if usr.get('name') == owner: return usr.get('id')   
        raise ValueError(f"User '{owner}' was not found")

    def __format_person_data(self, person: dict):
        return  {
            'id': person.get('id'),
            'cpf': person.get('cpf'),
            'category': person.get('category').get('name'),
            'name': person.get('name'),
            'first_name': person.get('name').split(' ')[0],
            'phone': person.get('contact').get('whatsapp'),
            'owner_id': person.get('ownerUser').get('id'),
            'payroll': person.get('customFields', []).get('convenio').get('value')
        }


# agendor_api = AgendorAPI()
# people_data = agendor_api.get_people_stream(since=args.datetime, category=args.category)
# print(people_data)