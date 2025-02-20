from datetime import datetime
from application import db
from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

class Evaluation_Data(db.Model):
    __tablename__ = 'evaluation_data'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    added_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now) 
    education: Mapped[str] = mapped_column(String(50), nullable=False)
    credit_score: Mapped[float] = mapped_column(nullable=False)
    geography: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[float] = mapped_column(nullable=False)
    tenure: Mapped[float] = mapped_column(nullable=False)
    balance: Mapped[float] = mapped_column(nullable=False)
    num_of_products: Mapped[int] = mapped_column(nullable=False)
    has_cr_card: Mapped[int] = mapped_column(nullable=False)
    card_type: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active_member: Mapped[int] = mapped_column(nullable=False)
    estimated_salary: Mapped[float] = mapped_column(nullable=False)
    housing: Mapped[str] = mapped_column(String(25), nullable=False)
    loan: Mapped[str] = mapped_column(String(25), nullable=False)
    exited: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self):
        return (f"Evaluation_Data(credit_score={self.credit_score}, "
                f"age={self.age}, balance={self.balance}, "
                f"num_of_products={self.num_of_products}, "
                f"is_active_member={self.is_active_member}, exited={self.exited})")
