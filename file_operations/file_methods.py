import pickle
import os
import shutil

class File_Operation:
    """
    This class is responsible for saving and loading machine learning models.

    Args:
        file_object (file): The log file to record messages.
        logger_object (object): The logger object for logging messages.

    Attributes:
        file_object (file): The log file.
        logger_object (object): The logger object.
        model_directory (str): The directory where models are saved.

    """

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.model_directory = 'models/'

    def save_model(self, model, filename):
        """
        Save the machine learning model to a file.

        Args:
            model (object): The machine learning model to be saved.
            filename (str): The name of the file to save the model.

        Returns:
            str: 'success' if the model is saved successfully.

        Raises:
            Exception: If there is an error while saving the model.

        """
        self.logger_object.log(self.file_object, 'Entered the save_model method of the File_Operation class')
        try:
            path = os.path.join(self.model_directory, filename)  # create a separate directory for each cluster
            if os.path.isdir(path):  # remove previously existing models for each cluster
                shutil.rmtree(self.model_directory)
                os.makedirs(path)
            else:
                os.makedirs(path)
            with open(path + '/' + filename + '.sav', 'wb') as f:
                pickle.dump(model, f)  # save the model to file
            self.logger_object.log(self.file_object, 'Model File ' + filename + ' saved. Exited the save_model method of the Model_Finder class')
            return 'success'
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in save_model method of the Model_Finder class. Exception message: ' + str(e))
            self.logger_object.log(self.file_object, 'Model File ' + filename + ' could not be saved. Exited the save_model method of the Model_Finder class')
            raise Exception()

    def load_model(self, filename):
        """
        Load a machine learning model from a file.

        Args:
            filename (str): The name of the file containing the model.

        Returns:
            object: The loaded machine learning model.

        Raises:
            Exception: If there is an error while loading the model.

        """
        self.logger_object.log(self.file_object, 'Entered the load_model method of the File_Operation class')
        try:
            with open(self.model_directory + filename + '/' + filename + '.sav', 'rb') as f:
                self.logger_object.log(self.file_object, 'Model File ' + filename + ' loaded. Exited the load_model method of the Model_Finder class')
                return pickle.load(f)
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in load_model method of the Model_Finder class. Exception message: ' + str(e))
            self.logger_object.log(self.file_object, 'Model File ' + filename + ' could not be loaded. Exited the load_model method of the Model_Finder class')
            raise Exception()

    def find_correct_model_file(self, cluster_number):
        """
        Find the correct model file based on the cluster number.

        Args:
            cluster_number (int): The cluster number for selecting the correct model.

        Returns:
            str: The name of the correct model file.

        Raises:
            Exception: If there is an error while finding the model file.

        """
        self.logger_object.log(self.file_object, 'Entered the find_correct_model_file method of the File_Operation class')
        try:
            self.cluster_number = cluster_number
            self.folder_name = self.model_directory
            self.list_of_model_files = []
            self.list_of_files = os.listdir(self.folder_name)
            for self.file in self.list_of_files:
                try:
                    if (self.file.index(str(self.cluster_number)) != -1):
                        self.model_name = self.file
                except:
                    continue
            self.model_name = self.model_name.split('.')[0]
            self.logger_object.log(self.file_object, 'Exited the find_correct_model_file method of the Model_Finder class.')
            return self.model_name
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in find_correct_model_file method of the Model_Finder class. Exception message: ' + str(e))
            self.logger_object.log(self.file_object, 'Exited the find_correct_model_file method of the Model_Finder class with Failure')
            raise Exception()
