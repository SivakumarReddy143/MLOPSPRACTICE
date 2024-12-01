import os
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkModel:
    def __init__(self,preprocess,model):
        try:
            self.preprocess=preprocess
            self.model=model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def predict(self,x):
        try:
            x_transform=self.preprocess.transform(x)
            y_hat=self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys)