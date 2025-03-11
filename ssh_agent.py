import paramiko
import time
#authorization_ssh = man
authorization_ssh = sert

if authorization_ssh == man:
    host = ''
    user = ''
    secret = ''
    port = 22
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.connect(hostname=host, username=user, password=secret, port=port)
    stdin, stdout, stderr = client.exec_command('ls -l')
    time.sleep(1)
    stdin, stdout, stderr = client.exec_command('ls -l')
    time.sleep(1)
    #data = stdout.read() + stderr.read()
    client.close()
    #print (data)
else:
    host = ''
    user = 'your_username'
    port = 22
    key_filename = 'path/to/your/id_rsa'  # Замените на путь к вашему приватному ключу
    open_fier = 
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.WarningPolicy()) #Более безопасный вариант, но нужно будет подтвердить ключ при первом подключении.
    client.connect(hostname=host, username=user, key_filename=key_filename, port=port)
    stdin, stdout, stderr = client.exec_command('ls -l')
    time.sleep(1)
    stdin, stdout, stderr = client.exec_command('ls -l')
    time.sleep(1)
    data = stdout.read() + stderr.read()
    client.close()
    print(data.decode()) #Добавлена декодировка для корректного вывода
