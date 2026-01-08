# python3 main.py --agent 'Aldriely Lima' --flow_id 6 --category 'Cliente em potencial' --limit 20 --datetime 2025-11-23T06:00:00Z
# python3 main.py --agent 'Rosilene Mendes' --flow_id 3 --category 'Cliente em potencial' --limit 40 --datetime 2025-11-23T06:00:00Z
# python3 main.py --agent 'Douglas Oliveira' --flow_id 7 --category 'Cliente em potencial' --limit 40 --datetime 2025-12-01T06:00:00Z

# python3 main.py --agent 'Aldriely Lima' --flow_name disparo_consignado_siape_bb --category 'Aguardando atendimento' --payroll Siape
# python3 main.py --agent 'Rosilene Mendes' --flow_name portabilidade_direcionado_rosilene --category 'Aguardando atendimento' --payroll Siape --instances 1,2,3

import os
import logging
import random
import time
import json
from dotenv import load_dotenv
from dataclasses import dataclass, field
from models.agendor import AgendorAPI
from models.wapi import WAPI
from models.flow import Flow, FlowActionType
from models.utils import Args

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('logs/main.log'), # log to file
        logging.StreamHandler() # stream to console
    ]
)
args = Args.parse_args()

@dataclass
class Instance:
    id: int
    active: bool
    mature: bool
    name: str
    phone: str
    instance_id: int
    instance_token: int
    block_instances_ids: list[str] = field(default_factory=list)

@dataclass
class Client:
    id: int
    cpf: str
    category: str
    name: str
    first_name: str
    phone: str
    owner_id: int
    payroll: str

with open(f'configs/flows/{args.flow_name}.json', 'r') as f:
    flow_cfg = json.load(f)

with open(f'configs/instances.json', 'r') as f:
    INSTANCES: list[Instance] = [
        Instance(**instance) for instance in json.load(f)
        if instance.get('active') and instance.get('id') in map(int, args.instances.split(','))
    ]
    if len(INSTANCES) == 0 or len(INSTANCES) != len(args.instances.split(',')):
        logging.error('No active instances found or some instance IDs were not found in configs/instances.json')
        exit()

flow = Flow(**flow_cfg)
agendor_api = AgendorAPI(token=os.getenv('AGENDOR_TOKEN'))

# confirmation section
print(f'Agent: {args.agent}')
print(f'Flow: {flow.description} ({flow.id})')
print(f'Number of clients to be contacted: {args.limit}')
print(f'Category: {args.category}')
print(f'Payroll: {args.payroll}') if args.payroll else None
print(f'Since: {args.since}') if args.since else None
print(f'Instances:')
for instance in INSTANCES:
    print(f'-- id: {instance.id} phone: {instance.phone} name: {instance.name} ')

choice = input('Do you confirm starting the WhatsApp campaign with above parameters (Y/N)? ').upper()
if choice == 'Y':
    logging.info('Campaign started successfully!')
elif choice == 'N':
    print('Cancelling execution of campaign!')
    exit()
else:
    print('invalid option!')
    exit()

clients = agendor_api.get_people_stream(
    since=args.since,
    category=args.category,
    agent=args.agent,
    limit=args.limit,
    payroll=args.payroll
)

success: int = 0
failed: int = 0
for client in clients:
    client: Client = Client(**client)

    chosen_instance: Instance = random.choice([
        instance for instance in INSTANCES
    ])
    w_api: WAPI = WAPI(
        instance_id=os.getenv(chosen_instance.instance_id),
        instance_token=os.getenv(chosen_instance.instance_token)
    )

    logging.info(f'contacting client ({success + failed}/{len(clients)}): {client.name} ({client.cpf}) | phone: {client.phone} | owner: {args.agent} | instance: {chosen_instance.name} ({chosen_instance.phone})')
    if not w_api.check_number_status(phone=client.phone):
        logging.warning(f'-- phone incorrect, skipping to next client')
        payload = Flow.replace_text_by_variables(
            text="{'cpf': '{{client.cpf}}', 'category': 'Telefone incorreto', 'customFields': {'contato_via': 'Disparo'}}",
            vars={'{{client.cpf}}': client.cpf}
        )
        agendor_api.custom_execution(
            url='https://api.agendor.com.br/v3/people/upsert',
            payload=payload
        )
        failed += 1
        continue
    else:
        success += 1

    for action_loop in flow.actions:
        action = action_loop
        logging.info(f"-- triggering type: {action.type}")
        if action.type == FlowActionType.RANDOM.value:
            population, weights = [], []
            for choice in action.choices:
                population.append(choice.action)
                weights.append(choice.prob)
            action = random.choices(
                population=population,
                weights=weights,
                k=1
            )[0]
            logging.info(f"---- choice selected: {action.type}")

        if action.type == FlowActionType.SEND_MESSAGE.value:
            message = Flow.replace_text_by_variables(
                text=action.message,
                vars={
                    '{{agent.first_name}}': args.agent.split(' ')[0],
                    '{{client.first_name}}': client.first_name
                }
            )
            w_api.send_message(
                phone=client.phone,
                message=message,
                delay=action.delay
            )

        elif action.type == FlowActionType.SEND_AUDIO.value:
            w_api.send_audio(
                phone=client.phone,
                audio_url=action.audio_url,
                delay=action.delay
            )

        elif action.type == FlowActionType.SEND_VIDEO.value:
            w_api.send_video(
                phone=client.phone,
                video_url=action.video_url,
                delay=action.delay
            )

        elif action.type == FlowActionType.SEND_BUTTON_ACTIONS.value:
            message = Flow.replace_text_by_variables(
                text=action.message,
                vars={
                    '{{agent.first_name}}': args.agent.split(' ')[0],
                    '{{client.first_name}}': client.first_name
                }
            )
            w_api.send_button_actions(
                phone=client.phone,
                message=message,
                buttons=action.buttons
            )

        elif action.type == FlowActionType.SEND_CAROUSEL.value:
            message = Flow.replace_text_by_variables(
                text=action.message,
                vars={
                    '{{agent.first_name}}': args.agent.split(' ')[0],
                    '{{client.first_name}}': client.first_name
                }
            )
            w_api.send_carousel(
                phone=client.phone,
                message=message,
                cards=action.cards
            )

        elif action.type == FlowActionType.WEBHOOK.value:
            payload = Flow.replace_text_by_variables(
                text=action.payload,
                vars={'{{client.cpf}}': client.cpf}
            )
            agendor_api.custom_execution(
                url=action.endpoint,
                payload=payload
            )

    wait_seconds: int = random.randint(30, 300)
    logging.info(f'-- waiting for {wait_seconds} seconds')
    time.sleep(wait_seconds)

logging.info('Campaign finished successfully! Report:')
logging.info(f'-- success: {success}')
logging.info(f'-- failed: {failed}')