from application import db
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, Float, ForeignKey

class Model_Hyper_Parameters(db.Model):
    __tablename__ = 'model_hyper_parameters'

    id: Mapped[int] = mapped_column(primary_key=True)
    model_info_id: Mapped[int] = mapped_column(ForeignKey('model_info.id'))
    learnning_rate: Mapped[float] = mapped_column(Float, nullable= True)
    reg_alpha: Mapped[float] = mapped_column(Float, nullable= True)
    reg_lambda: Mapped[float] = mapped_column(Float, nullable= True)
    n_estimators: Mapped[int] = mapped_column(Integer, nullable= True)
    max_depth: Mapped[int] = mapped_column(Integer, nullable= True)
    num_leaves: Mapped[int] = mapped_column(Integer, nullable= True)

    model_info: Mapped["Model_Info"] = relationship(back_populates="model_hyper_parameters")

    def __repr__(self):
        return f'Model_Hyper_Parameters(model_info_id = {self.model_info_id}, learnning_rate = {self.learnning_rate}, reg_lambda = {self.reg_lambda})'