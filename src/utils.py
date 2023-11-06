import os
import sys 
import pandas as pd, numpy as np 
import dill
import pickle 

from src.exception import customException 

def save_object(filepath, obj):
    try:
        dir_path = os.path.dirname(filepath)

        os.makedirs(dir_path, exist_ok = True)

        with open(filepath, 'wb') as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise customException(e, sys)