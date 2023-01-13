from extensions import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class Classes(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    choice = db.Column(db.String(255), nullable=False)
    uuid = db.Column(UUID(as_uuid=True), nullable=True)

    statistics = relationship("Statistics", uselist=False, backref="classes")

    def __repr__(self):
        return f'<uuid {self.uuid})>'

    def to_dict(self):
        return {
            'choice': self.choice,
            'uuid': self.uuid
        }

db.Index('idx_classes_id', Classes.id, unique=True)
