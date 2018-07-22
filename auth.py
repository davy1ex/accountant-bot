from getpass import getpass
from vk_api import *

while True:
    LOGIN = input("Логин: ")
    PASSWORD = getpass("Пароль: ")
    try:
        v = VkApi(login=LOGIN, password=PASSWORD)
        v.auth()
        with open("auth.py", "w") as f:
            f.write("LOGIN = '{0}'\nPASSWORD = '{1}'\n".format(LOGIN, PASSWORD))
        break
    except BadPassword:
        print("Неверный логин или пароль")


# from getpass import getpass
# from vk_api import *
#
# while True:
#     LOGIN = str(input("Логин: "))
#     PASSWORD = str(getpass("Пароль: "))
#     try:
#         v = VkApi(login=LOGIN, password=PASSWORD)
#         v.auth()
#         with open("auth.py", 'w') as f:
#             f.write("LOGIN = '{0}', PASSWORD = '{1}'".format(LOGIN, PASSWORD)
#         break
#     except BadPassword:
#         print("Неверный логин или пароль")
