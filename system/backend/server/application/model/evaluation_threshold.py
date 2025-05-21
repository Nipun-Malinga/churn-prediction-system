from datetime import datetime
from application import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Evaluation_Threshold(db.Model):
    __tablename__ = 'evaluation_threshold'

    id: Mapped[int] = mapped_column(primary_key=True)
    accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    precision: Mapped[int] = mapped_column(Integer, nullable=False)
    recall: Mapped[str] = mapped_column(Integer, nullable=False)
    f1_score: Mapped[str] = mapped_column(Integer, nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "accuracy": self.accuracy,
            "precision": self.precision,
            "recall": self.recall,
            "f1_score": self.f1_score
        }

    def __repr__(self) -> str:
        return (
            f"EvaluationThreshold("
            f"accuracy={self.accuracy}, "
            f"precision={self.precision}, "
            f"recall='{self.recall}', "
            f"f1_score='{self.f1_score}')"
        )
