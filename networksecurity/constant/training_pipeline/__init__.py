import os
import numpy as np

"universal constant names will be declared here"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
FILE_NAME: str = "PhishingData.csv"
TARGET_COLUMN: str = "Result"
PIPELINE_NAME: str = "networksecurity"
ARTIFACT_NAME: str = "Artifacts"
SCHEMA_CONFIG = os.path.join("data_schema","schema.yaml")
PREPROCESS_FILE: str = "preprocess.pkl"
MODEL_FILE_NAME: str = "model.pkl"
"""
Data ingestion constants start with DATAINGESTION VAR NAME
"""

DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_DATABASE_NAME: str = "SIVAKUMAR"
DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2


"""
Data Validation constants start with DATAVALIDATION VAR NAME
"""

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "valid"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_FILE_NAME: str = "report.yaml"

"""
Data Transformation constants start with DATA_TRANSFORMATION VAR NAME
"""

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values":np.nan,
    "n_neighbors":3,
    "weights":"uniform"
}
DATA_TRANSFORMATION_TRAIN_FILE_PATH: str ="train.npy"
DATA_TRANSFORMATION_TEST_FILE_PATH: str ="test.npy"

"""
Model training constants start with MODEL_TRAINER VAR NAME
"""

MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_OVERFITTING_AND_UNDERFITTING_THRESOLD: float = 0.05
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6


