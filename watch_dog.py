import os
import time
import datetime as DT
import paramiko
import Config

date_config = Config.ConfigFile()
host, user, secret, port, key_filename, authorization_ssh = date_config.get_data_for_ssh_agent()
WATCH_DOG_DATA = '/var/www/html/watch_dog_data'

def load_dates_start_finish():
    if os.path.exists(WATCH_DOG_DATA):
        with open(WATCH_DOG_DATA, 'r') as f:
            return f.read().splitlines()
    return None

while True:
    dates = load_dates_start_finish()
    real_time = DT.datetime.now()
    if dates and len(dates) >= 2:
        Date_finish = dates[1]
        date_finish_dt = DT.datetime.strptime(Date_finish, '%Y-%m-%d %H:%M:%S')
        if real_time >= date_finish_dt:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host, username=user, password=secret, port=port)
            client.exec_command('ip/firewall/nat disable numbers=3')
            time.sleep(1)
            client.exec_command('/ip/firewall/filter/disable numbers=0')
            time.sleep(1)
            os.remove(WATCH_DOG_DATA)
            client.close()
    time.sleep(10)
