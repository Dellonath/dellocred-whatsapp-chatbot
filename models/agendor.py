import os
import requests
import logging
from dotenv import load_dotenv
load_dotenv()

_log = logging.getLogger(__name__)
logging.basicConfig(filename='logs/agendor.log',
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
                    filemode='a',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

class AgendorAPI:
    def __init__(self):
        self.token = os.getenv('AGENDOR_TOKEN')
        self.base_url = 'https://api.agendor.com.br/v3'

    def get_people_stream(self, since: str, category: str) -> list:
        _log.info(f"Starting collecting people data since: {since}")
        people=[]
        url = f'{self.base_url}/people/stream?since={since}'
        headers = {
            'Authorization': f'Token {self.token}',
            'Content-Type': 'application/json'
        }
        params = {
            'since': since,
            'per_page': 50
        }
        while True:
            response = requests.get(url, headers=headers, params=params).json()
            for person in response['data']:
                if person.get('category', {}).get('name') == category:
                    people.append({
                        'name': person.get('name'),
                        'phone': person.get('contact').get('whatsapp')
                    })
                    _log.info(f"-- person name: {person.get('name')} phone: {person.get('contact').get('whatsapp')}")

            if 'next' in response['links']: 
                url = response.get('links').get('next')
            else: break
        
        return people

# agendor_api = AgendorAPI()
# people_data = agendor_api.get_people_stream(since=args.datetime, category=args.category)
# print(people_data)