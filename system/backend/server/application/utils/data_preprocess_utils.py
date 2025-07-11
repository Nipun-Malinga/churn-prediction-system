from os.path import abspath, dirname, exists, join

import joblib
import pandas as pd
from application import db
from application.models import Data_Transformer

ABS_DIR = dirname(abspath(__file__))
BASE_DIR = join(ABS_DIR, "trained_models/")
DATA_TRANSFORMER_PATH = join(BASE_DIR, "data_transformers/")


def load_encoder(file_name):
    path = join(DATA_TRANSFORMER_PATH, f"{file_name}.pkl")
    if not exists(path):
        raise FileNotFoundError(f"File {file_name} not found at {path}")
    return joblib.load(path)


def json_data_preprocessor(json_data):
    # TODO: Implement A Dynamic Preprocessing System
    dataframe = pd.json_normalize(json_data)

    results = db.session.query(Data_Transformer).all()

    if not results:
        raise FileNotFoundError("Currently there are no trained encoders available.")

    transformers = {row.name: load_encoder(row.name) for row in results}

    def encode_data(data):

        # OneHot encoding
        oneHotEncoder = transformers["One_Hot_Encoder"]

        encoded = oneHotEncoder.transform(data[["geography", "education", "card_type"]])

        encoded_df = pd.DataFrame(
            encoded,
            columns=oneHotEncoder.get_feature_names_out(
                ["geography", "education", "card_type"]
            ),
        )

        # Reset index before concatenation
        data = data.reset_index(drop=True)
        encoded_df = encoded_df.reset_index(drop=True)

        # Concatenate DataFrames
        data = pd.concat([data, encoded_df], axis=1)

        # Drop original categorical columns
        data = data.drop(columns=["geography", "education", "card_type"])

        # Label encoding
        data["gender"] = transformers["gender_Encoder"].transform(data["gender"])
        data["housing"] = transformers["housing_Encoder"].transform(data["housing"])
        data["loan"] = transformers["loan_Encoder"].transform(data["loan"])

        data.columns = data.columns.str.strip()
        return data

    def scale_data(data):
        # Standard scaling
        return transformers["Standard Scaler"].transform(data)

    try:

        encoded_data = encode_data(dataframe)
        scaled_data = scale_data(encoded_data)
        return scaled_data
    except Exception as ex:
        raise ValueError("Failed to preprocess data") from ex


def csv_data_preprocessor(csv_data):
    dataframe = pd.read_csv(csv_data)

    expected_features = [
        "CustomerId",
        "Surname",
        "Education",
        "CreditScore",
        "Geography",
        "Gender",
        "Age",
        "Tenure",
        "Balance",
        "NumOfProducts",
        "HasCrCard",
        "Card Type ",
        "IsActiveMember",
        "EstimatedSalary",
        "Housing",
        "Loan",
        "Exited",
    ]

    actual_features = list(dataframe.columns)

    if set(actual_features) != set(expected_features):
        raise ValueError(
            f"Invalid Features Detected. Make Sure dataset only contain features: {expected_features}"
        )

    dataframe["Card Type "] = dataframe["Card Type "].where(
        dataframe["HasCrCard"] == 1, "None"
    )

    dataframe = dataframe.drop(columns=["CustomerId", "Surname"])

    dataframe = dataframe.rename(
        columns={
            "Education": "education",
            "CreditScore": "credit_score",
            "Geography": "geography",
            "Gender": "gender",
            "Age": "age",
            "Tenure": "tenure",
            "Balance": "balance",
            "NumOfProducts": "num_of_products",
            "HasCrCard": "has_cr_card",
            "Card Type ": "card_type",
            "IsActiveMember": "is_active_member",
            "EstimatedSalary": "estimated_salary",
            "Housing": "housing",
            "Loan": "loan",
            "Exited": "exited",
        }
    )

    return dataframe.to_dict(orient="records")
