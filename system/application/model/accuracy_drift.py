import datetime
from application import db
from sqlalchemy.orm import mapped_column, Mapped, Relationship
from sqlalchemy import ForeignKey, DateTime

class Accuracy_Drift(db.Model):
    __tablename__ = 'accuracy_drift'

    id: Mapped[int] = mapped_column(primary_key=True)
    model_info_id: Mapped[int] = mapped_column(ForeignKey('model_info.id'), nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    accuracy: Mapped[float] = mapped_column(nullable=False, default=0)
    drift: Mapped[float] = mapped_column(nullable=False, default=0)
    model_info = Relationship("model_info", back_populates='accuracy_drift')