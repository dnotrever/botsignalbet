def send_message(message):
    
    import requests, os
    from dotenv import load_dotenv
    
    load_dotenv()

    token = os.environ.get('API_KEY')
    group_id = os.environ.get('GROUP_ID')
    
    data = {'chat_id': group_id, 'text': message}
    
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
    
    requests.post(url, data)
