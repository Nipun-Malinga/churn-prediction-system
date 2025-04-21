from os.path import abspath, dirname, join

import joblib
from application import db
from application.model import Model, Model_Info

ABS_DIR = dirname(abspath(__file__))
BASE_DIR = join(ABS_DIR, "trained_models/")

ML_MODEL_PATH = join(BASE_DIR, "ml_models/")

def make_prediction(preprocessed_data):
     
    try:
        result = db.session.query(
            Model.name
        ).join(
            Model_Info, Model.id == Model_Info.model_id
        ).where(
            Model.base_model == True,
            Model_Info.is_production_model == True
        ).one_or_none()
        
        if not result:
            raise FileNotFoundError(
                "Currently there are no trained models available."
            )

        voting_classifier = joblib.load(join(ML_MODEL_PATH, f"{result[0]}.pkl"))

        prediction = voting_classifier.predict(preprocessed_data).tolist()
        probability = voting_classifier.predict_proba(preprocessed_data).tolist()

        return prediction, probability  
                 
    except FileNotFoundError as ex:
        raise ex
    except ValueError as ex:
        raise ValueError from ex