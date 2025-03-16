from sqlalchemy import text
from scripts import database_engine
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, precision_score, recall_score, f1_score

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
            "version_name": model["version"]
        })

    return model_evaluation_list