import datetime
from application import db
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Float, ForeignKey, DateTime

class Accuracy_Drift(db.Model):
    __tablename__ = 'accuracy_drift'

    id: Mapped[int] = mapped_column(primary_key=True)
    model_info_id: Mapped[int] = mapped_column(ForeignKey('model_info.id'), nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    accuracy: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    drift: Mapped[float] = mapped_column(Float, nullable=False, default=0)

    # Relationship
    model_info: Mapped["Model_Info"] = relationship(back_populates='accuracy_drift')

    def __repr__(self):
        return f'Accuracy_Drift(model_info_id = {self.model_info_id}, date = {self.date}, accuracy = {self.accuracy}, drift = {self.drift})'
