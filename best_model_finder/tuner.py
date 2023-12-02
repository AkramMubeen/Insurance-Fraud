from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score, accuracy_score

class Model_Finder:
    """
    This class is used to find the model with the best accuracy and AUC score.
    """

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.logistic_regression = LogisticRegression()
        self.xgb = XGBClassifier(objective='binary:logistic', n_jobs=-1)

    def get_best_params_for_logistic_regression(self, train_x, train_y):
        """
        Get the parameters for the Logistic Regression Algorithm that give the best accuracy.
        Use Hyper Parameter Tuning.
        """
        self.logger_object.log(self.file_object, 'Entered get_best_params_for_logistic_regression method')
        try:
            # Initialize with different combinations of parameters
            param_grid = {
                "penalty": ['l1', 'l2'],
                "C": [0.01, 0.1, 1.0, 10.0]
            }

            # Create an object of the Grid Search class
            grid = GridSearchCV(estimator=self.logistic_regression, param_grid=param_grid, cv=5, verbose=3)
            # Find the best parameters
            grid.fit(train_x, train_y)

            # Extract the best parameters
            penalty = grid.best_params_['penalty']
            C = grid.best_params_['C']

            # Create a new model with the best parameters
            self.logistic_regression = LogisticRegression(penalty=penalty, C=C)
            # Train the new model
            self.logistic_regression.fit(train_x, train_y)
            self.logger_object.log(self.file_object,
                                   'Logistic Regression best params: ' + str(grid.best_params_) +
                                   '. Exited get_best_params_for_logistic_regression method')
            return self.logistic_regression
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occurred in get_best_params_for_logistic_regression method. '
                                   'Exception message: ' + str(e))
            self.logger_object.log(self.file_object,
                                   'Logistic Regression training failed. Exited get_best_params_for_logistic_regression method')
            raise Exception()

    def get_best_params_for_xgboost(self, train_x, train_y):
        """
        Get the parameters for the XGBoost Algorithm that give the best accuracy.
        Use Hyper Parameter Tuning.
        """
        self.logger_object.log(self.file_object, 'Entered get_best_params_for_xgboost method')
        try:
            # Initialize with different combinations of parameters
            param_grid_xgboost = {
                "n_estimators": [100, 130],
                "learning_rate": ['0.1', '0.01'],
                "max_depth": range(8, 10, 1)
            }

            # Create an object of the Grid Search class
            grid = GridSearchCV(XGBClassifier(objective='binary:logistic'), param_grid_xgboost, verbose=3, cv=5)
            # Find the best parameters
            grid.fit(train_x, train_y)

            # Extract the best parameters
            learning_rate = grid.best_params_['learning_rate']
            max_depth = grid.best_params_['max_depth']
            n_estimators = grid.best_params_['n_estimators']

            # Create a new model with the best parameters
            self.xgb = XGBClassifier(learning_rate=learning_rate, max_depth=max_depth, n_estimators=n_estimators, n_jobs=-1)
            # Train the new model
            self.xgb.fit(train_x, train_y)
            self.logger_object.log(self.file_object,
                                   'XGBoost best params: ' + str(grid.best_params_) +
                                   '. Exited get_best_params_for_xgboost method')
            return self.xgb
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occurred in get_best_params_for_xgboost method. '
                                   'Exception message: ' + str(e))
            self.logger_object.log(self.file_object,
                                   'XGBoost Parameter tuning failed. Exited get_best_params_for_xgboost method')
            raise Exception()

    def get_best_model(self, train_x, train_y, test_x, test_y):
        """
        Find the model with the best AUC score.
        Output: The best model name and the model object.
        """
        self.logger_object.log(self.file_object, 'Entered get_best_model method')
        try:
            # Create the best model for Logistic Regression
            self.logistic_regression = self.get_best_params_for_logistic_regression(train_x, train_y)
            self.prediction_logistic = self.logistic_regression.predict(test_x)  # Predictions using Logistic Regression

            if len(test_y.unique()) == 1:  # If there is only one label in y, use accuracy
                self.logistic_regression_score = accuracy_score(test_y, self.prediction_logistic)
                self.logger_object.log(self.file_object, 'Accuracy for Logistic Regression:' + str(
                    self.logistic_regression_score))  # Log accuracy
            else:
                self.logistic_regression_score = roc_auc_score(test_y, self.prediction_logistic)  # AUC for Logistic Regression
                self.logger_object.log(self.file_object, 'AUC for Logistic Regression:' + str(
                    self.logistic_regression_score))  # Log AUC

            # Create the best model for XGBoost
            self.xgb = self.get_best_params_for_xgboost(train_x, train_y)
            self.prediction_xgboost = self.xgb.predict(test_x)  # Predictions using XGBoost

            if len(test_y.unique()) == 1:  # If there is only one label in y, use accuracy
                self.xgboost_score = accuracy_score(test_y, self.prediction_xgboost)
                self.logger_object.log(self.file_object, 'Accuracy for XGBoost:' + str(self.xgboost_score))  # Log accuracy
            else:
                self.xgboost_score = roc_auc_score(test_y, self.prediction_xgboost)  # AUC for XGBoost
                self.logger_object.log(self.file_object, 'AUC for XGBoost:' + str(self.xgboost_score))  # Log AUC

            # Compare the two models
            if self.logistic_regression_score < self.xgboost_score:
                return 'XGBoost', self.xgb
            else:
                return 'Logistic Regression', self.logistic_regression

        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occurred in get_best_model method. Exception message: ' + str(e))
            self.logger_object.log(self.file_object, 'Model Selection Failed. Exited get_best_model method')
            raise Exception()
