from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, precision_score, recall_score, f1_score

def evaluate_model(model_list: list, X_test, y_test):
    model_evaluation_list = []

    def display_model_accuracy(model, model_name,  X_test, y_test):
        y_pred = model.predict(X_test)
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

        model_evaluation_list.append({
            "model_name": model_name,
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall": recall_score(y_test, y_pred),
            "f1_score": f1_score(y_test, y_pred),
            "tp": tp,
            "tn": tn,
            "fp": fp,
            "fn": fn 
        })

        return 

    for model in model_list:
        display_model_accuracy(model["model"], model["name"],  X_test, y_test)

    return model_evaluation_list