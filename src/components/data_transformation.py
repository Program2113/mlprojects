import sys
import os
import numpy as np, pandas as pd 

from dataclasses import dataclass

from sklearn.compose import ColumnTransformer 
from sklearn.impute import SimpleImputer 
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline

from src.exception import customException
from src.logger import logging 
from src.utils import save_object


@dataclass 
class DataTransformationConfig:
    preprocessor_obj_filepath = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_obj(self):
        try:
            numerical_features = ['writing score','reading score']
            categorical_features = ['gender','race/ethnicity','parental level of education','lunch','test preparation course']

            numerical_pipeline = Pipeline(
                steps = [
                    'imputer',SimpleImputer(strategy = 'median'),
                    ('scaler',StandardScaler()),
            
                ]
            )          
            logging.info("Numerical features scaling completed")


            categorical_pipeline = Pipeline(
               steps = [
                   ('imputer',SimpleImputer(strategy = 'most_frequent')),
                   ('one_hot_encoder',OneHotEncoder()),
                   ('scaler',StandardScaler())
               ] 
            )

            logging.info("Categorical features encoding completed")

            preprocessor = ColumnTransformer(
                [
                    ('Numerical_pipleine',numerical_pipeline,numerical_features),
                    ('Categorical_pipleine',categorical_pipeline,categorical_features),

                ]
            ) 
            return preprocessor
        
        except Exception as e:
            raise customException(e,sys)
        

    def initiate_data_transformation(self,train_path,test_path):
        
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Finished reading train and test data")

            logging.info("Obtaining preprocessor object")

            preprocessing_obj = self.get_data_transformer_obj()

            target_feature = "math score"
            numerical_features = ['writing score','reading score']

            input_feature_train_df = train_df.drop(target_feature)
            target_feature_train_df = train_df[target_feature]

            input_feature_test_df = test_df.drop(target_feature)
            target_feature_test_df = test_df[target_feature]

            logging.info("Applying preprocessing object on train and test dataset")

            input_feature_train = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test = preprocessing_obj.tranform(input_feature_test_df)

            train_arr = np.c_[input_feature_train, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test, np.array(target_feature_test_df)]

            logging.info("Saved preprocessing object.")
            
            save_object(
                filepath = self.data_transformation_config.preprocessor_obj_filepath,
                obj = preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_filepath
            )
        except Exception as e:
            raise customException(e,sys)
        

        
        