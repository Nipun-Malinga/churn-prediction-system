import joblib
from os.path import join, dirname, abspath

def make_prediction(preprocessed_data):
    ABS_DIR = dirname(abspath(__file__))
    BASE_DIR = join(ABS_DIR, "trained_models\\")

    voting_classifier = joblib.load(join(BASE_DIR, "ml_models\\voting_classifier.pkl"))
    print(voting_classifier.predict_proba(preprocessed_data).tolist())
    return [0]