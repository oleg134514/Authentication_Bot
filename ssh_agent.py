import paramiko
import time
import Config
import datetime as DT
import random

def ssh_agent(ip, command, name, phone):
    t_sleep = 60
    now = DT.datetime.now()
    start_time = now.strftime("%Y-%m-%d %H:%M:%S")
    finish_time = (now + DT.timedelta(seconds=t_sleep)).strftime("%Y-%m-%d %H:%M:%S")
    t_name = now.strftime("%Y-%m-%d-%H_%M_%S")
    r_name = random.randint(100, 1000)
    with open('/var/www/html/watch_dog_data', 'w') as text_file:
        text_file.write(f"{start_time}\n{finish_time}\n{name} {phone} {ip}\n")

    date_config = Config.ConfigFile()
    host, user, secret, port, key_filename, authorization_ssh = date_config.get_data_for_ssh_agent()

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if authorization_ssh == 'man':
        client.connect(hostname=host, username=user, password=secret, port=port)
    else:
        client.connect(hostname=host, username=user, key_filename=key_filename, port=port)

    command_mapping = {
        "BAN (Add Black List)": [f'/ip/firewall/filter/add chain=input src-address={ip} action=drop'],
        "WEB_80": [
            'ip/firewall/nat/set action=dst-nat to-addresses=192.168.100.100 to-ports=80 protocol=tcp port=80 in-interface=ether3 numbers=3 dst-port=80',
            'ip/firewall/nat enable numbers=3',
            f'/ip/firewall/filter/set chain=input protocol=tcp port=80 src-address={ip} action=accept numbers=0',
            '/ip/firewall/filter/enable numbers=0'
        ],
        "WEB_443": [
            'ip/firewall/nat/set action=dst-nat to-addresses=192.168.100.100 to-ports=443 protocol=tcp port=443 in-interface=ether3 numbers=3 dst-port=443',
            'ip/firewall/nat enable numbers=3',
            f'/ip/firewall/filter/set chain=input protocol=tcp port=443 src-address={ip} action=accept numbers=0',
            '/ip/firewall/filter/enable numbers=0'
        ],
        "FTP": [
            'ip/firewall/nat/set action=dst-nat to-addresses=192.168.100.100 to-ports=21 protocol=tcp port=21 in-interface=ether3 numbers=3 dst-port=21',
            'ip/firewall/nat enable numbers=3',
            f'/ip/firewall/filter/set chain=input protocol=tcp port=21 src-address={ip} action=accept numbers=0',
            '/ip/firewall/filter/enable numbers=0'
        ],
        "SFTP": [
            'ip/firewall/nat/set action=dst-nat to-addresses=192.168.100.100 to-ports=22 protocol=tcp port=22 in-interface=ether3 numbers=3 dst-port=22',
            'ip/firewall/nat enable numbers=3',
            f'/ip/firewall/filter/set chain=input protocol=tcp port=22 src-address={ip} action=accept numbers=0',
            '/ip/firewall/filter/enable numbers=0'
        ],
        "FTPS": [
            'ip/firewall/nat/set action=dst-nat to-addresses=192.168.100.100 to-ports=990 protocol=tcp port=990 in-interface=ether3 numbers=3 dst-port=990',
            'ip/firewall/nat enable numbers=3',
            f'/ip/firewall/filter/set chain=input protocol=tcp port=990 src-address={ip} action=accept numbers=0',
            '/ip/firewall/filter/enable numbers=0'
        ]
    }
    commands = command_mapping.get(command, [])

    for cmd in commands:
        client.exec_command(cmd)
        time.sleep(1)

    client.close()
