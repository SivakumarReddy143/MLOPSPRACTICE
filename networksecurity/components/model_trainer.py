import os
import sys
import mlflow
from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import DataTaransformationArtifact,ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig



from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_object,load_object
from networksecurity.utils.main_utils.utils import load_numpy_array_data,evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classifaction_score

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)



import dagshub
dagshub.init(repo_owner='mshivakumarreddy78', repo_name='MLOPSPRACTICE', mlflow=True)

class ModelTrainer:
    def __init__(self,model_training_config:ModelTrainerConfig,data_transformation_artifact:DataTaransformationArtifact):
        try:
            self.model_training_config=model_training_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def track_model(self,best_model,classificationmetric):
        # mlflow.set_tracking_uri('http://localhost:5000')
        with mlflow.start_run():
            f1_score=classificationmetric.f1_score
            precision_score=classificationmetric.precision_score
            recall_score=classificationmetric.recall_score
            
            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("precision_score",precision_score)
            mlflow.log_metric("recall_score",recall_score)
            mlflow.sklearn.log_model(best_model,"model")
        
    def model_trainer(self,X_train,y_train,X_test,y_test):
        try:
            models = {
                "Decision Tree": DecisionTreeClassifier(),
                "Random Forest": RandomForestClassifier(verbose=1),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }
            params={
                "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }
            model_report:dict = evaluate_models(X_train,y_train,X_test,y_test,models,params)
            best_model_score=max(sorted(list(model_report.values())))
            best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            
            best_model=models[best_model_name]
            
            y_train_pred=best_model.predict(X_train)
            classification_train_metric=get_classifaction_score(y_train,y_train_pred)
            
            self.track_model(best_model,classificationmetric=classification_train_metric)
            
            y_test_pred=best_model.predict(X_test)
            classification_test_metric=get_classifaction_score(y_test,y_test_pred)
            
            self.track_model(best_model,classificationmetric=classification_test_metric)
            
            preprocessor=load_object(self.data_transformation_artifact.preprocess_object_file_path)
            
            model_dir_path=os.path.dirname(self.model_training_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)
            
            network_model=NetworkModel(preprocess=preprocessor,model=best_model)
            save_object(self.model_training_config.trained_model_file_path,network_model)
            
            save_object("final_model/model.pkl",best_model)
            
            model_trainer_artifact=ModelTrainerArtifact(
                trained_model_file_path=self.model_training_config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
            )
            
            return model_trainer_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    
    
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.numpy_array_train_file_path
            test_file_path = self.data_transformation_artifact.numpy_array_test_file_path

            #loading training array and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model_trainer_artifact=self.model_trainer(x_train,y_train,x_test,y_test)
            return model_trainer_artifact

            
        except Exception as e:
            raise NetworkSecurityException(e,sys)