import joblib
import pandas as pd
from os.path import join, dirname, realpath, abspath

def json_data_preprocessor(json_data):
    dataframe = pd.json_normalize(json_data)

    ABS_DIR = dirname(abspath(__file__))
    print(ABS_DIR)
    BASE_DIR = join(ABS_DIR, "trained_models/")

    def encode_data(data):
        # Onehot encoding
        oneHotEncoder = joblib.load(join(BASE_DIR, "encoders/onehot_encoder.pkl"))
        encoded = oneHotEncoder.transform(data[['geography', 'education', 'card_type']])
        encoded_df = pd.DataFrame(encoded,
                                    columns=oneHotEncoder.get_feature_names_out(
                                        ['geography', 'education', 'card_type']
                                    ))

        # Reset index before concatenation
        data= data.reset_index(drop=True)
        encoded_df = encoded_df.reset_index(drop=True)

        # Concatenate DataFrames
        data = pd.concat([data, encoded_df], axis=1)

        # Drop original categorical columns
        data = data.drop(columns=['geography', 'education', 'card_type'])

        # Label encoding
        genderEncoder = joblib.load(join(BASE_DIR, "encoders/gender_encoder.pkl"))
        housingEncoder = joblib.load(join(BASE_DIR, "encoders/housing_encoder.pkl"))
        loanEncoder = joblib.load(join(BASE_DIR, "encoders/loan_encoder.pkl"))

        data['gender'] = genderEncoder.transform(data['gender'])
        data['housing'] = housingEncoder.transform(data['housing'])
        data['loan'] = loanEncoder.transform(data['loan'])

        data.columns = data.columns.str.strip()
        return data

    def scale_data(data):
        # Min-Max scaling
        minmaxScaler = joblib.load(join(BASE_DIR, "scaler/minMax_scaler.pkl"))
        return minmaxScaler.transform(data)

    encoded_data = encode_data(dataframe)
    scaled_data = scale_data(encoded_data)
    return scaled_data