from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str
    
@dataclass
class DataValidationArtifact:
    validation_status: str
    valid_train_file_path: str
    valid_test_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path: str
    drift_report_file_path: str
    
@dataclass
class DataTaransformationArtifact:
    numpy_array_train_file_path:str
    numpy_array_test_file_path:str
    preprocess_object_file_path:str

@dataclass
class DataClassificationArtifact:
    f1_score: float
    precision_score: float
    recall_score: float
 
@dataclass
class ModelTrainerArtifact:
    trained_model_file_path:str
    train_metric_artifact:DataClassificationArtifact
    test_metric_artifact:DataClassificationArtifact
    
    