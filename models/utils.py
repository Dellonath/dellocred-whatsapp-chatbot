import argparse
import json
class Args:
    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(description='Script to collect people information data from Agendor API and send messages via WhatsApp API')
        parser.add_argument('--since', type=str, help="Datetime in ISO 8601 format to filter recently edited people data from Agendor API. Format should be 'YYYY-MM-DDTHH:MM:SSZ'")
        parser.add_argument('--agent', type=str, required=True, help='Agent responsible for sending messages via WhatsApp API')
        parser.add_argument('--flow_id', type=int, required=True, help='Flow ID to determine the type trigger to be sent via WhatsApp API')
        parser.add_argument('--category', type=str, required=True, help='Category of people to filter from Agendor API')
        parser.add_argument('--limit', type=int, default=100, help='Limit of clients to contact')
        return parser.parse_args()

class LoadObjectCfn:
    @staticmethod
    def by_id(file_path: str, id: int) -> list:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for obj in data:
                if obj.get('id') == id: return obj

    @staticmethod
    def by_name(file_path: str, name: str) -> list:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for obj in data:
                if obj.get('name') == name: return obj
        raise ValueError(f"User '{name}' was not found in configs/agents.json")
