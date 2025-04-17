from application import db
from application.model import Model, Model_Info
from flask import abort
from sqlalchemy import desc
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import aliased
from sqlalchemy.sql import desc, func

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

    from sqlalchemy.orm import aliased

    @classmethod
    def get_basic_model_info(cls):
        latest_info_subq = db.session.query(
            Model_Info.model_id,
            func.max(Model_Info.updated_date).label('latest_date')
        ).group_by(
            Model_Info.model_id
        ).subquery()

        LatestModelInfo = aliased(Model_Info)

        results = db.session.query(
            Model.id,
            Model.name,
            Model.base_model,
            LatestModelInfo.accuracy,
            LatestModelInfo.updated_date
        ).join(
            LatestModelInfo, Model.id == LatestModelInfo.model_id
        ).join(
            latest_info_subq,
            (LatestModelInfo.model_id == latest_info_subq.c.model_id) &
            (LatestModelInfo.updated_date == latest_info_subq.c.latest_date)
        ).all()

        model_info = []
        for result in results:
            id, name, base_model, accuracy, updated_date = result
            model_info.append({
                "id": id,
                "name": name,
                "base_model": base_model,
                "accuracy": accuracy,
                "updated_date": updated_date.isoformat() if updated_date else None
            })

        return model_info
  
    def get_advanced_model_info(cls, model_id):
        try:
            result = db.session.query(
                Model_Info
            ).filter(
                Model_Info.model_id == model_id
            ).order_by(
                desc(
                    Model_Info.updated_date
                )
            ).limit(1).one()     

            return result.to_dict() if result else {}
        except NoResultFound as ex:
            raise NoResultFound from ex
        
    """
        Chart Data Services
    """    
    
    @classmethod
    def model_performance_history(cls, model_id, filter):
        
        match filter:
            case "accuracy":
                filter_by = Model_Info.accuracy
            case "precision":
                filter_by = Model_Info.precision
            case "recall":
                filter_by = Model_Info.recall
            case "f1_score":
                filter_by = Model_Info.f1_score
        
        results = db.session.query(
            filter_by, Model_Info.updated_date
        ).filter(
            Model_Info.model_id == model_id
        ).all()
        
        return [
            {
            "data": result[0],
            "updated_date": result[1]
            }
            for result in results
        ]