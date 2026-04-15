import os
import sys
from datetime import datetime

from networksecurity.exception.exception import NetworkSecurityException


class TrainingPipelineConfig:
    def __init__(self):
        try:
            timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
            self.timestamp = timestamp

            self.artifact_dir = os.path.join("artifact", timestamp)

            self.model_dir = os.path.join(self.artifact_dir, "final_model")

        except Exception as e:
            raise NetworkSecurityException(e, sys)


# ✅ FIXED
class DataIngestionConfig:
    def __init__(
        self,
        training_pipeline_config: TrainingPipelineConfig,
        database_name="networksecurity",
        collection_name="data"
    ):
        try:
            self.database_name = database_name
            self.collection_name = collection_name

            self.feature_store_file_path = os.path.join(
                training_pipeline_config.artifact_dir,
                "data_ingestion",
                "feature_store",
                "data.csv"
            )

            self.training_file_path = os.path.join(
                training_pipeline_config.artifact_dir,
                "data_ingestion",
                "dataset",
                "train.csv"
            )

            self.testing_file_path = os.path.join(
                training_pipeline_config.artifact_dir,
                "data_ingestion",
                "dataset",
                "test.csv"
            )

            self.train_test_split_ratio = 0.2

        except Exception as e:
            raise NetworkSecurityException(e, sys)


# ✅ FIXED (THIS WAS YOUR ERROR)
class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            self.schema_file_path = os.path.join(
                "config", "schema.yaml"
            )

            # ✅ Drift report
            self.drift_report_file_path = os.path.join(
                training_pipeline_config.artifact_dir,
                "data_validation",
                "drift_report",
                "report.yaml"
            )

            # 🔥 ADD THESE (YOUR CURRENT ERROR FIX)
            self.valid_train_file_path = os.path.join(
                training_pipeline_config.artifact_dir,
                "data_validation",
                "validated",
                "train.csv"
            )

            self.valid_test_file_path = os.path.join(
                training_pipeline_config.artifact_dir,
                "data_validation",
                "validated",
                "test.csv"
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)


class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            self.transformed_train_file_path = os.path.join(
                training_pipeline_config.artifact_dir,
                "data_transformation",
                "train.npy"
            )

            self.transformed_test_file_path = os.path.join(
                training_pipeline_config.artifact_dir,
                "data_transformation",
                "test.npy"
            )

            self.preprocessor_obj_file_path = os.path.join(
                training_pipeline_config.artifact_dir,
                "data_transformation",
                "preprocessor.pkl"
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)


class ModelTrainerConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            self.trained_model_file_path = os.path.join(
                training_pipeline_config.artifact_dir,
                "model_trainer",
                "model.pkl"
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)
