import argparse
import time
import datetime
import logging
from models import agendor, zapi

_log = logging.getLogger(__name__)
logging.basicConfig(filename='logs/main.log',
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
                    filemode='a',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

parser = argparse.ArgumentParser(description='Script to collect people information data from Agendor API and send messages via WhatsApp API')
parser.add_argument('--datetime', type=str, help="Datetime in ISO 8601 format to filter recently edited people data from Agendor API. Format should be 'YYYY-MM-DDTHH:MM:SSZ'")
parser.add_argument('--agents', type=str, nargs='+', help='Whitespace-separated Agents IDs responsible for sending messages via WhatsApp API')
parser.add_argument('--category', type=str, default='Cliente em potencial', help='Category of people to filter from Agendor API')
args = parser.parse_args()

print(args)

agendor_api = agendor.AgendorAPI()
people_data = agendor_api.get_people_stream(since=args.datetime, category=args.category)

chatbot = zapi.ZAPIChatbot()
chatbot_message = 'Hello, this is a test message from the chatbot.'
audio_url = 'https://audio.jukehost.co.uk/jaILZtwFPSNXUye3W2VNLiczBDr0mIw3'
for person in people_data:
    _log.info(f'Starting {person.get("name")} - {person.get("phone")}')
    _log.info(f'Sending message to {person.get("phone")}')
    response_message = chatbot.send_message(phone=person.get('phone'), message=chatbot_message)
    _log.info(f'Sending audio to {person.get("phone")}')
    response_audio = chatbot.send_audio(phone=person.get('phone'), audio_url=audio_url)
    _log.info(person, response_message.json(), response_audio.json())
    time.sleep(180)