class ConfigFile:
    def __init__(self):
        self.host = ''
        self.user = ''
        self.secret = ''
        self.port = '22'
        self.key_filename = '/home/ssh_user/id_rsa'
        self.authorization_ssh = 'man'
        self.apy_key = ''
        self.id_chat = 

    def get_data_for_ssh_agent(self):
        return self.host, self.user, self.secret, self.port, self.key_filename, self.authorization_ssh  
    def get_data_for_watch_dog(self):
        return self.host, self.user, self.secret, self.port, self.key_filename, self.authorization_ssh
    def get_data_for_telebot(self):
        return self.apy_key, self.id_chat
