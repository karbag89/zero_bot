from extensions import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Picture(db.Model):
    __tablename__ = 'picture'
    extend_existing=True

    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.Text)
    uuid = db.Column(UUID(as_uuid=True), nullable=False)

    task = relationship("Task", uselist=False, backref="picture")

    def __repr__(self):
        return f'<uuid {self.uuid})>'

    def to_dict(self):
        return {
            'picture': self.picture,
            'uuid': self.uuid
        }

db.Index('idx_picture_id', Picture.id, unique=True)
