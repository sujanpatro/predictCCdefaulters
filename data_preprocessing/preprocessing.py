import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


class Preprocessor:
    def __init__(self, file_object, logger_object):
        self.useful_data = None
        self.columns = None
        self.df_without_spaces = None
        self.data = None
        self.file_object = file_object
        self.logger_object = logger_object

    def remove_unwanted_spaces(self, data):
        self.logger_object.log(self.file_object, 'Entered the remove_unwanted_spaces method of the Preprocessor class')
        self.data = data

        try:
            self.df_without_spaces = self.data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)  # drop the labels specified in the columns
            self.logger_object.log(self.file_object,
                                   'Unwanted spaces removal successful. Exited the remove_unwanted_spaces method of the Preprocessor class')
            return self.df_without_spaces
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occurred in remove_unwanted_spaces method of the Preprocessor class. Exited method %s' % e)
            raise Exception()

    def remove_columns(self, data, columns):
        self.logger_object.log(self.file_object, 'Entered the remove_columns method of the Preprocessor class')
        self.data = data
        self.columns = columns
        try:
            self.useful_data = self.data.drop(labels=self.columns, axis=1)  # drop the labels specified in the columns
            self.logger_object.log(self.file_object,
                                   'Column removal Successful. Exited the remove_columns method of the Preprocessor class')
            return self.useful_data
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in remove_columns method of the Preprocessor class. Exited method %s' % e)
            raise e

    def separate_label_feature(self, data, label_column_name):
        pass
