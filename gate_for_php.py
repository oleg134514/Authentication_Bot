import sys
import subprocess

name = sys.stdin.readline().strip()
phone = sys.stdin.readline().strip()
ip = sys.stdin.readline().strip()

class CateFile:
    def __init__(self):
        self.name = name
        self.phone = phone
        self.ip = ip

    def get_data_for_telebot(self):
        return self.name, self.phone, self.ip
    def get_data_for_ssh_agent(self):
        return self.name, self.phone, self.ip

cate = CateFile()
name, phone, ip = cate.get_data_for_telebot()

# Запускаем telebot.py асинхронно
subprocess.Popen(["python3", "telebot.py", name, phone, ip])

sys.exit(0)
