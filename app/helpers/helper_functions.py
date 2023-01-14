import random
import string

from helpers.db_helper import (save_picture, save_choise,
                               create_new_task)


def save_pictures(pictures: str, uuid: str):
    for picture in pictures:
        picture_id = save_picture(picture.read(), uuid)
        create_new_task(picture_id)


def save_choices(choices: str, uuid: str):
    for choice in choices.split(','):
        save_choise(choice, uuid)


def generate_login_password():
    login_source = string.ascii_letters + string.digits
    password_source = string.digits
    login = "Zero_" + ''.join((random.choice(login_source) for i in range(3)))
    password = "Bot_" + ''.join(random.choice(password_source) for i in range(3))
    return login, password
