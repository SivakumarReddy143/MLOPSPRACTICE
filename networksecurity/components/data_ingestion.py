from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.constant import training_pipeline
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import os
import sys
import pymongo
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def export_collection_as_dataframe(self):
        try:
            database_name=training_pipeline.DATA_INGESTION_DATABASE_NAME
            collection_name=training_pipeline.DATA_INGESTION_COLLECTION_NAME
            mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=mongo_client[database_name][collection_name]
            df=pd.DataFrame(collection.find())
            if "_id" in df.columns.to_list():
                df=df.drop(columns=['_id'],axis=1)
            df.replace({'na':np.nan},inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def export_dataframe_as_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def split_data_as_train_test(self,dataframe):
        try:
            train_data,test_data=train_test_split(dataframe,
                                                  test_size=self.data_ingestion_config.train_test_split_ratio
                                                  )
            dir_path=os.path.dirname(self.data_ingestion_config.ingested_train_data)
            os.makedirs(dir_path,exist_ok=True)
            train_data.to_csv(self.data_ingestion_config.ingested_train_data,index=False,header=True)
            test_data.to_csv(self.data_ingestion_config.ingested_test_data,index=False,header=True)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_dataframe_as_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            data_ingestion_artifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.ingested_train_data,
                                                          test_file_path=self.data_ingestion_config.ingested_test_data
                                                          )
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
