import os
import sys
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.constant.training_pipeline import SCHEMA_CONFIG
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.schema_config=read_yaml_file(SCHEMA_CONFIG)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    @staticmethod
    def read_data(filepath:str):
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame):
        try:
            number_of_columns=len(self.schema_config)
            logging.info(f"number of columns in schema file {number_of_columns}")
            logging.info(f"number of columns in dataframe {len(dataframe.columns)}")
            if(number_of_columns==len(dataframe.columns)):
                return True
            else:
                return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def detect_dataset_drift(self,basedf:pd.DataFrame,currentdf:pd.DataFrame,thresold=0.05):
        try:
            status=True
            report={}
            for column in basedf.columns:
                df1=basedf[column]
                df2=currentdf[column]
                is_same_dist=ks_2samp(df1,df2)
                if(thresold<=is_same_dist.pvalue):
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                }})
            drift_report_file_path=self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_report_file_path),exist_ok=True)
            write_yaml_file(drift_report_file_path,report)
                
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def initiate_data_validation(self):
        try:
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path= self.data_ingestion_artifact.test_file_path
            
            train_data=DataValidation.read_data(train_file_path)
            test_data=DataValidation.read_data(test_file_path)
            status=self.validate_number_of_columns(train_data)
            if not status:
                error_message=f"train data does not contain all columns"
            status=self.validate_number_of_columns(test_data)
            if not status:
                error_message=f"test data does not contain all columns"
            status=self.detect_dataset_drift(train_data,test_data)
            
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            train_data.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)
            test_data.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)
            
            data_validation_artifact=DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)