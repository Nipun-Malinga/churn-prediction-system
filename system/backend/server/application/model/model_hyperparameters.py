from application import db
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, Float, JSON, ForeignKey

class Model_Hyperparameters(db.Model):
    __tablename__ = 'model_hyperparameters'

    id: Mapped[int] = mapped_column(primary_key=True)
    model_info_id: Mapped[int] = mapped_column(ForeignKey('model_info.id'))
    json_hyperparameters: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    model_info: Mapped["Model_Info"] = relationship(back_populates="model_hyperparameters")

    def __repr__(self):
        return f"""
            Model_Hyperparameters(
                model_info_id = {self.model_info_id},
                json_hyperparameters = {self.json_hyperparameters}
            )
        """