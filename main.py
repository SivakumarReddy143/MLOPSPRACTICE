from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os
import sys
import pandas as pd
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
if __name__=="__main__":
    try:
        training_pipeline_config=TrainingPipelineConfig()
        data_ingestion_config=DataIngestionConfig(training_pipeline_config)
        data_ingestion=DataIngestion(data_ingestion_config)
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        data_validation_config=DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=data_validation_config)
        data_validation_artifatcs=data_validation.initiate_data_validation()
        data_transformation_config=DataTransformationConfig(training_pipelne_config=training_pipeline_config)
        data_transformation=DataTransformation(data_validation_artifact=data_validation_artifatcs,data_transformation_config=data_transformation_config)
        data_transformation_artifacts=data_transformation.initiate_data_transformation()
        print(data_transformation_artifacts)
        model_trainer_config=ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        model_trainer=ModelTrainer(model_training_config=model_trainer_config,data_transformation_artifact=data_transformation_artifacts)
        model_trainer_artifacts=model_trainer.initiate_model_trainer()
        print(model_trainer_artifacts)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    