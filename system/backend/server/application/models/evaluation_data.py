from datetime import datetime

from application import db
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column


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
    
    def to_dict(self):
        return {
            "id": self.id,
            "added_date": self.added_date.isoformat() if self.added_date else None,
            "education": self.education,
            "credit_score": self.credit_score,
            "geography": self.geography,
            "gender": self.gender,
            "age": self.age,
            "tenure": self.tenure,
            "balance": self.balance,
            "num_of_products": self.num_of_products,
            "has_cr_card": self.has_cr_card,
            "card_type": self.card_type,
            "is_active_member": self.is_active_member,
            "estimated_salary": self.estimated_salary,
            "housing": self.housing,
            "loan": self.loan,
            "exited": self.exited,
        }


    def __repr__(self):
        return (f"Evaluation_Data(credit_score={self.credit_score}, "
                f"age={self.age}, balance={self.balance}, "
                f"num_of_products={self.num_of_products}, "
                f"is_active_member={self.is_active_member}, exited={self.exited})")
