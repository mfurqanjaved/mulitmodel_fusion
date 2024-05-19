import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from src.logger import logging
from src.exception import CustomException
import os
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from src.utils import save_object



@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifact","preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.transformation_config = DataTransformationConfig()

    def get_data_transformer(self):
        try:
            numerical_colums=["writing_score","reading_score"]
            categorical_columns=["gender","race_ethnicity","parental_level_of_education","lunch","test_preparation_course"]
            numerical_pipeline=Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='median')),
                ('scaler',StandardScaler(with_mean=False))
            ])
            cat_pipeline=Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),
                ('onehot',OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
            ])
            preprocessor=ColumnTransformer(
                transformers=[
                    ('num',numerical_pipeline,numerical_colums),
                    ('cat',cat_pipeline,categorical_columns)
                ]
            )
            logging.info("column transformer initiated")

            return preprocessor
        
        except Exception as e:
            raise CustomException(e.sys)
        
    def initiate_data_transormation(self,train_path,test_path):
        try:
           train_df=pd.read_csv(train_path)
           test_df=pd.read_csv(test_path)

           logging.info("read the train and test data")
           logging.info("initiate the preprocessor")
           preprocessing_obj=self.get_data_transformer()
           target_column_name="math_score"
           numerical_colums=["writing_score","reading_score"]

           input_features=train_df.drop(target_column_name,axis=1)
           target_feature=train_df[target_column_name]

           input_feature_train_df=train_df.drop(target_column_name,axis=1)
           input_feature_test_df = test_df.drop(target_column_name, axis=1)
           target_feature_train_df=train_df[target_column_name]
           target_feature_test_df = test_df[target_column_name]

           logging.info(f"Applying the preprocessor on the input features")

           input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
           input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

           train_arr = np.c_[
               input_feature_train_arr, np.array(target_feature_train_df)
            ]
           test_arr=np.c_[input_feature_test_arr,np.array(target_feature_test_df)]
           logging.info("preprocessing is completed")

           save_object(
               file_path=self.transformation_config.preprocessor_obj_file_path,
               obj=preprocessing_obj
           )

           return (train_arr,test_arr,self.transformation_config.preprocessor_obj_file_path)


        except Exception as e:
            raise CustomException(e,sys)
                                 