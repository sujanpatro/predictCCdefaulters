import pandas as pd


class Data_Getter_Pred:
    def __init__(self, file_object, logger_object):
        self.prediction_file = 'Prediction_FileFromDB/InputFile.csv'
        self.file_object = file_object
        self.logger_object = logger_object

    def get_data(self):
        self.logger_object.log(self.file_object, "Enter the get_data method of the Data_Getter class")
        try:
            self.data = pd.read_csv(self.prediction_file)
            self.logger_object.log(self.file_object,
                                   "Data loaded successfully. Exited the get_data method of the Data_Getter class")
            return self.data

        except Exception as e:
            self.logger_object.log(self.file_object, "Data load unsuccessful. Exited get_data method. %s" % e)
            raise e
