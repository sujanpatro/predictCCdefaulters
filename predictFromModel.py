import pandas as pd
from Prediction_Raw_Data_Validation.predictionDataValidation import Prediction_Data_validation
from application_logging import logger
from data_ingestion import data_loader_prediction
from data_preprocessing import preprocessing
from file_operation import file_methods


class prediction:
    def __init__(self, path):
        self.log_writer = logger.App_Logger()
        self.file_object = open("Prediction_Logs/ModelPredictionLog.txt", 'a+')
        self.pred_data_val = Prediction_Data_validation(path)

    def predictionFromModel(self):
        try:
            self.pred_data_val.deletePredictionFile()
            self.log_writer.log(self.file_object, 'Start of Prediction')
            data_getter = data_loader_prediction.Data_Getter_Pred(self.file_object, self.log_writer)
            data = data_getter.get_data()

            preprocessor = preprocessing.Preprocessor(self.file_object, self.log_writer)

            is_null_present, cols_with_missing_values = preprocessor.is_null_present(data)
            if is_null_present:
                data = preprocessor.impute_missing_values(data, cols_with_missing_values)

            X = preprocessor.scale_numerical_columns(data)

            file_loader = file_methods.File_Operation(self.file_object, self.log_writer)
            kmeans = file_loader.load_model('KMeans')

            clusters = kmeans.predict(X)
            X['clusters'] = clusters
            clusters = X['clusters'].unique()
            predictions = []

            for i in clusters:
                cluster_data = X[X['clusters'] == i]
                cluster_data = cluster_data.drop(['clusters'], axis=1)
                model_name = file_loader.find_correct_model_file(i)
                model = file_loader.load_model(model_name)
                result = model.predict(cluster_data)

            final = pd.DataFrame(list(zip(result)), columns=['Predictions'])
            path = "Prediction_Output_File/Predictions.csv"
            final.to_csv("Prediction_Output_File/Predictions.csv", header=True, mode='a+')
            self.log_writer.log(self.file_object, "End of Prediction")
        except Exception as e:
            self.log_writer.log(self.file_object, "Error occurred while running prediction!! Error:: %s" % e)
            raise e
        return path
