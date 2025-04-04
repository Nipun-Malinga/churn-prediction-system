from application import db
from application.model import Evaluation_Data

class Evaluation_Data_Service:

    @classmethod
    def save_evaluation_data(cls, data):
        new_data_entry = Evaluation_Data(**data)
        db.session.add(new_data_entry)
        db.session.commit()
        return new_data_entry