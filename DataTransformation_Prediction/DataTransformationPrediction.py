import os
import pandas as pd
from application_logging.logger import App_Logger


class dataTransformPredict:
    def __init__(self):
        self.goodDataPath = "Prediction_Raw_files_validated/Good_Raw"
        self.logger = App_Logger()

    def replaceMissingWithNULL(self):
        try:
            f = open("Prediction_Logs/dataTransformLog.txt", 'a+')
            onlyfiles = [file for file in os.listdir(self.goodDataPath)]
            for file in onlyfiles:
                df = pd.read_csv(self.goodDataPath + '/' + file)
                df.to_csv(self.goodDataPath + '/' + file, index=None, header=True)
                self.logger.log(f, "%s: File Transformed successfully" % file)
        except Exception as e:
            self.logger.log(f, "Data Transformation failed because:: %s" % e)
            raise e
        finally:
            f.close()
