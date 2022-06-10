import os
import pandas as pd
from application_logging.logger import App_Logger


class dataTransformation:
    def __init__(self):
        self.goodDataPath = "Training_Raw_files_validated/Good_Raw/"
        self.logger = App_Logger()

    def replaceMissingWithNULL(self):
        f = open("Training_Logs/dataTransformLog.txt", 'a+')
        try:
            onlyfiles = [files for files in os.listdir(self.goodDataPath)]
            for file in onlyfiles:
                df = pd.read_csv(self.goodDataPath + '/' + file)
                df.to_csv(self.goodDataPath + '/' + file, index=None, header=True)
                self.logger.log(f, "%s: missing replaced with 'NULL' successfully" % file)
        except Exception as e:
            self.logger.log(f, "Data Transformation failed because:: %s" % e)
            f.close()
        f.close()
