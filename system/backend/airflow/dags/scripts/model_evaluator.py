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

def fetch_drift_thresholds_from_db():
    """
    Placeholder function to simulate fetching thresholds from the database.
    """
    return {
        "accuracy": -15,
        "precision": -10,
        "recall": -10,
        "f1_score": -10,
    }

def compare_model_performance(base_performance, evaluated_performance):
    """
    Compares current model performance against a baseline and decides whether retraining is needed.
    """
    drift_thresholds = fetch_drift_thresholds_from_db()
    
    metrics = ["accuracy", "precision", "recall", "f1_score"]
    drift = {}
    retrain_model = False

    for metric in metrics:
        base_value = base_performance[0][metric]
        new_value = evaluated_performance[0][metric]
        loss = (new_value - base_value) * 100
        drift[metric] = loss

        if loss < drift_thresholds[metric]:
            retrain_model = True

        if metric == "accuracy" and new_value < 0.75:
            retrain_model = True

    return drift, retrain_model


def update_accuracy_drift(model_info, performance_drift):

    print(type(performance_drift["precision"]))
    with database_engine().connect() as connection:
        connection.execute(
            text(
                """
                INSERT INTO 
                    accuracy_drift
                (
                    model_info_id, 
                    date, 
                    accuracy_drift, 
                    precision_drift,
                    recall_drift,
                    f1_score_drift
                )
                VALUES 
                (
                    :model_info_id, 
                    :date, 
                    :accuracy, 
                    :precision,
                    :recall,
                    :f1_score
                )
                """
            ),
            {
                "model_info_id": model_info[0]["id"],
                "date": datetime.now(),
                "accuracy": float(performance_drift["accuracy"]),
                "precision": float(performance_drift["precision"]),
                "recall": float(performance_drift["recall"]),
                "f1_score": float(performance_drift["f1_score"])
            }
        )