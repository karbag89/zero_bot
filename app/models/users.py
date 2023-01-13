from extensions import db
from sqlalchemy.orm import relationship


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    telegram_user = db.Column(db.String(100), unique=True, nullable=False)

    statistics = relationship("Statistics", uselist=False, backref="users")

    def __repr__(self):
        return f'<User {self.username})>'

    def to_dict(self):
        return {
            'username': self.username,
            'telegram_user': self.telegram_user
        }

db.Index('idx_username', Users.username, unique=True)
db.Index('idx_telegram_user', Users.telegram_user, unique=True)
