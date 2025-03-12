import paramiko
import time
#authorization_ssh = 'man'
authorization_ssh = 'sert'
if authorization_ssh == 'man':
    host = ''
    user = ''
    secret = ''
    port = 22
    open_fier = '19.19.19.19'
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.connect(hostname=host, username=user, password=secret, port=port)
    stdin, stdout, stderr = client.exec_command('ip/firewall/nat/set action=dst-nat to-addresses=192.168.100.100 to-ports=80 protocol=tcp port=80 in-interface=ether3  numbers=3 dst-port=80')
    time.sleep(1)
    stdin, stdout, stderr = client.exec_command('ip/firewall/nat enable numbers=3')
    time.sleep(1)
    stdin, stdout, stderr = client.exec_command('/ip/firewall/filter/set chain=input protocol=tcp port=8080 src-address={open_fief} action=accept numbers=0')
    time.sleep(1)
    stdin, stdout, stderr = client.exec_command('/ip/firewall/filter/enable numbers=0')
    time.sleep(60)
    stdin, stdout, stderr = client.exec_command('ip/firewall/nat disable numbers=3')
    time.sleep(1)
    stdin, stdout, stderr = client.exec_command('/ip/firewall/filter/disable numbers=0')
    data = stdout.read() + stderr.read()
    #data = stdout.read() + stderr.read()
    client.close()
    #print (data)
else:
    host = ''
    user = ''
    port = 22
    key_filename = 'path/to/your/id_rsa'  # Замените на путь к вашему приватному ключу
    open_fier = '19.19.19.19'
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.WarningPolicy()) #Более безопасный вариант, но нужно будет подтвердить ключ при первом подключении.
    client.connect(hostname=host, username=user, key_filename=key_filename, port=port)
    stdin, stdout, stderr = client.exec_command('ip/firewall/nat/set action=dst-nat to-addresses=192.168.100.100 to-ports=80 protocol=tcp port=80 in-interface=ether3  numbers=3 dst-port=80')
    time.sleep(1)
    stdin, stdout, stderr = client.exec_command('ip/firewall/nat enable numbers=3')
    time.sleep(1)
    stdin, stdout, stderr = client.exec_command('/ip/firewall/filter/set chain=input protocol=tcp port=8080 src-address={open_fief} action=accept numbers=0')
    time.sleep(1)
    stdin, stdout, stderr = client.exec_command('/ip/firewall/filter/enable numbers=0')
    time.sleep(60)
    stdin, stdout, stderr = client.exec_command('ip/firewall/nat disable numbers=3')
    time.sleep(1)
    stdin, stdout, stderr = client.exec_command('/ip/firewall/filter/disable numbers=0')
    data = stdout.read() + stderr.read()
    client.close()
    print(data.decode()) #Добавлена декодировка для корректного вывода
