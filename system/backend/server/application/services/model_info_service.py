from application import db
from application.models import Accuracy_Drift, Model, Model_Info
from sqlalchemy import desc
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.orm import aliased
from sqlalchemy.sql import desc, func
from application.models import Evaluation_Threshold


# TODO: Build DTO class for necessary endpoints
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

        try:
            results = (
                db.session.query(Model_Info)
                .filter(
                    Model_Info.model_id == model_id,
                    Model_Info.is_production_model == True,
                )
                .all()
            )

            return [r.to_dict() for r in results] if results else []
        except SQLAlchemyError as ex:
            raise SQLAlchemyError(
                "Failed to fetch model information from database"
            ) from ex

    @classmethod
    def get_basic_model_info(cls):
        try:
            latest_info_subq = (
                db.session.query(
                    Model_Info.model_id,
                    func.max(Model_Info.updated_date).label("latest_date"),
                )
                .group_by(Model_Info.model_id)
                .filter(Model_Info.is_production_model == True)
                .subquery()
            )

            LatestModelInfo = aliased(Model_Info)

            results = (
                db.session.query(
                    Model.id,
                    Model.name,
                    Model.base_model,
                    LatestModelInfo.accuracy,
                    LatestModelInfo.updated_date,
                )
                .join(LatestModelInfo, Model.id == LatestModelInfo.model_id)
                .join(
                    latest_info_subq,
                    (LatestModelInfo.model_id == latest_info_subq.c.model_id)
                    & (LatestModelInfo.updated_date == latest_info_subq.c.latest_date),
                )
                .all()
            )

            model_info = []
            for result in results:
                id, name, base_model, accuracy, updated_date = result
                model_info.append(
                    {
                        "id": id,
                        "name": name,
                        "base_model": base_model,
                        "accuracy": accuracy,
                        "updated_date": (
                            updated_date.isoformat() if updated_date else None
                        ),
                    }
                )

            return model_info
        except SQLAlchemyError as ex:
            raise SQLAlchemyError(
                "An error occurred while retrieving basic model information."
            ) from ex

    def get_advanced_model_info(cls, model_id):
        try:
            result = (
                db.session.query(Model_Info)
                .filter(
                    Model_Info.model_id == model_id,
                    Model_Info.is_production_model == True,
                )
                .order_by(desc(Model_Info.updated_date))
                .limit(1)
                .one()
            )

            return result.to_dict() if result else {}
        except NoResultFound as ex:
            raise NoResultFound(f"Resource not found for model id: {model_id}") from ex
        except SQLAlchemyError as ex:
            raise SQLAlchemyError(
                "An error occurred while retrieving advanced model information."
            ) from ex

    @classmethod
    def get_base_model_performance(cls):
        try:
            result = (
                db.session.query(Model_Info)
                .join(Model, Model.id == Model_Info.model_id)
                .filter(
                    Model.base_model == True, Model_Info.is_production_model == True
                )
                .order_by(desc(Model_Info.updated_date))
                .limit(1)
                .one_or_none()
            )

            if result:
                return result.to_dict()
            else:
                # Graceful fallback instead of raising an exception
                return {"message": "No base model performance found."}

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

            results = (
                db.session.query(filter_by, Model_Info.updated_date)
                .filter(
                    Model_Info.model_id == model_id,
                    Model_Info.is_production_model == True,
                )
                .all()
            )

            return [
                {"data": result[0], "updated_date": result[1]} for result in results
            ]
        except SQLAlchemyError as ex:
            raise SQLAlchemyError(
                "An error occurred while retrieving model performance history."
            ) from ex

    @classmethod
    def model_drift_history(cls):
        try:
            results = (
                db.session.query(Accuracy_Drift)
                .join(
                    Model_Info,
                    Model_Info.id == Accuracy_Drift.model_info_id,
                )
                .filter(Model_Info.is_production_model == True)
                .all()
            )

            return [r.to_dict() for r in results] if results else []
        except SQLAlchemyError as ex:
            raise SQLAlchemyError(
                "An error occurred while retrieving model drift history."
            ) from ex

    @classmethod
    def new_trained_models(cls):
        try:
            results = (
                db.session.query(Model, Model_Info)
                .join(Model_Info, Model.id == Model_Info.model_id)
                .filter(
                    Model.base_model == True,
                    Model_Info.is_production_model == False,
                )
                .order_by(desc(Model_Info.updated_date))
                .limit(1)
                .one_or_none()
            )

            if not results:
                return None

            model, info = results

            return {
                "batch_id": info.batch_id,
                "model_name": model.name,
                "version_name": info.version_name,
                "accuracy": info.accuracy,
                "precision": info.precision,
                "recall": info.recall,
                "f1_score": info.f1_score,
                "is_production_model": info.is_production_model,
                "trained_date": info.updated_date,
            }
        except SQLAlchemyError as ex:
            raise SQLAlchemyError(
                "An error occurred while retrieving new trained models."
            ) from ex

    @classmethod
    def production_model(cls, batch_id):
        session = db.session()
        try:
            selected_models = (
                session.query(Model_Info).filter(Model_Info.batch_id == batch_id).all()
            )

            if not selected_models:
                raise NoResultFound(f"No results found for batch id: {batch_id}")

            response = []
            for model in selected_models:
                model.is_production_model = True
                response.append(model.to_dict())

            session.commit()
            return response

        except NoResultFound as ex:
            session.rollback()
            raise NoResultFound(f"Resource not found for batch id: {batch_id}") from ex
        except SQLAlchemyError as ex:
            session.rollback()
            raise SQLAlchemyError(
                "An error occurred while setting production models."
            ) from ex
        finally:
            session.close()

    @classmethod
    def set_threshold(cls, thresholds):
        session = db.session()
        try:
            existing = session.query(Evaluation_Threshold).first()
            if existing:
                existing.accuracy = thresholds["accuracy"]
                existing.precision = thresholds["precision"]
                existing.recall = thresholds["recall"]
                existing.f1_score = thresholds["f1_score"]
                session.commit()
                return existing.to_dict()
            else:
                new_data_entry = Evaluation_Threshold(**thresholds)
                session.add(new_data_entry)
                session.commit()
                return new_data_entry.to_dict()
        except SQLAlchemyError as ex:
            session.rollback()
            raise RuntimeError(
                "An error occurred while setting evaluation thresholds."
            ) from ex
        finally:
            session.close()

    @classmethod
    def get_threshold(cls):
        session = db.session()
        try:
            existing = session.query(Evaluation_Threshold).first()
            if existing:
                return existing.to_dict()
            default_thresholds = {
                "accuracy": -15,
                "precision": -10,
                "recall": -10,
                "f1_score": -10,
            }
            return default_thresholds
        except SQLAlchemyError as ex:
            raise RuntimeError(
                "An error occurred while fetching evaluation thresholds."
            ) from ex
        finally:
            session.close()
