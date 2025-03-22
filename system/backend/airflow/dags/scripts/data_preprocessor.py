import uuid
import joblib

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype, is_object_dtype

from os.path import join, dirname, realpath, abspath
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, MinMaxScaler

from imblearn.over_sampling import SMOTENC

from sqlalchemy import text

from scripts import database_engine
from scripts.utils import upload_to_gcs, remove_models

ABS_DIR = dirname(abspath(__file__))
BASE_DIR = join(ABS_DIR, "trained_models/")

DATA_TRANSFORMER_PATHS = {
    "non_versioned": join(BASE_DIR, "data_transformers/non_versioned/"),
    "versioned": join(BASE_DIR, "data_transformers/versioned/"),
}

def preprocess_dataset(dataset):
    # Store the data transformers
    data_transformer_list = []
     
    def handle_outliers(dataset):
        # Note: Dropped columns are categorical features. There is no use to handle outliers for them.
        for index, feature in enumerate(dataset.drop(columns=["education", "geography", "gender", "card_type", "is_active_member", "has_cr_card", "housing", "loan", "exited"])):
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
        oneHotEncoder = OneHotEncoder(drop="first", sparse_output=False)

        # Transform and convert to DataFrame
        encoded = oneHotEncoder.fit_transform(dataset[["geography", "education", "card_type"]])
        encoded_df = pd.DataFrame(encoded, columns=oneHotEncoder.get_feature_names_out(["geography", "education", "card_type"]))

        # Reset index before concatenation
        dataset = dataset.reset_index(drop=True)
        encoded_df = encoded_df.reset_index(drop=True)

        # Concatenate DataFrames
        dataset = pd.concat([dataset, encoded_df], axis=1)

        # Drop original categorical columns
        dataset = dataset.drop(columns=["geography", "education", "card_type"])

        # # Label encoding
        gender_encoder = LabelEncoder()
        housing_encoder = LabelEncoder()
        loan_encoder = LabelEncoder()

        # Fitting and transforming each column separately
        dataset["gender"] = gender_encoder.fit_transform(dataset["gender"])
        dataset["housing"] = housing_encoder.fit_transform(dataset["housing"])
        dataset["loan"] = loan_encoder.fit_transform(dataset["loan"])

        dataset["gender"] = dataset["gender"].astype(float)
        dataset["housing"] = dataset["housing"].astype(float)
        dataset["loan"] = dataset["loan"].astype(float)

        # Export all the unversioned encoders
        joblib.dump(oneHotEncoder, join(DATA_TRANSFORMER_PATHS["non_versioned"], "onehot_encoder.pkl"))
        joblib.dump(gender_encoder, join(DATA_TRANSFORMER_PATHS["non_versioned"], "gender_encoder.pkl"))
        joblib.dump(housing_encoder, join(DATA_TRANSFORMER_PATHS["non_versioned"], "housing_encoder.pkl"))
        joblib.dump(loan_encoder, join(DATA_TRANSFORMER_PATHS["non_versioned"], "loan_encoder.pkl"))

         # Versioning the encoders
        onehot_encoder_version = f"onehot_encoder_V{str(uuid.uuid4())[:8]}.pkl"
        gender_encoder_version = f"gender_encoder_V{str(uuid.uuid4())[:8]}.pkl"
        housing_encoder_version = f"housing_encoder_V{str(uuid.uuid4())[:8]}.pkl"
        loan_encoder_version = f"loan_encoder_V{str(uuid.uuid4())[:8]}.pkl"

        # Export all versioned the encoders
        joblib.dump(oneHotEncoder, join(DATA_TRANSFORMER_PATHS["versioned"], onehot_encoder_version))
        joblib.dump(gender_encoder, join(DATA_TRANSFORMER_PATHS["versioned"], gender_encoder_version))
        joblib.dump(housing_encoder, join(DATA_TRANSFORMER_PATHS["versioned"], housing_encoder_version))
        joblib.dump(loan_encoder, join(DATA_TRANSFORMER_PATHS["versioned"], loan_encoder_version))

        # Moving the Y predictor to the end of the dataset
        feature_exited = dataset["exited"]
        dataset = dataset.drop(columns=["exited"])
        dataset = pd.concat([dataset, feature_exited], axis=1)

        dataset.columns = dataset.columns.str.strip()
        
        data_transformer_list.extend(
            [
                {"transformer_name": "One_Hot_Encoder", "version": onehot_encoder_version},
                {"transformer_name": "gender_Encoder", "version": gender_encoder_version},
                {"transformer_name": "housing_Encoder", "version": housing_encoder_version},
                {"transformer_name": "loan_Encoder", "version": loan_encoder_version}
            ]
        )
        
        return dataset

    def split_dataset_to_X_y(dataset):
        X = dataset.iloc[:, :-1]
        y = dataset.iloc[:, -1]
        return X, y

    def handle_class_imbalance(X, y):
        categorical_features = [
            "gender",
            "has_cr_card", "is_active_member",
            "housing", "loan","geography_Germany",
            "geography_Spain", "education_secondary",
            "education_tertiary", "education_unknown",
            "card_type_GOLD","card_type_None",
            "card_type_PLATINUM", "card_type_SILVER"
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
        joblib.dump(scaler, join(DATA_TRANSFORMER_PATHS["non_versioned"], "minMax_scaler.pkl"))

        # Versioning the scaler
        minmax_scaler_version = f"minMax_scaler_V{str(uuid.uuid4())[:8]}.pkl"

        # Expoting versioned scaler
        joblib.dump(scaler, join(DATA_TRANSFORMER_PATHS["versioned"], minmax_scaler_version))
        
        data_transformer_list.append(
            {"transformer_name": "Min Max Scaler", "version": minmax_scaler_version}
        )

        return X_train_scaled, X_test_scaled

    dataset = dataset.drop(columns=["id", "added_date"])

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

    return X_train, X_test, y_train, y_test, data_transformer_list

# FIXME: Fix the preprocessing faliure due to untrained data
def preprocess_evaluation_data(dataset):
    dataset = dataset.drop(columns=["id", "added_date"])

    def split_dataset_to_X_y(dataset):
        X = dataset.iloc[:, :-1]
        y = dataset.iloc[:, -1]
        return X, y

    def encode_data(data):
        # Onehot encoding
        oneHotEncoder = joblib.load(join(DATA_TRANSFORMER_PATHS["non_versioned"], "onehot_encoder.pkl"))
        encoded = oneHotEncoder.transform(data[["geography", "education", "card_type"]])
        encoded_df = pd.DataFrame(encoded,
                                    columns=oneHotEncoder.get_feature_names_out(
                                        ["geography", "education", "card_type"]
                                    ))

        # Reset index before concatenation
        data= data.reset_index(drop=True)
        encoded_df = encoded_df.reset_index(drop=True)

        # Concatenate DataFrames
        data = pd.concat([data, encoded_df], axis=1)

        # Drop original categorical columns
        data = data.drop(columns=["geography", "education", "card_type"])

        # Label encoding
        genderEncoder = joblib.load(join(DATA_TRANSFORMER_PATHS["non_versioned"], "gender_encoder.pkl"))
        housingEncoder = joblib.load(join(DATA_TRANSFORMER_PATHS["non_versioned"], "housing_encoder.pkl"))
        loanEncoder = joblib.load(join(DATA_TRANSFORMER_PATHS["non_versioned"], "loan_encoder.pkl"))

        data["gender"] = genderEncoder.transform(data["gender"])
        data["housing"] = housingEncoder.transform(data["housing"])
        data["loan"] = loanEncoder.transform(data["loan"])

        data.columns = data.columns.str.strip()
        return data

    def scale_data(data):
        # Min-Max scaling
        minmaxScaler = joblib.load(join(DATA_TRANSFORMER_PATHS["non_versioned"], "minMax_scaler.pkl"))
        return minmaxScaler.transform(data)

    X_test, Y_test = split_dataset_to_X_y(dataset)
    encoded_X_test = encode_data(X_test)
    scaled_X_test = scale_data(encoded_X_test)
    return scaled_X_test, Y_test

def deploy_preprocessing_models(data_transformer_list):
    
    with database_engine().connect() as connection:
        transformer_id_result = connection.execute(
            text("SELECT id FROM data_transformer")
        )
        
    for id in transformer_id_result: 
        remove_models(
            DATA_TRANSFORMER_PATHS["versioned"],
            f"""
                SELECT 
                    version_name 
                FROM data_transformer_info 
                WHERE data_transformer_id = {id[0]}
                ORDER BY updated_date 
                DESC
                LIMIT 1
            """
        )
    
    for data_transformer in data_transformer_list:
        encoder_version = data_transformer["version"]
        # upload_to_gcs("churn_prediction_model_storage", join(ENCODER_PATHS["versioned"], encoder_version), f"data_transformers/{encoder_version}")
