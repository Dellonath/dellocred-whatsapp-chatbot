from dataclasses import dataclass, field
from enum import Enum

class FlowActionType(Enum):
    SEND_MESSAGE = 'send_message'
    SEND_AUDIO = 'send_audio'
    SEND_VIDEO = 'send_video'
    SEND_BUTTON_ACTIONS = 'send_button_actions'
    SEND_CAROUSEL = 'send_carousel'
    WEBHOOK = 'webhook'
    RANDOM = 'random'

@dataclass
class MessageAction:
    message: str
    type: str = field(default=FlowActionType.SEND_MESSAGE.value, init=False)
    delay: int = field(default=1)

@dataclass
class AudioAction:
    audio_url: str
    type: str = field(default=FlowActionType.SEND_AUDIO.value, init=False)
    delay: int = field(default=1)

@dataclass
class VideoAction:
    video_url: str
    type: str = field(default=FlowActionType.SEND_VIDEO.value, init=False)
    delay: int = field(default=1)

@dataclass
class WebhookAction:
    endpoint: str
    payload: list
    type: str = field(default=FlowActionType.WEBHOOK.value, init=False)

@dataclass
class RandomActionOption:
    prob: float
    action: MessageAction | AudioAction | WebhookAction

@dataclass
class RandomAction:
    choices: list[RandomActionOption]
    type: str = field(default=FlowActionType.RANDOM.value, init=False)

@dataclass
class ButtonActionsActionOptions:
    type: str
    button_text: str
    url: str | None
    phone: str | None

@dataclass
class ButtonActionsAction:
    message: str
    buttons: list[ButtonActionsActionOptions]
    type: str = field(default=FlowActionType.SEND_BUTTON_ACTIONS.value, init=False)

@dataclass
class CarouselCard:
    text: str
    image: str
    buttons: list[ButtonActionsActionOptions]

@dataclass
class CarouselAction:
    message: str
    cards: list[CarouselCard]
    type: str = field(default=FlowActionType.SEND_CAROUSEL.value, init=False)

class Flow:
    def __init__(self, id: int, active: bool, description: str, actions: dict):
        self.id = id
        self.active = active
        self.description = description
        self.actions = [self.__create_action(action) for action in actions]
        assert self.active, f'-- flow id {self.id} is inactive'

    def __create_action(self, action: dict):
        action_type: str = action.get('type')

        if action_type == FlowActionType.SEND_MESSAGE.value:
            return MessageAction(
                message=action.get('message')
            )
        elif action_type == FlowActionType.SEND_AUDIO.value:
            return AudioAction(
                audio_url=action.get('audio_url')
            )
        elif action_type == FlowActionType.SEND_VIDEO.value:
            return VideoAction(
                video_url=action.get('video_url')
            )
        elif action_type == FlowActionType.SEND_BUTTON_ACTIONS.value:
            return ButtonActionsAction(
                message=action.get('message'),
                buttons=[
                    ButtonActionsActionOptions(
                        type=button.get('type'),
                        button_text=button.get('button_text'),
                        url=button.get('url'),
                        phone=button.get('phone')
                    ) for button in action.get('buttons')
                ]
            )
        elif action_type == FlowActionType.SEND_CAROUSEL.value:
            return CarouselAction(
                message=action.get('message'),
                cards=[
                    CarouselCard(
                        text=card.get('text'),
                        image=card.get('image'),
                        buttons=[
                            ButtonActionsActionOptions(
                                type=button.get('type'),
                                button_text=button.get('button_text'),
                                url=button.get('url', None),
                                phone=button.get('phone', None)
                            ) for button in card.get('buttons')
                        ]
                    ) for card in action.get('cards')
                ]
            )
        elif action_type == FlowActionType.WEBHOOK.value:
            return WebhookAction(
                endpoint=action.get('endpoint'),
                payload=action.get('payload')
            )
        elif action_type == FlowActionType.RANDOM.value:
            probs: list[float] = [choice.get('prob') for choice in action.get('choices')]
            if sum(probs) != 1.0:
                raise Exception(f'-- invalid sum of probabilities {round(sum(probs), 2)}, sum must be 1.0')
            return RandomAction(
                choices=[
                    RandomActionOption(
                        prob=choice.get('prob'),
                        action=self.__create_action(choice.get('action'))
                    ) for choice in action.get('choices')
                ]
            )
        else:
            raise Exception(f"Unknown action type: '{action_type}'")

    @staticmethod
    def replace_text_by_variables(text: str, vars: dict | None = None) -> list:
        if not vars: return text
        for key, value in vars.items():
            text = text.replace(key, str(value)).replace("'", '"')
        return text
