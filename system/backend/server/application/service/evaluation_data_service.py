from application import db
from application.model import Evaluation_Data
from application.util import csv_data_preprocessor

class Evaluation_Data_Service:

    @classmethod
    def save_evaluation_data(cls, data):
        new_data_entry = Evaluation_Data(**data)
        db.session.add(new_data_entry)
        db.session.commit()
        return new_data_entry
    
    @classmethod
    def preprocess_csv_data(cls, csv_data):
        try:
            return csv_data_preprocessor(csv_data)
        except ValueError as ex:
            raise ValueError(ex) from ex