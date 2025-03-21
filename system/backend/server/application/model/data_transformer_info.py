import datetime
from application import db
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, DateTime

# Stores the model details
class Data_Transformer_Info(db.Model):
    __tablename__ = 'data_transformer_info'

    id: Mapped[int] = mapped_column(primary_key=True)
    data_transformer_id: Mapped[int] = mapped_column(ForeignKey('data_transformer.id'))
    updated_date: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    version_name: Mapped[str] = mapped_column(String, nullable= True)

    # Relationships
    data_transformer: Mapped["Data_Transformer"] = relationship(back_populates='data_transformer_info')  

    def __repr__(self):
        return f'Data_Transformer_Info(data_transformer_id = {self.data_transformer_id}, version_name = {self.version_name})'
                
