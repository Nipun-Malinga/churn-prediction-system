from os.path import abspath, dirname, join

import joblib
from application import db
from application.models import Model, Model_Info
from sqlalchemy import desc
from sqlalchemy.exc import NoResultFound

ABS_DIR = dirname(abspath(__file__))
BASE_DIR = join(ABS_DIR, "trained_models/")

ML_MODEL_PATH = join(BASE_DIR, "ml_models/")


def make_prediction(preprocessed_data):

    try:
        result = (
            db.session.query(Model.name)
            .join(Model_Info, Model.id == Model_Info.model_id)
            .where(
                Model.base_model == True,
                Model_Info.is_production_model == True,
            )
            .order_by(desc(Model_Info.updated_date))
            .limit(1)
            .one()
        )

        voting_classifier = joblib.load(join(ML_MODEL_PATH, f"{result[0]}.pkl"))

        y_pred_proba = voting_classifier.predict_proba(preprocessed_data)
        positive_class_proba = y_pred_proba[:, 1]
        # TODO: Develop Dynamic Probability threshold tuner
        prediction = (positive_class_proba >= 0.3).astype(int)

        return prediction.tolist(), positive_class_proba.tolist()

    except NoResultFound as ex:
        raise NoResultFound("Currently there are no trained models available.") from ex
    except ValueError as ex:
        raise ValueError("System cannot make predictions for untrained data.") from ex
