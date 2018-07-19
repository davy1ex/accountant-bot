from getpass import getpass
from vk_api import *

while True:
    LOGIN = input("Логин: ")
    PASSWORD = getpass("Пароль: ")
    try:
        v = VkApi(login=LOGIN, password=PASSWORD)
        v.auth()
        with open("auth.py", "w") as f:
            f.write("".format(LOGIN, PASSWORD))
        break
    except BadPassword:
        print("Неверный логин или пароль")
