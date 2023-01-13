from extensions import db


class Statistics(db.Model):
    __tablename__ = 'statistics'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'),
                        nullable=False, unique=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id', ondelete='CASCADE'),
                        nullable=False, unique=False)
    choice_id = db.Column(db.Integer, db.ForeignKey('classes.id', ondelete='CASCADE'),
                        nullable=False, unique=False)

    def __repr__(self):
        return f'<User {self.user_id})>'

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'task_id': self.task_id,
            'choice_id': self.choice_id
        }
