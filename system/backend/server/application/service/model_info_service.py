from application import db
from application.model import Model, Model_Info
from flask import abort
from sqlalchemy import desc


class Model_Info_Service:
    
    @classmethod
    def get_all_models(cls):
        return [
            {
                **Model.to_dict(),
            }
            for Model in db.session.query(Model).all()
        ]
        
    @classmethod
    def get_model_info(cls, model_id):
        
        results = db.session.query(
            Model_Info
        ).filter(
            Model_Info.model_id == model_id
        ).all()
    
        return [r.to_dict() for r in results] if results else []
    
    from sqlalchemy import desc

    @classmethod
    def get_basic_model_info(cls, model_id):
        result = db.session.query(
            Model_Info.id,
            Model_Info.accuracy,
            Model_Info.updated_date
        ).filter(
            Model_Info.model_id == model_id
        ).order_by(
            desc(Model_Info.updated_date)
        ).limit(1).all()

        if not result:
            abort(400, f"No model info found for model_id={model_id}")

        model_info_id, accuracy, updated_date = result[0]

        return {
            "model_info_id": model_info_id,
            "accuracy": accuracy,
            "updated_date": updated_date.isoformat() if updated_date else None
        }     