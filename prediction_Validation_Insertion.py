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
