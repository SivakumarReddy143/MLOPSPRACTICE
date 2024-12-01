from sklearn.metrics import f1_score,precision_score,recall_score
import os
import sys
import numpy as np
import pandas as pd
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataClassificationArtifact

def get_classifaction_score(y_test,y_pred)->DataClassificationArtifact:
    try:
        f1_Score=f1_score(y_test,y_pred)
        precision_Score=precision_score(y_test,y_pred)
        recall_Score=recall_score(y_test,y_pred)
        classification_artifact=DataClassificationArtifact(
            f1_score=f1_Score,
            precision_score=precision_Score,
            recall_score=recall_Score
        )
        return classification_artifact
    except Exception as e:
        raise NetworkSecurityException(e,sys)