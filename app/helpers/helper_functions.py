from .db_helper import (_save_picture, _save_choise,
                        _create_new_task)


def save_pictures(pictures: str, uuid: str):
    for picture in pictures:
        picture_id = _save_picture(picture.read(), uuid)
        _create_new_task(picture_id)


def save_choices(choices: str, uuid: str):
    for choice in choices.split(','):
        _save_choise(choice, uuid)
