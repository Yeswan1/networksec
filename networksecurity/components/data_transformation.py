import sys
import os
import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact
from networksecurity.entity.artifact_entity import DataValidationArtifact


class DataTransformation:
    def __init__(
        self,
        data_validation_artifact: DataValidationArtifact,
        data_transformation_config: DataTransformationConfig,
    ):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def get_data_transformer_object(self):
        try:
            # Simple pipeline (scaling)
            pipeline = Pipeline(
                steps=[
                    ("scaler", StandardScaler())
                ]
            )
            return pipeline
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self):
        try:
            logging.info("Starting data transformation")

            # ✅ Load data
            train_df = pd.read_csv(self.data_validation_artifact.valid_train_file_path)
            test_df = pd.read_csv(self.data_validation_artifact.valid_test_file_path)

            logging.info(f"Train shape: {train_df.shape}")
            logging.info(f"Test shape: {test_df.shape}")

            # 🔥 FIX: use label instead of Result
            target_column_name = "label"

            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            # ✅ Preprocessor
            preprocessing_obj = self.get_data_transformer_object()

            # Fit transform
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            # Combine input + target
            train_arr = np.c_[input_feature_train_arr, target_feature_train_df]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_df]

            # ✅ Save files
            os.makedirs(os.path.dirname(self.data_transformation_config.transformed_train_file_path), exist_ok=True)

            np.save(self.data_transformation_config.transformed_train_file_path, train_arr)
            np.save(self.data_transformation_config.transformed_test_file_path, test_arr)

            # Save preprocessor
            import pickle
            with open(self.data_transformation_config.preprocessor_obj_file_path, "wb") as f:
                pickle.dump(preprocessing_obj, f)

            logging.info("Data transformation completed")

            return DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                preprocessed_object_file_path=self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)
