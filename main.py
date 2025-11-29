# Aldry: python3 main.py --agent 938214 --flow_id 2 --category 'Cliente em potencial' --limit 40 --interval 180 --datetime 2025-11-23T06:00:00Z
# Rosilene: python3 main.py --agent 932790 --flow_id 3 --category 'Cliente em potencial' --limit 40 --interval 180 --datetime 2025-11-23T06:00:00Z
# Douglas: python3 main.py --agent 933092 --flow_id 5 --category 'Cliente em potencial' --limit 40 --interval 2 --datetime 2025-11-23T06:00:00Z

import os
import time
import logging
import random
from dotenv import load_dotenv
from dataclasses import dataclass
from models.agendor import AgendorAPI
from models.wapi import WAPI
from models.flow import Flow, FlowActionType
from models.utils import Args, GetIdByJson

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
class AgentCredentials:
    instance_id: int
    instance_token: int

@dataclass
class Agent:
    id: int
    name: str
    first_name: str
    creds: AgentCredentials
    
@dataclass
class Client:
    id: int
    cpf: str
    category: str
    name: str
    first_name: str
    phone: str
    owner_id: int

agent_data = GetIdByJson.get_by_id('configs/agents.json', args.agent_id)
flow_data = GetIdByJson.get_by_id('configs/flows.json', args.flow_id)

flow = Flow(**flow_data)
agent = Agent(
    id=agent_data.get('id'),
    name=agent_data.get('name'),
    first_name=agent_data.get('name').split()[0],
    creds=AgentCredentials(
        instance_id=os.getenv(agent_data.get('creds').get('instance_id')),
        instance_token=os.getenv(agent_data.get('creds').get('instance_token'))
    )
)

agendor_api = AgendorAPI()
w_api = WAPI(
    instance_id=agent.creds.instance_id,
    instance_token=agent.creds.instance_token
)

filters={
    'category': args.category,
    'owner_id': args.agent_id
}

clients = agendor_api.get_people_stream(
    since=args.datetime,
    filters=filters
)

# limit number of clients to be contacted
clients_filtered = clients[:args.limit]

# confirmation section
print(f'Extract clients updates from: {args.category})')
print(f'Agent: {agent.id} ({agent.name})')
print(f'Flow: {flow.id} ({flow.description})')
print(f'Since: {args.datetime}')
print(f'Number of clients extracted: {len(clients)}')
print(f'Number to be contacted: {len(clients_filtered)}')
print(f'interval in secods: {round(args.interval/60, 2)} min ({args.interval} secs)')
print(f'Filter was applied: {filters}')
choice = input('Do you confirm starting the WhatsApp campaign with above parameters (Y/N)? ').upper()
if choice == 'Y':
    logging.info('Campaign started successfully!')
elif choice == 'N':
    print('Cancelling execution of campaign!')
    exit()
else:
    print('invalid option!')
    exit()

for client in clients_filtered:
    client = Client(**client)

    logging.info(f'contacting client: {client.name} ({client.cpf}) | phone: {client.phone} | owner: {agent.name}')
    for action_loop in flow.actions:

        action = action_loop
        logging.info(f"-- triggering type: {action.type}")

        if not w_api.check_number_status(phone=client.phone):
            logging.warning(f"-- client {client.first_name} ({client.cpf}): phone incorrect, skipping to next client")
            payload = Flow.replace_text_by_variables(
                text="{'cpf': '{{client.cpf}}', 'category': 'Telefone incorreto', 'customFields': {'contato_via': 'Disparo'}}",
                vars={'{{client.cpf}}': client.cpf}
            )
            agendor_api.custom_execution(
                url='https://api.agendor.com.br/v3/people/upsert',
                payload=payload
            )
            continue

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
            logging.info(f"-- choice selected: {action.type}")
            
        if action.type == FlowActionType.SEND_MESSAGE.value:
            message = Flow.replace_text_by_variables(
                text=action.message,
                vars={
                    '{{agent.first_name}}': agent.first_name,
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

        elif action.type == FlowActionType.SEND_BUTTON_ACTIONS.value:
            message = Flow.replace_text_by_variables(
                text=action.message,
                vars={
                    '{{agent.first_name}}': agent.first_name,
                    '{{client.first_name}}': client.first_name
                }
            )
            w_api.send_button_actions(
                phone=client.phone,
                message=message,
                buttons=action.buttons
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

    time.sleep(args.interval)

logging.info('Campaign finished successfully!')