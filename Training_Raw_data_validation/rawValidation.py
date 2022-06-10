import re
from datetime import datetime
import json
import os
import shutil
import pandas as pd

from application_logging.logger import App_Logger


class Raw_Data_validation:
    def __init__(self, path):
        self.Batch_directory = path
        self.schema_path = 'schema_training.json'
        self.logger = App_Logger()

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
            with open("Training_Logs/GeneralLog.txt", 'a+') as f:
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
                if not os.path.isdir(path):
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

    def validationFileNameRaw(self, regex, LengthOfDateStampInFile, LengthOfTimeStampInFile):
        self.deleteExistingBadDataTrainingFolder()
        self.deleteExistingGoodDataTrainingFolder()
        self.createDirectoryForGoodBadRawData()

        onlyfiles = [f for f in os.listdir(self.Batch_directory)]

        try:
            f = open("Training_Logs/nameValidationLog.txt", "a+")
            for filename in onlyfiles:
                if re.match(regex, filename):
                    splitAtDot = re.split('.csv', filename)
                    splitAtDot = re.split('_', splitAtDot[0])

                    if len(splitAtDot[1]) == LengthOfDateStampInFile:
                        if len(splitAtDot[2]) == LengthOfTimeStampInFile:
                            shutil.copy("Training_Batch_Files/" + filename, "Training_Raw_files_validated/Good_Raw")
                            self.logger.log(f, "Valid File name! File copied to validated -> GoodRaw folder :: filename: %s" % filename)

                        else:
                            shutil.copy("Training_Batch_Files/" + filename, "Training_Raw_files_validated/Bad_Raw")
                            self.logger.log(f, "Invalid File name! File copied to validated -> BadRaw folder :: filename: %s" % filename)

                    else:
                        shutil.copy("Training_Batch_Files/" + filename, "Training_Raw_files_validated/Bad_Raw")
                        self.logger.log(f, "Invalid File name! File copied to validated -> BadRaw folder :: filename: %s" % filename)

                else:
                    shutil.copy("Training_Batch_Files/" + filename, "Training_Raw_files_validated/Bad_Raw")
                    self.logger.log(f, "Invalid File name! File copied to validated -> BadRaw folder :: filename: %s" % filename)
            f.close()

        except Exception as e:
            with open("Training_Logs/nameValidationLog.txt", 'a+') as f:
                self.logger.log(f, "Error occurred while validating filename %s" % e)
                f.close()
            raise e

    def validateColumnLength(self, NumberOfColumns):
        try:
            f = open("Training_Logs/columnsValidationLog.txt", 'a+')
            self.logger.log(f, "Column length validation started")
            for file in os.listdir("Training_Raw_files_validated/Good_Raw"):
                df = pd.read_csv("Training_Raw_files_validated/Good_Raw/" + file)
                if df.shape[1] != NumberOfColumns:
                    shutil.move("Training_Raw_files_validated/Good_Raw/" + file, "Training_Raw_files_validated/Bad_Raw/")
                    self.logger.log(f, "Invalid Columns Length for the file!! File moved to Bad Raw Folder :: %s" % file)
            self.logger.log(f, "Column length validation completed")

        except OSError as e:
            with open("Training_Logs/columnValidationLog.txt", 'a+') as f:
                self.logger.log(f, "Error Occurred while moving files %s" % e)
                f.close()
            raise e
        except Exception as e:
            with open("Training_Logs/columnValidationLog.txt", 'a+') as f:
                self.logger.log(f, "Error Occurred :: %s" % e)
                f.close()
            raise e

        finally:
            f.close()

    def validateMissingValuesInWholeColumn(self):
        try:
            f = open("Training_Logs/missingValuesInColumn.txt", 'a+')
            self.logger.log(f, "Missing Values Validation Started!!")

            for file in os.listdir("Training_Raw_files_validated/Good_Raw/"):
                df = pd.read_csv("Training_Raw_files_validated/Good_Raw/" + file)
                found = False
                for columns in df:
                    if len(df[columns]) - df[columns].count() == len(df[columns]):
                        found = True
                        shutil.move("Training_Raw_files_validated/Good_Raw/" + file, "Training_Raw_files_validated/BAD_Raw/")
                        self.logger.log(f, "Invalid Column for the file!! File moved to Bad Raw folder :: %s" %file)
                        break
                if not found:
                    df.to_csv("Training_Raw_files_validated/Good_Raw/" + file, index=None, header=True)
            f.close()

        except OSError as e:
            with open("Training_Logs/missingValuesInColumns.txt", 'a+') as f:
                self.logger.log(f, "Error occurred while moving the file :: %s" % e)
                f.close()
            raise e
        except Exception as e:
            with open("Training_Logs/columnValidationLog.txt", 'a+') as f:
                self.logger.log(f, "Error Occurred :: %s" % e)
                f.close()
            raise e
