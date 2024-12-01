import os
import sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS,TARGET_COLUMN
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifact_entity import DataValidationArtifact,DataTaransformationArtifact
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    
    @staticmethod
    def read_data(filepath:str):
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def get_transformed_object(cls):
        try:
            knnImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            preprocess=Pipeline([("impute",knnImputer)])
            return preprocess
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_transformation(self):
        try:
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            #training dataframe
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_train_df=target_feature_train_df.replace(-1,0)
            
            #testing dataframe
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df=target_feature_test_df.replace(-1,0)
            preprocess=self.get_transformed_object()
            preprocess_object=preprocess.fit(input_feature_train_df)
            transformed_input_feature_traindf=preprocess_object.transform(input_feature_train_df)
            transformed_input_feature_testdf=preprocess_object.transform(input_feature_test_df)
            
            train_arr=np.c_[transformed_input_feature_traindf,target_feature_train_df]
            test_arr=np.c_[transformed_input_feature_testdf,target_feature_test_df]
            
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,test_arr)
            save_object(self.data_transformation_config.preprocess_object_path,preprocess_object)
            
            save_object("final_model/preprocess.pkl",preprocess_object)
            
            data_transformation_artifact=DataTaransformationArtifact(
                numpy_array_train_file_path=self.data_transformation_config.transformed_train_file_path,
                numpy_array_test_file_path=self.data_transformation_config.transformed_test_file_path,
                preprocess_object_file_path=self.data_transformation_config.preprocess_object_path
            )
            return data_transformation_artifact
            
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)