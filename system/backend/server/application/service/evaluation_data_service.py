from application import db
from application.model import Evaluation_Data

def save_evaluation_data(data):
    new_data_entry = Evaluation_Data(**data)
    db.session.add(new_data_entry)
    db.session.commit()
    return new_data_entry


