#
# PyAlgoGem Project
# backtest/model
#
# class definition for Model object
#
# Andrew Edmonds - 2018
#

from sklearn.ensemble import forest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

class Model(object):
    """
    Object for training/testing machine learning
    models on dataset in Backtest object
    """
    def __init__(self, model_type):
        if model_type.lower() not in ['long-out','tiered']:
            raise ValueError("'model_type' must be 'long-out' or 'tiered'")
