import os
import sys
from networksecurity.logging.logger import logging
class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys):
        self.error_message=error_message
        _,_,exc_tb=error_details.exc_info()
        self.lineno=exc_tb.tb_lineno
        self.file_name=exc_tb.tb_frame.f_code.co_filename
        
    def __str__(self):
        return "Error found in Python script [{0}] in line number [{1}] in file [{2}]".format(
            self.file_name,self.lineno,self.error_message
        )
        
if __name__ == "__main__":
    try:
        print(1/0)
    except Exception as e:
        logging.info("Exception occured")
        raise NetworkSecurityException(e,sys)