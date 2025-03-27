import requests
import json
import time
import os
import sys
import Config
import ssh_agent
import html

if len(sys.argv) != 4:
    sys.exit(1)

name = sys.argv[1]
phone = sys.argv[2]
ip = sys.argv[3]

date_config = Config.ConfigFile()
apy_key, id_chat = date_config.get_data_for_telebot()
url = f'https://api.telegram.org/bot{apy_key}'
request_timeout = 10
polling_delay = 5
offset_file = '/var/www/html/last_update_id.txt'

default_request_params = {'parse_mode': 'HTML'}

def load_last_update_id():
    if os.path.exists(offset_file):
        with open(offset_file, 'r') as f:
            return int(f.read().strip())
    return 0

def save_last_update_id(update_id):
    with open(offset_file, 'w') as f:
        f.write(str(update_id))

def send_message(text, reply_markup=None):
    data = {'chat_id': id_chat, 'text': text, **default_request_params}
    if reply_markup:
        data['reply_markup'] = json.dumps(reply_markup)
    requests.post(url + '/sendMessage', data=data, timeout=request_timeout).json()

def get_updates(offset=None):
    params = {'offset': offset} if offset is not None else {}
    return requests.get(url + '/getUpdates', params=params, timeout=request_timeout).json()

updates = get_updates()
last_update_id = max([update['update_id'] for update in updates['result']], default=0) + 1 if updates.get('ok', False) and updates.get('result') else 0

reply_markup = {
    "keyboard": [
        ["WEB_80", "WEB_443"],
        ["BAN (Add Black List)"],
        ["FTP", "SFTP", "FTPS"]
    ],
    "resize_keyboard": True,
    "one_time_keyboard": True
}

text_out_m = f'Запрос от {html.escape(phone)} {html.escape(name)}\nВыберите действие:'
send_message(text_out_m, reply_markup)

stop_polling = False
valid_commands = ["BAN (Add Black List)", "WEB_80", "WEB_443", "FTP", "SFTP", "FTPS"]

while not stop_polling:
    updates = get_updates(last_update_id)
    if updates.get('ok', False) and updates.get('result'):
        max_update_id = 0
        for update in updates['result']:
            update_id = update['update_id']
            max_update_id = max(max_update_id, update_id)
            if 'message' in update and 'text' in update['message']:
                message_text = update['message']['text'].strip()
                if message_text in valid_commands:
                    ssh_agent.ssh_agent(ip, message_text, name, phone)
                    stop_polling = True
                    break
        last_update_id = max_update_id + 1
        save_last_update_id(last_update_id)
    time.sleep(polling_delay)
