from application import db
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(25), nullable=False)

    def __repr__(self):
        return f'User(username = {self.username}, email = {self.email})'