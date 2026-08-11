from dotenv import load_dotenv
import pandas as pd
import numpy as np
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException
import pymongo
import os
import sys
import json
import certifi

load_dotenv()

uri = os.getenv("MONGO_DB_URL")
ca = certifi.where()

import pandas as pd
import pymongo


class NetworkDataExtract:

    def __init__(self, uri):
        try:
            self.mongo_client = pymongo.MongoClient(uri)

        except Exception as e:
            raise CustomException(e)

    def csv_to_json(self, file_path):
        try:
            data = pd.read_csv(file_path)
            return data.to_dict("records")

        except Exception as e:
            raise CustomException(e)

    def insert_data_to_mongodb(self, records, database_name, collection_name):
        try:
            database = self.mongo_client[database_name]
            collection = database[collection_name]

            if records:
                result = collection.insert_many(records)
                return len(result.inserted_ids)

            return 0

        except Exception as e:
            raise CustomException(e)

if __name__ == "__main__":
    FILE_PATH =  "Network_Data/phisingData.csv"
    DATABASE = "AnantML"
    COLLECTION = "Network Security"
    network_obj = NetworkDataExtract(uri)
    records = network_obj.csv_to_json(file_path=FILE_PATH)
    no_of_records_inserted = network_obj.insert_data_to_mongodb(records=records, database_name=DATABASE, collection_name=COLLECTION)
    print(no_of_records_inserted)
    

