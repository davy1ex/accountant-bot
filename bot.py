from getpass import getpass

from vk_api import *
from vk_api.longpoll import *
from vk_api import exceptions

print("Accountant-bot by davy1ex")


def get_me(vk):
    """ получает имя авторизовавшегося пользователя"""
    info = vk.users.get(fields="nickname")
    return info


def delete_user(file, text):
    """
    удаляет пользователя из импровизированной базы данных
    :param file: файл бд
    :param text: кого надо удалить
    """
    # пример комманды: /удалить Вася Пупкин
    with open(file, "r") as f:
        text = text.split("/удалить ")[1]
        print("TEXT:", text)
        new_f_text = ""
        for line in f.readlines():
            print("LINE: " + line + "\n")
            if text not in line:
                new_f_text += line
    with open(file, "w") as f:
        f.write(new_f_text)


def add_new_user(file, text):
    """
    добавляет нового пользователя в бд
    :param file: файл бд
    :param text: кого надо добавить
    """
    # /добавить *
    with open(file, "a+") as f:
        text = text.split()
        text_for_add = ""
        for word in text:
            if "добавить" in word.lower():
                continue
            text_for_add += word + " "
        text_for_add += "\n"
        f.write(text_for_add)


def clear_all_users(file):
    """
    Очищает бд
    :param file: файл бд
    """
    with open(file, "w") as file:
        file.write("")


# авторизация

while True:
    login = input("Логин: ")
    password = getpass("Пароль: ")
    try:
        v = VkApi(login=login, password=password)
        v.auth()
        break
    except BadPassword:
        print("Неверный логин или пароль\n")

lp = VkLongPoll(v)
vk = v.get_api()

first_name = get_me(vk)[0]["first_name"]
last_name = get_me(vk)[0]["last_name"]
name = first_name + " " + last_name

print("{0}: Авторизация прошла успешно".format(name))

while True:
    for event in lp.listen():
        if event.type == VkEventType.MESSAGE_NEW and "/" in event.text and event.to_me and event.from_chat:
            text = event.text
            if "добавить" in text.lower():
                add_new_user(file="db.txt", text=text)
                vk.messages.send(
                    chat_id=event.chat_id,
                    message="Готово",
                    forward_messages=event.message_id
                )

            elif "помощь" in text.lower():
                vk.messages.send(
                    chat_id=event.chat_id,
                    message="Команды:"
                            "\n/добавить Вася Пупкин - добавляет Вася Пупкина в базу данных (дальше бд)\n"
                            "/покажи - показывает бд\n"
                            "/очистить - очищает бд\n"
                            "/удалить Вася Пупкин - удаляет Васю Пупкина из бд",
                    forward_messages=event.message_id
                )

            elif "покажи" in text.lower():
                with open("db.txt", "r") as file:
                    vk.messages.send(
                        chat_id = event.chat_id,
                        message=file.read(),
                        forward_messages=event.message_id
                    )

            elif "очистить" in text.lower():
                clear_all_users("db.txt")
                message = "Готово"
                vk.messages.send(
                    chat_id=event.chat_id,
                    message=message,
                    forward_messages=event.message_id
                )

            elif "удалить" in text.lower():
                delete_user("db.txt", text)
                vk.messages.send(
                    chat_id=event.chat_id,
                    message="Готово",
                    forward_messages=event.message_id
                )
