from extensions import db
from sqlalchemy.orm import relationship


class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    picture_id = db.Column(db.Integer, db.ForeignKey('picture.id', ondelete='CASCADE'), 
                           nullable=False, unique=True, index=True)

    statistics = relationship("Statistics", uselist=False, backref="task")

    def __repr__(self):
        return f'<Picture ID is {self.picture_id})>'

    def to_dict(self):
        return {
            'picture_id': self.picture_id
        }

db.Index('idx_task_id', Task.id, unique=True)
