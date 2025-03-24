import joblib
from os.path import join, dirname, abspath
from application import db
from application.model import Model

ABS_DIR = dirname(abspath(__file__))
BASE_DIR = join(ABS_DIR, "trained_models/")

ML_MODEL_PATH = join(BASE_DIR, "ml_models/")

def make_prediction(preprocessed_data):
    
    model_name_result = db.session.query(
        Model.name
    ).all()
         
    if not model_name_result:
        raise FileNotFoundError("Currently there are no trained encoders available.")
    
    for name in model_name_result:
        voting_classifier = joblib.load(join(ML_MODEL_PATH, f"{name[0]}.pkl"))

        prediction = voting_classifier.predict(preprocessed_data).tolist()
        probability = voting_classifier.predict_proba(preprocessed_data).tolist()

        return prediction, probability
    
    