import time

class Flow:
    def __init__(self, id: int, description: str, actions: dict):
        self.id = id
        self.description = description
        self.actions = actions
