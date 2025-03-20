from application import db
from sqlalchemy import String, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship

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

    def __repr__(self):
        return f'Model(name = {self.name})'