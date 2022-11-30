import requests, os
from dotenv import load_dotenv

def last_chat_id(token):
    
    url = 'https://api.telegram.org/bot{}/getUpdates'.format(token)

    resp = requests.get(url)

    if resp.status_code == 200:
        
        json_msg = resp.json()
        
        for json_result in reversed(json_msg['result']):
                      
            message_keys = json_result['message'].keys()
            
            if ('new_chat_member' in message_keys) or ('group_chat_created' in message_keys):
                
                return print(json_result['message']['chat']['id'])

        print('Nenhum grupo encontrado!')
        
    else: print('A resposta falhou!')

load_dotenv()
API_KEY = os.environ.get('API_KEY')

last_chat_id(API_KEY)