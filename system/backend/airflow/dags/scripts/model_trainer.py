
import os
import uuid
import warnings
import joblib

from datetime import datetime

from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier, VotingClassifier

from imblearn.over_sampling import SMOTENC
from scipy.stats import randint, uniform

from lightgbm import LGBMClassifier
from xgboost import XGBClassifier

from sqlalchemy import text

from scripts import database_engine

from os.path import join, dirname, abspath

from google.cloud import storage

from scripts.utils import upload_to_gcs, remove_models

warnings.filterwarnings('ignore')

ABS_DIR = dirname(abspath(__file__))
BASE_DIR = join(ABS_DIR, "trained_models/")

ML_MODEL_PATHS = {
    "non_versioned": join(BASE_DIR, "ml_models/non_versioned/"),
    "versioned": join(BASE_DIR, "ml_models/versioned/"),
}

def train_model(X_train, y_train):

    def preform_random_search(model, params, n_tier=20, cv=5):
        random_search = RandomizedSearchCV(model, param_distributions=params, n_iter=n_tier, cv=cv, scoring='accuracy', n_jobs=-1, random_state=42)
        return random_search.fit(X_train, y_train)
    
    XGM = XGBClassifier(
        objective="binary:logistic",
        eval_metric="logloss",
        n_jobs=-1,
    )

    params_XG = {
        'max_depth': randint(2, 8),
        'reg_alpha': uniform(0.01, 1),
        'reg_lambda': uniform(0.01, 10),
        'n_estimators': randint(100, 600),
    }

    XGM_random_searched = preform_random_search(XGM, params_XG, 30)
    XGM_random_searched.best_params_

    joblib.dump(XGM_random_searched, join(ML_MODEL_PATHS["non_versioned"], "XGBOOST.pkl"))

    XGM_version = f"XGBOOST_V{str(uuid.uuid4())[:8]}.pkl"
    joblib.dump(XGM_random_searched, join(ML_MODEL_PATHS["versioned"], XGM_version))

    # LGB = LGBMClassifier()

    # params_LGB = {
    #     'learning_rate': uniform(0.01, 1),
    #     'max_depth': randint(2, 20),
    #     'num_leaves': randint(20, 60),
    #     'n_estimators': randint(100, 600),
    # }

    # LGB_random_searched = preform_random_search(LGB, params_LGB, 40, 10)
    # LGB_random_searched.best_params_

    # RF = RandomForestClassifier()

    # params_RF = {
    #     'max_depth': randint(3, 20),
    #     'min_samples_split': randint(2, 20),
    #     'n_estimators': randint(100, 600),
    # }

    # RF_random_searched = preform_random_search(RF, params_RF, 30, 10)
    # RF_random_searched.best_params_

    # voting_classifier = VotingClassifier(
    #     estimators=[
    #         ('xg', XGM_random_searched), 
    #         ('lgb', LGB_random_searched), 
    #         ('rf', RF_random_searched)], voting='soft').fit(X_train, y_train)
    
    return [
        {"model":XGM_random_searched, "name":"XGBOOST", "version": XGM_version}, 
        # {"model":LGB_random_searched, "name":"LIGHTGBM"}, 
        # {"model":RF_random_searched, "name":"RANDOM FORSET"}, 
        # {"model":voting_classifier, "name":"VOTING CLASSIFIER"}
        ]

def deploy_model(model_list: list):

    remove_models(
        join(ML_MODEL_PATHS["versioned"]),
        """
            SELECT 
                version_name 
            FROM model_info 
            WHERE model_id = (SELECT id FROM model WHERE name = 'XGBOOST') 
            ORDER BY updated_date 
            DESC 
            LIMIT 1")
        """
    )

    for model in model_list:
        model_version = model["version"]
        # upload_to_gcs("churn_prediction_model_storage", join(ML_MODEL_PATHS["versioned"], model_version), f"ml_models/{model_version}")

def update_database(model_evaluation_list):

    with database_engine().connect() as connection:
        try:
            for evaluation in model_evaluation_list:
                model_id_result = connection.execute(
                    text("SELECT id FROM model WHERE name = :model_name"), {"model_name": evaluation["model_name"]}
                ).fetchone()

                if not model_id_result:
                    model_id_result = connection.execute(
                        text("INSERT INTO model (name) VALUES (:name) RETURNING id"), {"name": evaluation["model_name"]}
                    ).fetchone()

                model_id = model_id_result[0] 

                model_info_query = text("""
                    INSERT INTO model_info 
                    (model_id, updated_date, accuracy, "TP", "TN", "FP", "FN", precision, recall, f1_score, is_automated_tunning, version_name)
                    VALUES 
                    (:model_id, :updated_date, :accuracy, :TP, :TN, :FP, :FN, :precision, :recall, :f1_score, :is_automated_tunning, :version_name)
                """)

                connection.execute(model_info_query, {
                    "model_id": model_id,
                    "updated_date": datetime.now(),
                    "accuracy": float(evaluation["accuracy"]), 
                    "TP": int(evaluation["tp"]),
                    "TN": int(evaluation["tn"]),
                    "FP": int(evaluation["fp"]),
                    "FN": int(evaluation["fn"]),
                    "precision": float(evaluation["precision"]),
                    "recall": float(evaluation["recall"]),
                    "f1_score": float(evaluation["f1_score"]),
                    "is_automated_tunning": True,
                    "version_name": evaluation["version_name"]
                })

                print("Database updated successfully!")

        except Exception as ex:
            print(f"Error updating database: {ex}")