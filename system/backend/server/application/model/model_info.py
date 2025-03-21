import datetime
from application import db
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Float, Boolean, ForeignKey, DateTime

# Stores the model details
class Model_Info(db.Model):
    __tablename__ = 'model_info'

    id: Mapped[int] = mapped_column(primary_key=True)
    model_id: Mapped[int] = mapped_column(ForeignKey('model.id'))
    updated_date: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    accuracy: Mapped[float] = mapped_column(Float, nullable=False, default=0)

    # Confusion matrix data
    TP: Mapped[float] = mapped_column(Float, nullable= False, default=0)
    TN: Mapped[float] = mapped_column(Float, nullable= False, default=0)
    FP: Mapped[float] = mapped_column(Float, nullable= False, default=0)
    FN: Mapped[float] = mapped_column(Float, nullable= False, default=0)

    precision: Mapped[float] = mapped_column(Float, nullable= False, default=0)
    recall: Mapped[float] = mapped_column(Float, nullable= False, default=0)
    f1_score: Mapped[float] = mapped_column(Float, nullable= False, default=0)

    is_automated_tunning: Mapped[bool] = mapped_column(Boolean, default=False)
    is_downloaded: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)
    version_name: Mapped[str] = mapped_column(String)

    # Relationships
    model: Mapped["Model"] = relationship(back_populates='model_info')
    accuracy_drift: Mapped[list["Accuracy_Drift"]] = relationship(
        back_populates='model_info', 
        cascade="all, delete-orphan"
    )  
    model_hyper_parameters: Mapped["Model_Hyper_Parameters"] = relationship(back_populates='model_info')

    def __repr__(self):
        return f'Model_Info(model_id = {self.model_id}, updated_date = {self.updated_date}, accuracy = {self.accuracy})'
                
