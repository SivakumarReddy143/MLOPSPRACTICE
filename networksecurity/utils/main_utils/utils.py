import yaml
import numpy as np
import sys
import pickle
import os
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score



def read_yaml_file(filepath: str):
    try:
        with open(filepath,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

def write_yaml_file(filepath: str,content: object,replace:bool=True):
    try:
        if replace:
            if os.path.exists(filepath):
                os.remove(filepath)
        os.makedirs(os.path.dirname(filepath),exist_ok=True)
        with open(filepath,'w') as yaml_file:
            yaml.dump(content,yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_numpy_array_data(filepath:str,array:np.array):
    try:
        os.makedirs(os.path.dirname(filepath),exist_ok=True)
        with open(filepath,'wb') as file:
            np.save(file=file,arr=array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_object(filepath:str,obj):
    try:
        os.makedirs(os.path.dirname(filepath),exist_ok=True)
        with open(filepath,'wb') as file:
            pickle.dump(obj=obj,file=file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def load_numpy_array_data(filepath:str):
    try:
        if not os.path.exists(filepath):
            raise Exception(f"The file: {filepath} not exists")
        with open(filepath,'rb') as file:
            return np.load(file=file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def load_object(filepath:str):
    try:
        if not os.path.exists(filepath):
            raise Exception(f"The file: {filepath} is not exists")
        with open(filepath,'rb') as file:
            return pickle.load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def evaluate_models(X_train,y_train,X_test,y_test,models,params):
    try:
        report={}
        for i in range(len(list(models))):
            model=list(models.values())[i]
            param=params[list(models.keys())[i]]
            gs=GridSearchCV(model,param_grid=param,cv=3)
            gs.fit(X_train,y_train)
            
            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)
            
            y_train_pred=model.predict(X_train)
            y_test_pred=model.predict(X_test)
            
            train_model_score=r2_score(y_train,y_train_pred)
            test_model_score=r2_score(y_test,y_test_pred)
            
            report[list(models.keys())[i]]=test_model_score
            return report
            
    except Exception as e:
        raise NetworkSecurityException(e,sys)