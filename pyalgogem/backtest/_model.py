#
# PyAlgoGem Project
# backtest/model
#
# class definition for Model object
#
# Andrew Edmonds - 2018
#



class Model(object):
    """
    Object for training/testing machine learning
    models on dataset in Backtest object
    """
    def __init__(self,type):
        if type.lower() not in ['long-out','tiered']:
            raise ValueError("'type' must be 'long-out' or 'tiered'")
