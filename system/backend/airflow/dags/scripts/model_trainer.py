from datetime import datetime

import warnings
import joblib

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype, is_object_dtype

from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier, VotingClassifier

from imblearn.over_sampling import SMOTENC
from scipy.stats import randint, uniform

from lightgbm import LGBMClassifier
from xgboost import XGBClassifier

from sqlalchemy import text

from scripts import database_engine

warnings.filterwarnings('ignore')

def preprocess_dataset():
    def handle_outliers(dataset):
        # Note: Dropped columns are categorical features. There is no use to handle outliers for them.
        for index, feature in enumerate(dataset.drop(columns=['education', 'geography', 'gender', 'card_type', 'is_active_member', 'has_cr_card', 'housing', 'loan', 'exited'])):
            Q1 = dataset[feature].quantile(0.25)
            Q3 = dataset[feature].quantile(0.75)
            IQR = Q3 - Q1
            dataset[feature] = np.clip(dataset[feature], Q1 - 1.5 * IQR, Q3 + 1.5 * IQR)
          
        return dataset

    def handle_missing_values(dataset):
        columns = dataset.columns.tolist()
        for column in columns:
            # Calculate null values and percentage
            null_count = dataset[column].isnull().sum()
            total_count = len(dataset[column])
            null_percentage = (null_count / total_count) * 100

            # Handle columns based on null percentage and data type
            if null_percentage < 50:
                # Fill missing values for numerical columns
                if is_numeric_dtype(dataset[column]):
                    mean = dataset[column].mean()
                    dataset[column].fillna(mean, inplace=True)
                # Fill missing values for categorical columns
                elif is_object_dtype(dataset[column]):
                    mode = dataset[column].mode()[0]
                    dataset[column].fillna(mode, inplace=True)
            # elif 50 <= null_percentage < 70:
            #     # TODO: Implement the data missing data handling
            #     print(f"Under development for column: {column}")
            else:   
                # Drop columns with more than 80% missing values
                dataset.drop(columns=column, inplace=True)

        return dataset

    def remove_duplicates(dataset):
        if dataset.duplicated().sum() > 0:
            dataset = dataset.drop_duplicates().reset_index(drop = True)
        return dataset

    def encode_categorical_features(dataset):
        # One-Hot encoding
        oneHotEncoder = OneHotEncoder(drop='first', sparse_output=False)

        # Transform and convert to DataFrame
        encoded = oneHotEncoder.fit_transform(dataset[['geography', 'education', 'card_type']])
        encoded_df = pd.DataFrame(encoded, columns=oneHotEncoder.get_feature_names_out(['geography', 'education', 'card_type']))

        # Reset index before concatenation
        dataset = dataset.reset_index(drop=True)
        encoded_df = encoded_df.reset_index(drop=True)

        # Concatenate DataFrames
        dataset = pd.concat([dataset, encoded_df], axis=1)

        # Drop original categorical columns
        dataset = dataset.drop(columns=['geography', 'education', 'card_type'])

        # # Label encoding
        gender_encoder = LabelEncoder()
        housing_encoder = LabelEncoder()
        loan_encoder = LabelEncoder()

        # Fitting and transforming each column separately
        dataset['gender'] = gender_encoder.fit_transform(dataset['gender'])
        dataset['housing'] = housing_encoder.fit_transform(dataset['housing'])
        dataset['loan'] = loan_encoder.fit_transform(dataset['loan'])

        dataset['gender'] = dataset['gender'].astype(float)
        dataset['housing'] = dataset['housing'].astype(float)
        dataset['loan'] = dataset['loan'].astype(float)

        # Export all the encoders
        # joblib.dump(oneHotEncoder, './trained_models/encoders/onehot_encoder.pkl')
        # joblib.dump(gender_encoder, './trained_models/encoders/gender_encoder.pkl')
        # joblib.dump(housing_encoder, './trained_models/encoders/housing_encoder.pkl')
        # joblib.dump(loan_encoder, './trained_models/encoders/loan_encoder.pkl')

        # Moving the Y predictor to the end of the dataset
        feature_exited = dataset['exited']
        dataset = dataset.drop(columns=['exited'])
        dataset = pd.concat([dataset, feature_exited], axis=1)

        dataset.columns = dataset.columns.str.strip()
        return dataset

    def split_dataset_to_X_y(dataset):
        X = dataset.iloc[:, :-1]
        y = dataset.iloc[:, -1]
        return X, y

    def handle_class_imbalance(X, y):
        categorical_features = [
            'gender',
            'has_cr_card', 'is_active_member',
            'housing', 'loan','geography_Germany',
            'geography_Spain', 'education_secondary',
            'education_tertiary', 'education_unknown',
            'card_type_GOLD','card_type_None',
            'card_type_PLATINUM', 'card_type_SILVER'
        ]

        cat_indices = [X.columns.get_loc(col) for col in categorical_features]
        
        smote = SMOTENC(categorical_features=cat_indices, k_neighbors=9, random_state=42)
        overSampled_X, overSampled_y = smote.fit_resample(X, y)

        return overSampled_X, overSampled_y  

    def scale_features(X_train, X_test):
        scaler = MinMaxScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Export scaler
        # joblib.dump(scaler, './trained_models/scaler/minMax_scaler.pkl')
        return X_train_scaled, X_test_scaled

    # Fetching data from the database
    with database_engine().connect() as conn:
        dataset = pd.read_sql(
            sql="SELECT * FROM evaluation_data",
            con=conn.connection
        )

    dataset = dataset.drop(columns=['added_date'])

    # Removing the white spaces from columns
    dataset.columns = dataset.columns.str.strip()

    # Removing whitespaces from dara
    dataset = dataset.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    # Handling null values
    dataset = handle_missing_values(dataset)

    # Check and drop duplicates from the database
    dataset =  remove_duplicates(dataset)

    # Check and handle outliers from the database
    dataset = handle_outliers(dataset)

    # Encoding categorical features using one-hot encoding and label encoding
    dataset = encode_categorical_features(dataset)

    # Re-Removing the white spaces from feature names
    dataset.columns = dataset.columns.str.strip()

    # Splitting the dataset into X and y
    X, y = split_dataset_to_X_y(dataset)

    # Generating synthetic data using SMOTE
    X, y = handle_class_imbalance(X, y)

    # Splitting the dataset into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    # Feature scaling using min max scaler
    X_train, X_test = scale_features(X_train, X_test)

    return X_train, X_test, y_train, y_test

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
        {"model":XGM_random_searched, "name":"XGBOOST"}, 
        # {"model":LGB_random_searched, "name":"LIGHTGBM"}, 
        # {"model":RF_random_searched, "name":"RANDOM FORSET"}, 
        # {"model":voting_classifier, "name":"VOTING CLASSIFIER"}
        ]

from sqlalchemy import text
from datetime import datetime

def update_database(model_evaluation_list):
    engine = database_engine()

    with engine.connect() as connection:
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
                    (model_id, updated_date, accuracy, "TP", "TN", "FP", "FN", precision, recall, f1_score, is_automated_tunning)
                    VALUES 
                    (:model_id, :updated_date, :accuracy, :TP, :TN, :FP, :FN, :precision, :recall, :f1_score, :is_automated_tunning)
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
                    "is_automated_tunning": True
                })


                print("Database updated successfully!")

        except Exception as ex:
            print(f"Error updating database: {ex}")
