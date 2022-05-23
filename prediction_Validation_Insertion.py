from DataTypeValidation_Insertion_Prediction.DataTypeValidationPrediction import dBOperation
from Prediction_Raw_Data_Validation.predictionDataValidation import Prediction_Data_validation
from application_logging import logger
from DataTransformation_Prediction.DataTransformationPrediction import dataTransformPredict


class pred_validation:
    def __init__(self, path):
        self.raw_data = Prediction_Data_validation(path)
        self.dBOperation = dBOperation()
        self.dataTransform = dataTransformPredict()
        self.file_object = open("Prediction_Logs/Prediction_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()

    def prediction_validation(self):
        try:
            self.log_writer.log(self.file_object, 'Start of Validation on files for Prediction')
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
            self.dBOperation.createTableDb('Prediction', column_names)
            self.log_writer.log(self.file_object, "Table creation completed!!")

            self.log_writer.log(self.file_object, "Insertion of good data into table started")
            self.dBOperation.insertIntoTableGoodData('Prediction')
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
            self.dBOperation.selectingDatafromtableintocsv('Prediction')
            self.file_object.close()

        except Exception as e:
            raise e
