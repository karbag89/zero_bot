from extensions import db
from models import Users, Classes, Statistics, Picture, Task
from werkzeug.security import generate_password_hash
from sqlalchemy import func


def create_user(username: str, password: str, telegram_user: str):
    password_hash = generate_password_hash(password)
    user = Users(username=username, password=password_hash,
                 telegram_user=telegram_user)
    db.session.add(user)
    db.session.commit()
    return user


def create_new_task(picture_id: int):
    task = Task(picture_id=picture_id)
    db.session.add(task)
    db.session.commit()


def create_statistics(user_id: str, task_id: str, choice_id: str):
    choises = Statistics(user_id=user_id, task_id=task_id,
                         choice_id=choice_id)
    db.session.add(choises)
    db.session.commit()
    return choises


def save_picture(picture: str, uuid: str):
    picture = Picture(picture=picture, uuid=uuid)
    db.session.add(picture)
    db.session.flush()
    return picture.id


def save_choise(choice: str, uuid: str):
    choice = Classes(choice=choice, uuid=uuid)
    db.session.add(choice)
    db.session.commit()


def get_pictures_count():
    pictures_count = Picture.query.count()
    return pictures_count


def get_labeled_count():
    labeled_count = Statistics.query.count()
    return labeled_count

def get_statistics():
    choice_list = db.session.query(Classes.choice, func.count(Classes.choice)) \
                            .join(Statistics, Classes.id == Statistics.choice_id) \
                            .group_by(Classes.choice) \
                            .order_by(func.count(Classes.choice)).all()
    return choice_list


def get_other_statistics():
    return Statistics.query.filter(Statistics.choice_id == 0).count()


def get_user(telegram_user: str):
    user = Users.query.filter(Users.telegram_user==telegram_user) \
                      .one_or_none()
    return user


def get_picture_by_task_id(picture_id: int):
    new_picture = Picture.query.join(Task, Picture.id == picture_id) \
                               .one_or_none()
    return new_picture


def get_new_task(user_id):
    query = """SELECT * 
                 FROM Task as tk 
                WHERE tk.id not in (select task_id from Statistics 
         WHERE EXISTS (SELECT st.id
                FROM Statistics as st WHERE st.user_id = '{}')
          AND Statistics.user_id = '{}') LIMIT 1""".format(user_id, user_id)
    new_task = db.session.execute(query).one_or_none()
    return new_task


def get_all_choices(picture_id: str):
    choice_list = db.session.query(Classes.choice) \
                    .join(Picture, Classes.uuid == Picture.uuid) \
                    .filter(Picture.id == picture_id).all()
    return choice_list


def get_choice_id(picture_id, choice):
    choice_id = db.session.query(Classes.id) \
                    .join(Picture, Classes.uuid == Picture.uuid) \
                    .filter(Picture.id == picture_id, 
                            Classes.choice == choice).one_or_none()
    return choice_id
