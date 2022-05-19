from Training_Raw_data_validation.rawValidation import Raw_Data_validation
from DataTransform_Training.DataTransformation import dataTransform
from DataTypeValidation_Insertion_Training.DataTypeValidation import dBOperation
from application_logging import logger
import os

class train_validation:
    def __init__(self, path):
        self.raw_data = Raw_Data_validation(path)
        self.dataTransform = dataTransform()
        self.dBOperation = dBOperation()
        self.cwd = os.getcwd()
        self.file_object = open(self.cwd + 'Training_Main_Log.txt', 'a+')
        self.log_writer = logger.App_logger()

    def train_validation(self):
        try:
            self.log_writer.log(self.file_object, 'Start of Validation on files for Training')
            LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, noofcolumns = self.raw_data.ValuesFromSchema()
            regex = self.raw_data.manualRegexCreation()

            self.raw_data.validationFileNameRaw(regex, LengthOfDateStampInFile, LengthOfTimeStampInFile)
            self.raw_data.validateColumnLength(noofcolumns)
            self.raw_data.validateMissingValuesInWholeColumn()
            self.log_writer.log(self.file_object, "Raw data validation complete!!")

            self.log_writer.log(self.file_object, "Starting data transformation")
            self.dataTransform.replaceMissingWithNULL()
            self.log_writer.log(self.file_object, "Data transformation complete!!")

            self.log_writer.log(self.file_object, "Creating training database and tables for given schema")
            self.dBOperation.createTableDb('Training', column_names)
            self.log_writer.log(self.file_object, "Table creation completed!!")

            self.log_writer.log(self.file_object, "Insertion of good data into table started")
            self.dBOperation.insertIntoTableGoodData('Training')
            self.log_writer.log(self.file_object, "Insertion in table completed")

            self.log_writer.log(self.file_object, "Deleting good data folder!!")
            self.raw_data.deleteExistingGoodDataTrainingFolder()
            self.log_writer.log(self.file_object, "Good data folder deleted")

            self.log_writer.log(self.file_object, "Moving files to archive and deleting bad data folder")
            self.raw_data.moveBadFilesToArchiveBad()
            self.raw_data.deleteExistingBadDataTrainingFolder()
            self.log_writer.log(self.file_object, "Bad data moved to archive and bad data folder deleted!!")

            self.log_writer.log(self.file_object, "Validation Operation Completed!!!")

            self.log_writer.log(self.file_object, "Extracting csv file from table")
            self.dBOperation.selectingDatafromtableintocsv('Training')
            self.file_object.close()

        except Exception as e:
            raise e
