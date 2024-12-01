import logging
import os
from datetime import datetime


File_Name=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

file_path=os.path.join(os.getcwd(),"logs",File_Name)
os.makedirs(file_path,exist_ok=True)

log_file_path= os.path.join(file_path,File_Name)

logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="[ %(asctime)s ] %(lineno)d %(levelname)s %(message)s"
)
