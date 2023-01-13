from extensions import db
from models import Users, Classes, Statistics, Picture, Task


def _save_picture(picture: str, uuid: str):
    picture = Picture(picture=picture, uuid=uuid)
    db.session.add(picture)
    db.session.flush()
    return picture.id


def _save_choise(choice: str, uuid: str):
    choice = Classes(choice=choice, uuid=uuid)
    db.session.add(choice)
    db.session.commit()


def _get_pictures_count():
    pictures_count = Picture.query.count()
    return pictures_count


def _get_labeled_count():
    labeled_count = Statistics.query.count()
    return labeled_count


def _create_new_task(picture_id: int):
    task = Task(picture_id=picture_id)
    db.session.add(task)
    db.session.commit()


def _get_statistics():
    query = """SELECT count(*), choice 
                 FROM classes as cl 
                 JOIN statistics as st
                   ON cl.id = st.choice_id
             GROUP BY choice
             ORDER BY count(*)"""
    choice_list = db.session.execute(query).all()
    return choice_list
