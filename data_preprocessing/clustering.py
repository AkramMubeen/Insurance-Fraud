import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
from file_operations import file_methods

class KMeansClustering:
    """
    This class is responsible for dividing the data into clusters before training.

    Args:
    file_object (str): The path to the log file.
    logger_object (object): An instance of the logger class.

    Methods:
    elbow_plot: Saves the plot to decide the optimum number of clusters to a file.
    create_clusters: Creates a new dataframe consisting of the cluster information.
    """

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object

    def elbow_plot(self, data):
        """
        Saves the plot to decide the optimum number of clusters to the file.

        Args:
        data (pandas.DataFrame): The data used for clustering.

        Returns:
        int: The optimum number of clusters.

        Raises:
        Exception: If finding the number of clusters fails.
        """
        self.logger_object.log(self.file_object, 'Entered the elbow_plot method of the KMeansClustering class')
        wcss = []  # initializing an empty list
        try:
            for i in range(1, 11):
                kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)  # initializing the KMeans object
                print("Data Features",data.columns)
                kmeans.fit(data)  # fitting the data to the KMeans Algorithm
                wcss.append(kmeans.inertia_)
            plt.plot(range(1, 11), wcss)  # creating the graph between WCSS and the number of clusters
            plt.title('The Elbow Method')
            plt.xlabel('Number of clusters')
            plt.ylabel('WCSS')
            plt.savefig('preprocessing_data/K-Means_Elbow.PNG')  # saving the elbow plot locally
            # finding the value of the optimum cluster programmatically
            self.kn = KneeLocator(range(1, 11), wcss, curve='convex', direction='decreasing')
            self.logger_object.log(self.file_object, 'The optimum number of clusters is: ' + str(self.kn.knee) + ' . Exited the elbow_plot method of the KMeansClustering class'+ ' \n Data Features'+ str(data.columns))
            return self.kn.knee

        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in elbow_plot method of the KMeansClustering class. Exception message: ' + str(e))
            self.logger_object.log(self.file_object, 'Finding the number of clusters failed. Exited the elbow_plot method of the KMeansClustering class')
            raise Exception()

    def create_clusters(self, data, number_of_clusters):
        """
        Create a new dataframe consisting of the cluster information.

        Args:
        data (pandas.DataFrame): The data to be clustered.
        number_of_clusters (int): The number of clusters to create.

        Returns:
        pandas.DataFrame: A dataframe with a 'Cluster' column.

        Raises:
        Exception: If fitting the data to clusters fails.
        """
        self.logger_object.log(self.file_object, 'Entered the create_clusters method of the KMeansClustering class')
        self.data = data
        try:
            self.kmeans = KMeans(n_clusters=number_of_clusters, init='k-means++', random_state=42)
            self.y_kmeans = self.kmeans.fit_predict(data)  # divide data into clusters

            self.file_op = file_methods.File_Operation(self.file_object, self.logger_object)
            self.save_model = self.file_op.save_model(self.kmeans, 'KMeans')  # saving the KMeans model to directory

            self.data['Cluster'] = self.y_kmeans  # create a new column in the dataset for storing the cluster information
            self.logger_object.log(self.file_object, 'Successfully created ' + str(self.kn.knee) + ' clusters. Exited the create_clusters method of the KMeansClustering class')
            return self.data
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in create_clusters method of the KMeansClustering class. Exception message: ' + str(e))
            self.logger_object.log(self.file_object, 'Fitting the data to clusters failed. Exited the create_clusters method of the KMeansClustering class')
            raise Exception()
