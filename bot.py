import os

from vk_api import *
from vk_api.longpoll import *
from auth import LOGIN, PASSWORD

print("Accountant-bot by davy1ex")
db_name = 'db.txt'


def first_start():
    if 'users_kick.txt' not in os.listdir():
        with open('users_kick.txt', 'w') as f:
            f.write('Беседу покинули:\n')
    if 'users_invite.txt' not in os.listdir():
        with open('users_invite.txt', 'w') as f:
            f.write('Добавились в беседу:\n')
    if db_name not in os.listdir():
        with open(db_name, "w") as f:
            f.write("")


def get_name_this_user(id=None):
    info = vk.users.get(fields="nickname", user_ids=id)
    first_name = info[0]["first_name"]
    last_name = info[0]["last_name"]

    return first_name + " " + last_name


def get_text_from_file(file):
    """
    возвращает текст из файла
    :param file: откуда нужно вернуть текст
    :return:
    """
    with open(file, 'r') as f:
        return f.read()


def delete_user(file, text):
    """
    удаляет пользователя из импровизированной базы данных
    :param file: файл бд
    :param text: кого надо удалить
    """
    # пример комманды: /удалить Вася Пупкин
    with open(file, "r") as f:
        text = text.split("/удалить ")[1]
        new_f_text = ""
        for line in f.readlines():
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


def clear_all_users(file, first_words=""):
    """
    Очищает бд
    :param file: файл бд
    :param first_words: слова, которые надо вставить вначало файла
    """
    with open(file, "w") as file:
        file.write(first_words)


# создание нужных файлов
first_start()

# авторизация
try:
    v = VkApi(login=LOGIN, password=PASSWORD)
    v.auth()
    lp = VkLongPoll(v)
    vk = v.get_api()
except Captcha:
    print("Лимит попыток авторизации исчерпан, заходи позже")
    exit()


name = get_name_this_user()

print("{0}: Авторизация прошла успешно".format(name))
print("Чтобы начать работу с ботом:\n"
      "\t1.Закиньте его в беседу;\n"
      "\t2. Напишите \"/помощь\";\n"
      "\t3. Наслаждайтесь.")


while True:
    for event in lp.listen():
        if event.type == VkEventType.MESSAGE_NEW and 'source_act' in event.raw[7]:
            name = get_name_this_user(event.raw[7]['source_mid'])
            if event.raw[7]['source_act'] == 'chat_kick_user' and \
                    name not in get_text_from_file('users_kick.txt'):
                with open('users_kick.txt', 'a') as f:
                    f.write(str(name + "\n"))
            elif event.raw[7]['source_act'] == 'chat_invite_user' and \
                    name not in get_text_from_file('users_invite.txt'):
                with open('users_invite.txt', 'a') as f:
                    f.write(str(name + "\n"))

        if event.type == VkEventType.MESSAGE_NEW and "/" in event.text and event.to_me and event.from_chat:
            text = event.text
            if "добавить" in text.lower():
                add_new_user(file=db_name, text=text)
                vk.messages.send(
                    chat_id=event.chat_id,
                    message="Готово.",
                    forward_messages=event.message_id
                )

            elif "помощь" in text.lower():
                vk.messages.send(
                    chat_id=event.chat_id,
                    message="Команды:"
                            "\n/добавить Вася Пупкин - добавляет Вася Пупкина в базу данных (дальше бд)\n"
                            "/покажи бд - показывает бд\n"
                            "/очистить бд - очищает бд\n"
                            "/удалить Вася Пупкин - удаляет Васю Пупкина из бд\n"
                            "/очисть кто ушёл - очищает списки тех, кто ушёл\n"
                            "/очистить кто пришёл - очищает списки тех, кто пришёл\n"
                            "/кто ушёл - показывает тех, кто ушёл\n"
                            "/кто пришёл - показывает тех, кто пришёл",
                    forward_messages=event.message_id
                )

            elif "покажи бд" in text.lower():
                with open(db_name, "r") as file:
                    vk.messages.send(
                        chat_id=event.chat_id,
                        message=file.read(),
                        forward_messages=event.message_id
                    )

            elif "очистить кто ушёл" in text.lower():
                clear_all_users(first_words='Беседу покинули:\n', file="users_kick.txt")
                vk.messages.send(
                    chat_id=event.chat_id,
                    message="Готово.",
                    forward_messages=event.message_id
                )

            elif "очистить кто пришёл" in text.lower():
                clear_all_users(first_words='Добавились в беседу:\n', file="users_invite.txt")
                vk.messages.send(
                    chat_id=event.chat_id,
                    message="Готово.",
                    forward_messages=event.message_id
                )

            elif "очистить бд" in text.lower():
                clear_all_users(db_name)
                message = "Готово."
                vk.messages.send(
                    chat_id=event.chat_id,
                    message=message,
                    forward_messages=event.message_id
                )

            elif "удалить" in text.lower():
                if len(text.lower().split()) > 1:
                    delete_user(db_name, text)
                    vk.messages.send(
                        chat_id=event.chat_id,
                        message="Готово.",
                        forward_messages=event.message_id
                    )
                else:
                    vk.messages.send(
                        chat_id=event.chat_id,
                        message="А удалить то мне кого?",
                        forward_messages=event.message_id
                    )

            elif "кто ушёл" in text.lower():
                vk.messages.send(
                    chat_id=event.chat_id,
                    message=get_text_from_file('users_kick.txt'),
                    forward_messages=event.message_id
                )

            elif "кто пришёл" in text.lower():
                vk.messages.send(
                    chat_id=event.chat_id,
                    message=get_text_from_file('users_invite.txt'),
                    forward_messages=event.message_id
                )
