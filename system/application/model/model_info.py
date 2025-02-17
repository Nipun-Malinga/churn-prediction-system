import datetime
from application import db
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, DateTime

# Stores the model details
class Model_Info(db.Model):
    __tablename__ = 'model_info'

    id: Mapped[int] = mapped_column(primary_key=True)
    model_id: Mapped[int] = mapped_column(ForeignKey('model.id'), nullable=False)
    updated_date: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    accuracy: Mapped[float] = mapped_column(nullable=False, default=0)
    # Confusion matrix data
    TP:Mapped[int] = mapped_column(nullable= False, default=0)
    TN:Mapped[int] = mapped_column(nullable= False, default=0)
    FP:Mapped[int] = mapped_column(nullable= False, default=0)
    FN:Mapped[int] = mapped_column(nullable= False, default=0)
    precision:Mapped[int] = mapped_column(nullable= False, default=0)
    recall:Mapped[int] = mapped_column(nullable= False, default=0)
    f1_score:Mapped[int] = mapped_column(nullable= False, default=0)
    model = relationship('model', back_populates='model_info')
