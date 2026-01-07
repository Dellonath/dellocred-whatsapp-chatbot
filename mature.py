import os
import string
import random
import time
from dotenv import load_dotenv
from dataclasses import dataclass, field
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
    block_sender: list[str] = field(default_factory=list)

DELAY_BETWEEN_INTERACTIONS: int = random.randint(3, 20)

ACTIONS = [
    {
        'type': FlowActionType.SEND_MESSAGE,
        'prob': 0.7
    },
    {
        'type': FlowActionType.SEND_AUDIO,
        'prob': 0.25
    },
    {
        'type': FlowActionType.SEND_IMAGE,
        'prob': 0.05
    }
]

INSTANCES = [
    {
        "active": True,
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
        "block_sender": [
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
        "block_sender": [
            "553588629435"
        ]
    }
]

AUDIOS = [
    'https://res.cloudinary.com/dg0nvnjqw/video/upload/v1767726360/tagarela_4_secs_clapku.ogg',
    'https://res.cloudinary.com/dg0nvnjqw/video/upload/v1767726359/tagarela_5_secs_cyhygd.ogg',
    'https://res.cloudinary.com/dg0nvnjqw/video/upload/v1767726358/tagarela_6_secs_ejuglr.ogg',
    'https://res.cloudinary.com/dg0nvnjqw/video/upload/v1767726358/tagarela_7_secs_wmakxo.ogg',
    'https://res.cloudinary.com/dg0nvnjqw/video/upload/v1767726358/tagarela_8_secs_bxyamk.ogg',
    'https://res.cloudinary.com/dg0nvnjqw/video/upload/v1767726358/tagarela_9_secs_smegzs.ogg',
    'https://res.cloudinary.com/dg0nvnjqw/video/upload/v1767726358/tagarela_10_secs_lryspe.ogg',
    'https://res.cloudinary.com/dg0nvnjqw/video/upload/v1767726358/tagarela_11_secs_b1poes.ogg',
    'https://res.cloudinary.com/dg0nvnjqw/video/upload/v1767726357/tagarela_12_secs_oapknw.ogg',
    'https://res.cloudinary.com/dg0nvnjqw/video/upload/v1767726357/tagarela_13_secs_ed554e.ogg',
    'https://res.cloudinary.com/dg0nvnjqw/video/upload/v1767726357/tagarela_14_secs_nxpcxn.ogg',
    'https://res.cloudinary.com/dg0nvnjqw/video/upload/v1767726218/tagarela_15_secs_bd0qoz.ogg'
]

IMAGES = [
    'https://res.cloudinary.com/dg0nvnjqw/image/upload/v1764680916/main-sample.png',
    'https://res.cloudinary.com/dg0nvnjqw/image/upload/v1764680916/cld-sample-5.jpg',
    'https://res.cloudinary.com/dg0nvnjqw/image/upload/v1764680915/cld-sample-4.jpg',
    'https://res.cloudinary.com/dg0nvnjqw/image/upload/v1764680915/cld-sample-3.jpg',
    'https://res.cloudinary.com/dg0nvnjqw/image/upload/v1764680914/cld-sample.jpg',
    'https://res.cloudinary.com/dg0nvnjqw/image/upload/v1764680915/cld-sample-2.jpg',
    'https://res.cloudinary.com/dg0nvnjqw/image/upload/v1764680914/samples/waves.png',
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

    sender_instance: AgentInstance = AgentInstance(
        **random.choices(population=active_instances)[0]
    )

    receiver_instances: list[AgentInstance] = random.choices(
        population=[
            AgentInstance(**instance) for instance in active_instances 
            if instance.get('phone') != sender_instance.phone
            and instance.get('phone') not in sender_instance.block_sender
        ],
        k=random.randint(1, len(active_instances) - 1)
    )

    w_api: WAPI = WAPI(
        instance_id=os.getenv(sender_instance.instance_id),
        instance_token=os.getenv(sender_instance.instance_token),
    )

    for receiver_instance in receiver_instances:
        number_of_random_actions: int = random.randint(1, 3)
        print(
            f'Interaction started ' 
            f'from {sender_instance.name} ({sender_instance.phone}) '
            f'to {receiver_instance.name} ({receiver_instance.phone}) '
            f'({number_of_random_actions} actions):'
        )
        for _ in range(number_of_random_actions):
            action: FlowActionType = random.choices(
                population=[action['type'] for action in ACTIONS],
                weights=[action['prob'] for action in ACTIONS],
            )[0]

            seconds: int = random.randint(1, 15)
            delay: int = random.randint(1, seconds)

            print(f'-- sending {action}, waiting for {seconds} seconds...')

            if action == FlowActionType.SEND_MESSAGE:
                request: dict = w_api.send_message(
                    phone=receiver_instance.phone,
                    message=generate_random_text(),
                    delay=delay
                )

            elif action == FlowActionType.SEND_AUDIO:
                request: dict = w_api.send_audio(
                    phone=receiver_instance.phone,
                    audio_url=random.choice(AUDIOS),
                    delay=delay
                )

            elif action == FlowActionType.SEND_IMAGE:
                request: dict = w_api.send_image(
                    phone=receiver_instance.phone,
                    image_url=random.choice(IMAGES),
                    delay=delay
                )
            
            time.sleep(seconds)

    time.sleep(DELAY_BETWEEN_INTERACTIONS)
    
