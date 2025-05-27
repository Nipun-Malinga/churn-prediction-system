from application import db
from application.models import Evaluation_Data
from application.utils import csv_data_preprocessor
from sqlalchemy import func, case, inspect
from sqlalchemy.exc import SQLAlchemyError

"""
    TODO: Add exception handing to every services
"""

class Evaluation_Data_Service:

    @classmethod
    def save_evaluation_data(cls, data):
        try:
            new_data_entry = Evaluation_Data(**data)
            db.session.add(new_data_entry)
            db.session.commit()
            return new_data_entry
        except SQLAlchemyError as ex:
            db.session.rollback()
            raise SQLAlchemyError(
                'An error occurred while adding data to the database.'
            ) from ex
    
    @classmethod
    def preprocess_csv_data(cls, csv_data):
        try:
            records = csv_data_preprocessor(csv_data)
            for entry in records:
                cls.save_evaluation_data(entry)
            return records
        except ValueError as ex:
            raise ValueError(ex) from ex
        
    @classmethod
    def basic_dataset_information(cls):
        try:
            num_of_rows = db.session.query(func.count()).select_from(Evaluation_Data).scalar()

            columns = inspect(db.engine).get_columns('evaluation_data')

            class_counts = db.session.query(
                func.sum(case((Evaluation_Data.exited == 0, 1), else_=0)).label("not_churned"),
                func.sum(case((Evaluation_Data.exited == 1, 1), else_=0)).label("churned")
            ).first()

            not_churned = class_counts.not_churned
            churned = class_counts.churned
            
            column_data = [
                {
                    "name": column.get('name'), 
                    "type": str(column.get('type'))
                }
                for column in columns
            ]
            
            sample_rows_result = db.session.query(
                Evaluation_Data
            ).order_by(
                func.random()
            ).limit(5).all()
            
            sample_rows = [row.to_dict() for row in sample_rows_result]
            
            return {
                "shape": {
                    "total_rows": num_of_rows,
                    "total_features": len(columns),
                },
                "class_imbalance": {
                    "not_churned": not_churned,
                    "churned": churned
                },
                "features": column_data,
                "sample_data": sample_rows
            } 
            
        except SQLAlchemyError as ex:
            raise SQLAlchemyError(
                "An error occurred while retrieving dataset information."
            ) from ex