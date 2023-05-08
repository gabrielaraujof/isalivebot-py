import os
import requests

chat_id = os.getenv('CHAT_ID')
domain = os.getenv('TELEGRAM_BOT_DOMAIN')

def notify(message):
    data = {'chatId': chat_id, 'message': message}
    try:
        response = requests.post(f'{domain}/notify', json=data)
        response.raise_for_status()
        print('Notification sent successfully.')
    except requests.exceptions.RequestException as err:
            print(f'Failed to send notification: {err}')

