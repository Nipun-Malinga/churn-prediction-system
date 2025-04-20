from application import db
from application.model import Accuracy_Drift, Model, Model_Info
from sqlalchemy import desc
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.orm import aliased
from sqlalchemy.sql import desc, func


class Model_Info_Service:
    
    @classmethod
    def get_all_models(cls):
        try:
            return [
                {
                    **Model.to_dict(),
                }
                for Model in db.session.query(Model).all()
            ]
        except SQLAlchemyError as ex:
            raise SQLAlchemyError(
                "An error occurred while retrieving ML model information."
            ) from ex
        
    @classmethod
    def get_model_info(cls, model_id):
        
        results = db.session.query(
            Model_Info
        ).filter(
            Model_Info.model_id == model_id
        ).all()
    
        return [r.to_dict() for r in results] if results else []
    
    @classmethod
    def get_basic_model_info(cls):
        try:
            latest_info_subq = db.session.query(
                Model_Info.model_id,
                func.max(Model_Info.updated_date).label("latest_date")
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
        except SQLAlchemyError as ex:
            raise SQLAlchemyError(
                "An error occurred while retrieving basic model information."
            ) from ex
  
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
        except SQLAlchemyError as ex:
            raise SQLAlchemyError(
                "An error occurred while retrieving advanced model information."
            ) from ex
        
    @classmethod
    def get_base_model_performance(cls):
        try:
            result = db.session.query(
                Model_Info
            ).join(
                Model, Model.id == Model_Info.model_id
            ).filter(
              Model.base_model == True, 
            ).order_by(
                desc(Model_Info.updated_date)
            ).limit(1).one()     

            return result.to_dict() if result else {}
        except NoResultFound as ex:
            raise NoResultFound from ex
        except SQLAlchemyError as ex:
            raise SQLAlchemyError(
                "An error occurred while retrieving base model performance."
            ) from ex

        
    """
        Chart Data Services
    """    
    
    @classmethod
    def model_performance_history(cls, model_id, filter):
        
        try:
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
        except SQLAlchemyError as ex:
            raise SQLAlchemyError(
                "An error occurred while retrieving model performance history."
            ) from ex
        
    @classmethod
    def model_drift_history(cls):
        try:
            results = db.session.query(
                Accuracy_Drift
            ).all()

            return [r.to_dict() for r in results] if results else []
        except SQLAlchemyError as ex:
            raise SQLAlchemyError(
                "An error occurred while retrieving model drift history."
            ) from ex