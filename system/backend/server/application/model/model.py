from application import db
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Model(db.Model):
    __tablename__ = 'model'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    base_model: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relationship
    model_info: Mapped[list["Model_Info"]] = relationship(
        back_populates='model', 
        cascade="all, delete-orphan"
    )
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "base_model": self.base_model
        }

    def __repr__(self):
        return f'Model(name = {self.name})'