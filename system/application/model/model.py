from application import db
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

class Model(db.Model):
    __tablename__ = 'model'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    model_info = relationship('model_info', back_populates='model')

    def __repr__(self):
        return f'Model(name = {self.name})'