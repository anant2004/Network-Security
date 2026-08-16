import os, sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig

from networksecurity.constants.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object

class DataTransformation():
    def __init__(self,data_validation_artifact:DataValidationArtifact, data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise CustomException(e)

    @staticmethod
    def read_data(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e)

    def get_data_transformer_object(cls) -> Pipeline:
        # it initialises a KNNImputer object with the parameters DATA_TRANSFORMATION_IMPUTER_PARAMS and return a pipeline object

        logging.info("Enterd get_data_transformer_object of DataTranaformation class")
        try:
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"initialisis knnimputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processor:Pipeline = Pipeline([("imputer", imputer)])
            return processor            

        except Exception as e:
            raise CustomException(e)


    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Entered initiate_data_transformation method of DataTransformation class")
            logging.info("Starting data transformation")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            #removing target column of train dataframe

            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN])
            target_feature_train_df = train_df[TARGET_COLUMN]
            #replacing all -1 with 0 in target coloumn
            target_feature_train_df = target_feature_train_df.replace(-1, 0)

            #removing target column of test dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN])
            target_feature_test_df = test_df[TARGET_COLUMN]
            #replacing all -1 with 0 in target coloumn
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            preprocessor = self.get_data_transformer_object()
            preprocessor_obj = preprocessor.fit(input_feature_train_df)

            #both these transformed input train and test features will be an array

            transformed_input_train_feature = preprocessor_obj.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_obj.transform(input_feature_test_df)      

            # we will now concatenate this array

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            # save numpy array data

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_obj)
            save_object(os.path.join("final_model", "preprocessor.pkl"), preprocessor_obj)

            #preparing artifacts

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifact

        except Exception as e:
            raise CustomException(e)