import joblib
import pandas as pd
from application import db
from application.model import Data_Transformer
from os.path import join, dirname, realpath, abspath

ABS_DIR = dirname(abspath(__file__))
BASE_DIR = join(ABS_DIR, "trained_models/")
DATA_TRANSFORMER_PATH = join(BASE_DIR, "data_transformers/")

def json_data_preprocessor(json_data):
    dataframe = pd.json_normalize(json_data)
    
    result = db.session.query(
        Data_Transformer.name
    ).all()
    
    def encode_data(data):
        
        if not result:
            raise FileNotFoundError("Currently there are no trained encoders available.")
        
        # Onehot encoding
        oneHotEncoder = joblib.load(join(DATA_TRANSFORMER_PATH, f"{result[0][0]}.pkl"))
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
        genderEncoder = joblib.load(join(DATA_TRANSFORMER_PATH, f"{result[1][0]}.pkl"))
        housingEncoder = joblib.load(join(DATA_TRANSFORMER_PATH, f"{result[2][0]}.pkl"))
        loanEncoder = joblib.load(join(DATA_TRANSFORMER_PATH, f"{result[3][0]}.pkl"))

        data['gender'] = genderEncoder.transform(data['gender'])
        data['housing'] = housingEncoder.transform(data['housing'])
        data['loan'] = loanEncoder.transform(data['loan'])

        data.columns = data.columns.str.strip()
        return data

    def scale_data(data):
        # Min-Max scaling
        minmaxScaler = joblib.load(join(DATA_TRANSFORMER_PATH, f"{result[4][0]}.pkl"))
        return minmaxScaler.transform(data)

    encoded_data = encode_data(dataframe)
    scaled_data = scale_data(encoded_data)
    return scaled_data