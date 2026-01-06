import os
import string
import random
import time
from dotenv import load_dotenv
from dataclasses import dataclass
from models.wapi import WAPI
from models.flow import FlowActionType

load_dotenv()

@dataclass
class AgentInstance:
    active: bool
    name: str
    phone: str
    instance_id: int
    instance_token: int
    block: list[str]

INSTANCES = [
    {
        "active": False,
        "name": "Chip 1",
        "phone": "553597693994",
        "instance_id": "WAPI_INSTANCE_ID_CHIP1",
        "instance_token": "WAPI_INSTANCE_TOKEN_CHIP1"
    },
    {
        "active": True,
        "name": "Chip 2",
        "phone": "553597082862",
        "instance_id": "WAPI_INSTANCE_ID_CHIP2",
        "instance_token": "WAPI_INSTANCE_TOKEN_CHIP2"
        
    },
    {
        "active": True,
        "name": "Rosilene Mendes Business",
        "phone": "553588629435",
        "instance_id": "WAPI_INSTANCE_ID_RMENDES",
        "instance_token": "WAPI_INSTANCE_TOKEN_RMENDES",
        "block": [
            "553599748699"
        ]
    },
    {
        "active": True,
        "name": "Bianca Caetano Business",
        "phone": "553591683067",
        "instance_id": "WAPI_INSTANCE_ID_CHIP3",
        "instance_token": "WAPI_INSTANCE_TOKEN_CHIP3" 
    },
    {
        "active": True,
        "name": "Danielle Oliveira Business",
        "phone": "553591464882",
        "instance_id": "WAPI_INSTANCE_ID_DOLIVEIRA",
        "instance_token": "WAPI_INSTANCE_TOKEN_DOLIVEIRA" 
    },
    {
        "active": True,
        "name": "Douglas Oliveira Business",
        "phone": "553599748699",
        "instance_id": "WAPI_INSTANCE_ID_DOUGLASOLIVEIRA",
        "instance_token": "WAPI_INSTANCE_TOKEN_DOUGLASOLIVEIRA",
        "block": [
            "553588629435"
        ]
    }
]

AUDIOS = [
    "https://audio.jukehost.co.uk/gjx488CfOgtEHMHx9CUHnadNiYFq6k47.ogg", # tagarela 4 secs
    "https://audio.jukehost.co.uk/ZeLPWpF6zKitGd2xHy4AruKxigTfHsji.ogg", # tagarela 5 secs
    "https://audio.jukehost.co.uk/zij15c6kGSC2cmiJf9BF4FNhoI67bXvA.ogg", # tagarela 6 secs
    "https://audio.jukehost.co.uk/DrGDkuNtgYoVLXYwQsMGTRXAkDGYhOAq.ogg", # tagarela 7 secs
    "https://audio.jukehost.co.uk/fYnBgU3tJbcmfVbsjN5xY7YfNHWFbwwJ.ogg", # tagarela 8 secs
    "https://audio.jukehost.co.uk/6wtE0udkRWEstzmwbAURxyYXcg9Z51LY.ogg", # tagarela 9 secs
    "https://audio.jukehost.co.uk/kZpZiXbUTTYEH7jSIc01YJfvuIR2uXiK.ogg", # tagarela 10 secs
    "https://audio.jukehost.co.uk/IC6fOaai6qKy0Nw3kbOisxGNXHsiBRlg.ogg", # tagarela 11 secs
    "https://audio.jukehost.co.uk/1NDi0hAAqdbcmzZXSTyW5pkA30VvySFd.ogg", # tagarela 12 secs
    "https://audio.jukehost.co.uk/Orf2GERba9h3BWmaGysAHOvAw3GLsmwt.ogg", # tagarela 13 secs
    "https://audio.jukehost.co.uk/x28Z9Yb1WVtaWlPqIZI264C9LfOjp1kR.ogg", # tagarela 14 secs
    "https://audio.jukehost.co.uk/3q0JEqaD7SV9zDrfCfsC4qEzj63qt6HA.ogg", # tagarela 15 secs

]

IMAGES = [
    "https://res.cloudinary.com/dg0nvnjqw/image/upload/v1764680916/main-sample.png",
    "https://res.cloudinary.com/dg0nvnjqw/image/upload/v1764680916/cld-sample-5.jpg",
    "https://res.cloudinary.com/dg0nvnjqw/image/upload/v1764680915/cld-sample-4.jpg",
    "https://res.cloudinary.com/dg0nvnjqw/image/upload/v1764680915/cld-sample-3.jpg",
    "https://res.cloudinary.com/dg0nvnjqw/image/upload/v1764680914/cld-sample.jpg",
    "https://res.cloudinary.com/dg0nvnjqw/image/upload/v1764680915/cld-sample-2.jpg",
    "https://res.cloudinary.com/dg0nvnjqw/image/upload/v1764680914/samples/waves.png",

]

def generate_random_text(chars=string.ascii_lowercase + string.ascii_uppercase + string.digits + '!?-.'):
    number_of_words: int = random.randint(2, 10)
    size_of_word: int = random.randint(2, 10)
    text: list = []
    for _ in range(number_of_words):
        text.append(''.join(random.choices(chars, k=size_of_word)))
    return ' '.join(text)

for _ in range(300):

    active_instances: list[dict] = [instance for instance in INSTANCES if instance.get('active')]

    sender_instance: dict = random.choices(
        population=active_instances
    )[0]

    receiver_instances: list = random.choices(
        population=[
            instance for instance in active_instances 
            if instance.get('phone') != sender_instance.get('phone')
            and instance.get('phone') not in sender_instance.get('block', [])
        ],
        k=random.randint(1, len(active_instances) - 1)
    )

    w_api: WAPI = WAPI(
        instance_id=os.getenv(sender_instance.get('instance_id')),
        instance_token=os.getenv(sender_instance.get('instance_token')),
    )

    for receiver_instance in receiver_instances:
        number_of_random_actions: int = random.randint(1, 3)
        print(
            f'Interaction started ' 
            f'from {sender_instance.get("name")} ({sender_instance.get("phone")}) '
            f'to {receiver_instance.get("name")} ({receiver_instance.get("phone")}) '
            f'({number_of_random_actions} actions):'
        )
        for _ in range(number_of_random_actions):
            action: FlowActionType = random.choices(
                population=[
                    FlowActionType.SEND_MESSAGE,
                    FlowActionType.SEND_AUDIO,
                    FlowActionType.SEND_IMAGE
                ],
                weights=[0.6, 0.3, 0.1],
            )[0]

            seconds: int = random.randint(1, 15)
            delay: int = random.randint(1, seconds)

            print(f'-- sending {action}, waiting for {seconds} seconds...')

            if action == FlowActionType.SEND_MESSAGE:
                request: dict = w_api.send_message(
                    phone=receiver_instance.get('phone'),
                    message=generate_random_text(),
                    delay=delay
                )

            elif action == FlowActionType.SEND_AUDIO:
                request: dict = w_api.send_audio(
                    phone=receiver_instance.get('phone'),
                    audio_url=random.choice(AUDIOS),
                    delay=delay
                )

            elif action == FlowActionType.SEND_IMAGE:
                request: dict = w_api.send_image(
                    phone=receiver_instance.get('phone'),
                    image_url=random.choice(IMAGES),
                    delay=delay
                )
            
            time.sleep(seconds)

    time.sleep(random.randint(5, 20))
    
