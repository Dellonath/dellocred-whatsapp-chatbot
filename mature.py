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
    phone: str
    instance_id: int
    instance_token: int

INSTANCES = [{
        "active": True,
        "phone": "553597693994",
        "instance_id": "WAPI_INSTANCE_ID_CHIP1",
        "instance_token": "WAPI_INSTANCE_TOKEN_CHIP1"
    },
    {
        "active": True,
        "phone": "553597082862",
        "instance_id": "WAPI_INSTANCE_ID_CHIP2",
        "instance_token": "WAPI_INSTANCE_TOKEN_CHIP2"
        
    }
]

AUDIOS = [
    "https://audio.jukehost.co.uk/aRj1U3HeGBeef0piiizzvtMuQVgXZxTs.ogg",
    "https://audio.jukehost.co.uk/WfDsaBkFCOVJW8ogPb8G9Wh7J2w6TClM.ogg",
    "https://audio.jukehost.co.uk/X7XLmZTpSSIFdF6Lef2PxLD3clJY8HMg.ogg",
    "https://audio.jukehost.co.uk/qCcIBfdY7LKWq9dOdgmA3mFqLzH4qxuC.ogg"
]

def generate_random_text(chars=string.ascii_lowercase + string.ascii_uppercase + string.digits + '!?-.'):
    text = []
    for _ in range(random.randint(2, 10)):
        text.append(''.join(random.choices(chars, k=random.randint(2, 10))))
    return ' '.join(text)

for _ in range(300):

    sender_instance = random.choices(
        population=[instance for instance in INSTANCES if instance.get('active')]
    )[0]

    receiver_instance = random.choices(
        population=[instance for instance in INSTANCES if instance.get('active') and instance.get('phone') != sender_instance.get('phone')]
    )[0]

    w_api = WAPI(
        instance_id=os.getenv(sender_instance.get('instance_id')),
        instance_token=os.getenv(sender_instance.get('instance_token')),
    )

    action = random.choices(
        population=[
            'send_message',
            'send_audio',
            # 'send_video'
        ],
        weights=[0.7, 0.3],
    )[0]

    if action == FlowActionType.SEND_MESSAGE.value:
        request = w_api.send_message(
            phone=receiver_instance.get('phone'),
            message=generate_random_text(),
            delay=random.randint(1, 15)
        )

    elif action == FlowActionType.SEND_AUDIO.value:
        request = w_api.send_audio(
            phone=receiver_instance.get('phone'),
            audio_url=random.choice(AUDIOS),
            delay=random.randint(1, 15)
        )

    elif action == FlowActionType.SEND_VIDEO.value:
        request = w_api.send_video(
            phone=receiver_instance.get('phone'),
            video_url=action.video_url,
            delay=random.randint(1, 15)
        )
    print(request)
    
    time.sleep(random.randint(5, 360))
