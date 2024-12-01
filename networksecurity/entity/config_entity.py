import os
import sys
from datetime import datetime
from networksecurity.constant import training_pipeline
class TrainingPipelineConfig:
    def __init__(self):
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_NAME
        self.artifact_dir = os.path.join(self.artifact_name,datetime.now().strftime('%m_%d_%Y_%H_%M_%S'))

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir,
                                               training_pipeline.DATA_INGESTION_DIR_NAME
                                               )
        self.feature_store_file_path = os.path.join(self.data_ingestion_dir,
                                                    training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
                                                    training_pipeline.FILE_NAME
                                                    )
        self.ingested_dir= os.path.join(self.data_ingestion_dir,
                                        training_pipeline.DATA_INGESTION_INGESTED_DIR
                                        )
        self.ingested_train_data= os.path.join(self.ingested_dir,
                                               training_pipeline.TRAIN_FILE_NAME
                                               )
        self.ingested_test_data = os.path.join(self.ingested_dir,
                                               training_pipeline.TEST_FILE_NAME
                                               )
        self.train_test_split_ratio=training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.database_name = training_pipeline.DATA_INGESTION_DATABASE_NAME
        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        
        
class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir=os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir=os.path.join(self.data_validation_dir,
                                         training_pipeline.DATA_VALIDATION_VALID_DIR
                                         )
        self.valid_train_file_path=os.path.join(self.valid_data_dir,
                                                training_pipeline.TRAIN_FILE_NAME
                                                )
        self.valid_test_file_path=os.path.join(self.valid_data_dir,
                                               training_pipeline.TEST_FILE_NAME
                                               )
        self.invalid_data_dir = os.path.join(self.data_validation_dir,
                                             training_pipeline.DATA_VALIDATION_INVALID_DIR
                                             )
        self.invalid_train_file_name = os.path.join(self.invalid_data_dir,
                                              training_pipeline.TRAIN_FILE_NAME
                                              )
        self.invalid_test_file_name = os.path.join(self.invalid_data_dir,
                                                   training_pipeline.TEST_FILE_NAME
                                                   )
        self.drift_report_file_path=os.path.join(self.data_validation_dir,
                                                 training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
                                                 training_pipeline.DATA_VALIDATION_DRIFT_FILE_NAME
                                                 )

class DataTransformationConfig:
    def __init__(self,training_pipelne_config:TrainingPipelineConfig):
        self.data_transformation_dir = os.path.join(training_pipelne_config.artifact_dir,
                                                    training_pipeline.DATA_TRANSFORMATION_DIR_NAME
                                                    )
        self.transformed_dir=os.path.join(self.data_transformation_dir,
                                          training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR
                                          )
        self.transformed_train_file_path=os.path.join(self.transformed_dir,
                                                             training_pipeline.DATA_TRANSFORMATION_TRAIN_FILE_PATH
                                                             )
        self.transformed_test_file_path=os.path.join(self.transformed_dir,
                                                training_pipeline.DATA_TRANSFORMATION_TEST_FILE_PATH
                                                )
        self.preprocess_object_path=os.path.join(self.data_transformation_dir,
                                                 training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
                                                 training_pipeline.PREPROCESS_FILE
                                                 )
        
class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir: str = os.path.join(training_pipeline_config.artifact_dir,
                                                   training_pipeline.MODEL_TRAINER_DIR_NAME
                                                   )
        self.trained_model_dir: str = os.path.join(self.model_trainer_dir,
                                                   training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR
                                                   )
        self.trained_model_file_path: str = os.path.join(self.trained_model_dir,
                                                    training_pipeline.MODEL_FILE_NAME
                                                    )
        self.overfitting_and_underfitting_thresold: str = training_pipeline.MODEL_TRAINER_OVERFITTING_AND_UNDERFITTING_THRESOLD
        self.expected_score: str = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        