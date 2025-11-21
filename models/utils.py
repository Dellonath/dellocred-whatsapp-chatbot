import argparse
import json
import logging
import datetime

class Args:
    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(description='Script to collect people information data from Agendor API and send messages via WhatsApp API')
        parser.add_argument('--datetime', type=str, default=datetime.datetime.now().strftime('%Y-%m-%dT06:00:00Z'), help="Datetime in ISO 8601 format to filter recently edited people data from Agendor API. Format should be 'YYYY-MM-DDTHH:MM:SSZ'")
        parser.add_argument('--agent_id', type=int, required=True, help='Agent ID responsible for sending messages via WhatsApp API')
        parser.add_argument('--flow_id', type=int, required=True, help='Flow ID to determine the type trigger to be sent via WhatsApp API')
        parser.add_argument('--category', type=str, required=True, help='Category of people to filter from Agendor API')
        parser.add_argument('--interval', type=int, default=180, help='Number of seconds between each contact')
        parser.add_argument('--limit', type=int, default=20, help='Limit of clients to contact')
        return parser.parse_args()

class GetIdByJson:
    @staticmethod
    def get_by_id(file_path: str, id: int) -> list:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for obj in data:
                if obj.get('id') == id: return obj


class Logs:
    logging.basicConfig(filename='logs/main.log',
                        format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
                        filemode='a',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)
    @staticmethod
    def get_logger():
        return logging.getLogger(__name__)
