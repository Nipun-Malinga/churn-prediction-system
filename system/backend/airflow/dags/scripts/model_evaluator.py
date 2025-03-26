from datetime import datetime

from scripts import database_engine
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score)
from sqlalchemy import text


def evaluate_model(model_list: list, X_test, y_test):
    model_evaluation_list = []
     
    for model in model_list:
        y_pred = model["model"].predict(X_test)
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

        model_evaluation_list.append({
            "model_name": model["name"],
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall": recall_score(y_test, y_pred),
            "f1_score": f1_score(y_test, y_pred),
            "tp": tp,
            "tn": tn,
            "fp": fp,
            "fn": fn,
            "version_name": model["version"],
            "base_model": model["base_model"],
            "best_params": model["best_params"]
        })

    return model_evaluation_list

def compare_model_performance(base_performance, evaluated_performance):
    retrain_model= False 
    accuracy_loss = (evaluated_performance[0]["accuracy"] - base_performance[0]["accuracy"]) * 100
    
    if accuracy_loss < -15 or evaluated_performance[0]["accuracy"] < 0.75:
        retrain_model = True
    
    return accuracy_loss, retrain_model

def update_accuracy_drift(model_info, evaluation_data, accuracy_drift):
    print(model_info)
    with database_engine().connect() as connection:
        connection.execute(
            text(
                """
                INSERT INTO 
                accuracy_drift  
                (model_info_id, date, accuracy, drift)
                VALUES 
                (:model_info_id, :date, :accuracy, :drift)
                """
            ),
            {
                "model_info_id": model_info[0]["id"],
                "date": datetime.now(),
                "accuracy": evaluation_data[0]["accuracy"],
                "drift": accuracy_drift
            }
        )