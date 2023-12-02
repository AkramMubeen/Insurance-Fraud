from datetime import datetime
from os import listdir
import pandas as pd
from application_logging.logger import App_Logger

class dataTransform:
    """
    This class is used to transform the Good Raw Training Data before loading it into the Database.

    """

    def __init__(self):
        self.goodDataPath = "Training_Raw_files_validated/Good_Raw"
        self.logger = App_Logger()

    def replaceMissingWithNull(self):
        """
        Method Name: replace_missing_with_null
        Description: Replaces the missing values in columns with "NULL" to store in the table.
                     It uses quotes to enclose values in string columns.
                     The first column containing integers is kept as is for future reference, as it will be removed during training.

        """
        log_file = open("Training_Logs/dataTransformLog.txt", 'a+')
        try:
            onlyfiles = [f for f in listdir(self.goodDataPath)]
            for file in onlyfiles:
                data = pd.read_csv(self.goodDataPath + "/" + file)
                # List of columns with string datatype variables
                columns = ["policy_bind_date", "policy_state", "policy_csl", "insured_sex", "insured_education_level",
                           "insured_occupation", "insured_hobbies", "insured_relationship", "incident_state",
                           "incident_date", "incident_type", "collision_type", "incident_severity",
                           "authorities_contacted", "incident_city", "incident_location", "property_damage",
                           "police_report_available", "auto_make", "auto_model", "fraud_reported"]

                for col in columns:
                    data[col] = data[col].apply(lambda x: "'" + str(x) + "'")

                data.to_csv(self.goodDataPath + "/" + file, index=None, header=True)
                self.logger.log(log_file, " %s: Quotes added successfully!!" % file)
        except Exception as e:
            self.logger.log(log_file, "Data Transformation failed because:: %s" % str(e))
        finally:
            log_file.close()



