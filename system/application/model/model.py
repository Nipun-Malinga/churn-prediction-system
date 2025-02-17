from application import db
from sqlalchemy.orm import mapped_column, Mapped, relationship

class Model(db.Model):
    __tablename__ = 'model'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    model_info = relationship('model_info', back_populates='model')