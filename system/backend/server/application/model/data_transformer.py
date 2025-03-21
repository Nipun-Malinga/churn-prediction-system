from application import db
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

class Data_Transformer(db.Model):
    __tablename__ = 'data_transformer'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Relationship
    data_transformer_info: Mapped[list["Data_Transformer_Info"]] = relationship(
        back_populates='data_transformer', 
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'Data_Transformer(name = {self.name})'