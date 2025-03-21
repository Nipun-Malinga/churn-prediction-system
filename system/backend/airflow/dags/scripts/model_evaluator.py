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
            "version_name": model["version"],
            "base_model": model["base_model"]
        })

    return model_evaluation_list

def compare_model_performance(base_performance, evaluated_performance):
    retrain_model= False 
    accuracy_loss = (evaluated_performance[0]["accuracy"] - base_performance[0]["accuracy"]) * 100
    
    if accuracy_loss < -15 or evaluated_performance[0]["accuracy"] < 0.75:
        retrain_model = True
    
    return accuracy_loss, retrain_model
