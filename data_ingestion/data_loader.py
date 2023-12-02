import pandas as pd

class Data_Getter:
    """
    This class is responsible for obtaining training data from a specified source.

    Args:
    file_object (str): The path to the log file.
    logger_object (object): An instance of the logger class.

    Methods:
    get_data: Reads data from the specified source and returns it as a pandas DataFrame.

    """
    def __init__(self, file_object, logger_object):
        self.training_file='Training_FileFromDB\InputFile.csv'
        self.file_object=file_object
        self.logger_object=logger_object

    def get_data(self):
        """
        Reads data from the specified source and returns it as a pandas DataFrame.

        Returns:
        pandas.DataFrame: The training data.

        Raises:
        Exception: If data loading fails.

        """
        self.logger_object.log(self.file_object,'Entered the get_data method of the Data_Getter class')
        try:
            self.data= pd.read_csv(self.training_file) # reading the data file
            self.logger_object.log(self.file_object,'Data Load Successful.Exited the get_data method of the Data_Getter class')
            return self.data
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in get_data method of the Data_Getter class. Exception message: '+str(e))
            self.logger_object.log(self.file_object,
                                   'Data Load Unsuccessful.Exited the get_data method of the Data_Getter class')
            raise Exception()

