from application import db
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from application.util import encrypt_password

class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    def __init__(self, username, email, password):
        self.username = username,
        self.email = email,
        self.password = encrypt_password(password)

    def __repr__(self):
        return f"""
        User(
            username = {self.username}, 
            email = {self.email}, 
            password = {self.password}
        )
        """