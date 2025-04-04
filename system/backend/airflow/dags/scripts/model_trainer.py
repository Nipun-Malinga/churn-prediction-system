import uuid
import warnings
from os.path import abspath, dirname, join

import joblib
from imblearn.over_sampling import SMOTENC
from lightgbm import LGBMClassifier
from scipy.stats import randint, uniform
from scripts import database_engine
from scripts.utils import remove_models, upload_to_gcs
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.model_selection import RandomizedSearchCV
from sqlalchemy import text
from xgboost import XGBClassifier

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
    XGM_best_params = XGM_random_searched.best_params_

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
    
    
    #TODO: Create a output template
    return [
        {
            "model":XGM_random_searched, 
            "name":"XGBOOST", 
            "version": XGM_version, 
            "base_model": True,
            "best_params": XGM_best_params
        }, 
        # {"model":LGB_random_searched, "name":"LIGHTGBM"}, 
        # {"model":RF_random_searched, "name":"RANDOM FORSET"}, 
        # {"model":voting_classifier, "name":"VOTING CLASSIFIER"}
        ]

def deploy_models(model_list: list):
    
    with database_engine().connect() as connection:
        model_id_result = connection.execute(
            text(
                """
                SELECT id
                FROM model
                """
            )
        )
    
    for id in model_id_result: 
        remove_models(
            ML_MODEL_PATHS["versioned"],
            f"""
                SELECT 
                    version_name 
                FROM model_info 
                WHERE model_id = {id[0]}
                ORDER BY updated_date 
                DESC
                LIMIT 1
            """
        )

    for model in model_list:
        model_version = model["version"]
        upload_to_gcs("churn_prediction_model_storage", join(ML_MODEL_PATHS["versioned"], model_version), f"ml_models/{model_version}")