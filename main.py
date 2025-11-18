# python3 main.py --datetime 2025-11-17T15:00:00Z --agent 938214 --flow_id 2 --category 'Cliente em potencial' --limit 10 --interval 180
# python3 main.py --datetime 2025-11-17T18:20:00Z --agent 932790 --flow_id 3 --category 'Cliente em potencial' --limit 22 --interval 180

import time
from models.agendor import AgendorAPI
from models.wapi import WAPI
from models.agent import Agent
from models.flow import Flow
from models.utils import Logs, Args, GetIdByJson

_log = Logs.get_logger()
args = Args.parse_args()

agent = Agent(**GetIdByJson.get_by_id('configs/agents.json', args.agent_id))
flow = Flow(**GetIdByJson.get_by_id('configs/flows.json', args.flow_id))
agendor_api = AgendorAPI()
w_api = WAPI(
    instance_id=agent.instance_id, 
    instance_token=agent.instance_token
)

filters={
    'category': args.category, 
    'owner_id': args.agent_id
}

clients = agendor_api.get_people_stream(
    since=args.datetime,
    filters=filters
)

# confirmation section
print(f'Extract clients updates from: {args.category})')
print(f'Agent: {agent.id} ({agent.name})')
print(f'Flow: {flow.id} ({flow.description})')
print(f'Number of clients extracted: {len(clients)}')
print(f'Number to be contacted: {args.limit}')
print(f'interval in secods: {args.interval/60} min ({args.interval} secs)')
print(f'Filter was applied: {filters}')
choic = input('Do you confirm starting the WhatsApp campaign with above parameters (Y/N)? ').upper()
if choic == 'Y':
    print('Starting campaign!')
elif choic == 'N':
    print('Cancelling execution of campaign!')
    exit()
else:
    print('invalid option!')
    exit()

# limit number of clients to be contacted
clients = clients[:args.limit]

for client in clients:
    client_id = client.get('id')
    client_cpf = client.get('cpf')
    client_name = client.get('name')
    client_first_name = client.get('first_name')
    client_phone = client.get('phone')
    client_owner_id = client.get('owner_id')
    
    for action in flow.actions:
        action_type = action.get('type')
        
        _log.info(f"{action_type} to client ID: {client_id}, Name: {client_name}, Phone: {client_phone}, Owner: {agent.first_name}")
        
        if action_type == 'send_message':
            message_template = action.get('message')
            personalized_message = message_template.replace('{{agent.first_name}}', agent.first_name).replace('{{client.first_name}}', client_first_name)
            delay=action.get('delay', 1)
            w_api.send_message(
                phone=client_phone,
                message=personalized_message,
                delay=delay
            )
        
        elif action_type == 'send_audio':
            audio_url = action.get('audio_url')
            delay=action.get('delay', 1)
            w_api.send_audio(
                phone=client_phone,
                audio_url=audio_url,
                delay=delay
            )
            
        elif action_type == 'wait':
            wait_seconds = action.get('seconds', 0)
            time.sleep(wait_seconds)
            
        elif action_type == 'send_button_actions':
            personalized_message = message_template.replace('{{agent.first_name}}', agent.first_name).replace('{{client.first_name}}', client_first_name)
            buttons = action.get('buttons')
            w_api.send_button_actions(
                phone=client_phone,
                message=personalized_message,
                buttons=buttons
            )
            
        elif action_type == 'webhook':
            endpoint = action.get('endpoint')
            personalized_payload = action.get('payload').replace('{{client.cpf}}', client_cpf).replace("'", '"')
            agendor_api.custom_execution(
                endpoint=endpoint,
                payload=personalized_payload
            )
        
    time.sleep(args.interval)
