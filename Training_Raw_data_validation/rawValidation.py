from datetime import datetime
import json
import os
import shutil

from application_logging.logger import App_logger


class Raw_Data_validation:
    def __init__(self, path):
        self.Batch_directory = path
        self.schema_path = 'schema_training.json'
        self.logger = App_logger()

    def ValuesFromSchema(self):
        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
                f.close()
            pattern = dic['SampleFileName']
            LengthOfDateStampInFile = dic['LengthOfDateStampInFile']
            LengthOfTimeStampInFile = dic['LengthOfTimeStampInFile']
            column_names = dic['ColName']
            NumberofColumns = dic['NumberofColumns']

        except ValueError:
            with open('Training_Logs/valuesFromSchemaValidationLog.txt', 'a+') as file:
                self.logger.log(file, "ValueError: Value not found inside schema_training.json")
                file.close()
            raise ValueError
        except KeyError:
            with open('Training_Logs/valuesFromSchemaValidationLog.txt', 'a+') as file:
                self.logger.log(file, "KeyError: Key value error, incorrect key passed")
                file.close()
            raise KeyError
        except Exception as e:
            with open('Training_Logs/valuesFromSchemaValidationLog.txt', 'a+') as file:
                self.logger.log(file, str(e))
                file.close()
            raise e

        return LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberofColumns

    def manualRegexCreation(self):
        # SampleFileName: creditCardFraud_021119920_010222.csv
        regex = "['credictCardFraud']+['\_'']+[\d_]+[\d]+\.csv"
        return regex

    def createDirectoryForGoodBadRawData(self):
        try:
            path = os.path.join("Training_Raw_files_validated/", "Good_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join("Training_Raw_files_validated/", "Bad_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)

        except OSError as e:
            with open ("Training_Logs/GeneralLog.txt", 'a+') as f:
                self.logger.log(f, "Error while creating directory %s:" % e)
                f.close()
            raise e

    def deleteExistingGoodDataTrainingFolder(self):
        try:
            path = "Training_Raw_files_validated/"
            if os.path.isdir(path + 'Good_Raw/'):
                shutil.rmtree(path + 'Good_Raw/')
                with open('Training_Logs/GeneralLog.txt', 'a+') as f:
                    self.logger.log(f, "GoodRaw directory deleted successfully")
                    f.close()
        except OSError as e:
            with open('Training_Logs/GeneralLog.txt', 'a+') as f:
                self.logger.log(f, "Error while deleting GoodRaw directory: %s" % e)
                f.close()
            raise e

    def deleteExistingBadDataTrainingFolder(self):
        try:
            path = "Training_Raw_files_validated/"
            if os.path.isdir(path + 'Bad_Raw/'):
                shutil.rmtree(path + 'Bad_Raw/')
                with open('Training_Logs/GeneralLog.txt', 'a+') as f:
                    self.logger.log(f, "BadRaw directory deleted successfully")
                    f.close()
        except OSError as e:
            with open('Training_Logs/GeneralLog.txt', 'a+') as f:
                self.logger.log(f, "Error while deleting BadRaw directory: %s" % e)
                f.close()
            raise e

    def moveBadFilesToArchiveBad(self):
        now = datetime.now()
        date = now.date()
        time = now.strftime("%H%M%S")
        try:
            source = 'Training_Raw_files_validated/Bad_Raw/'
            if os.path.isdir(source):
                path = 'TrainingArchiveBadData'
                if not os.path.isdir(path)
                    os.makedirs(path)
                dest = 'TrainingArchiveBadData/BadData_' + str(date) + '_' + str(time)
                if not os.path.isdir(dest):
                    os.makedirs(dest)
                files = os.listdir(source)
                for f in files:
                    if f not in os.listdir(dest):
                        shutil.move(source + f, dest)
                with open('Training_Logs/GeneralLog.txt', 'a+') as f:
                    self.logger.log(f, "Bad files moved to archive")
                    path = 'Training_Raw_files_validated/'
                    if os.path.isdir(path + 'Bad_Raw/'):
                        shutil.rmtree(path + 'Bad_Raw/')
                    self.logger.log(f, "BadRaw directory deleted successfully")
                    f.close()

        except Exception as e:
            with open('Training_Logs/GeneralLog.txt', 'a+') as f:
                self.logger.log(f, "Error while moving bad files to archive: %s" % e)
                f.close()
            raise e

