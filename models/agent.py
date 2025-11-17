import os

class Agent:
    def __init__(self, id: int, name: str, creds: dict):
        self.id = id
        self.name = name
        self.first_name = name.split(' ')[0]
        self.instance_id = os.getenv(creds.get('instance_id'))
        self.instance_token = os.getenv(creds.get('instance_token'))
