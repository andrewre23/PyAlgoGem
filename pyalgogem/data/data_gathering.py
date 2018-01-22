#
# PyAlgo Project
# data/data_gathering
#
#
# Andrew Edmonds - 2018
#

import os
import sys
import shutil


def initialize_data_directory(path=None, folder=None, over_write=False):
    """
    Function to create local directory for historical data storage

    path: string
        current dir will be used if no path chosen
    folder: string
        name of "datasets" will be used for folder if no name chosen
    over_write: bool
        delete and over-write if dir already exists
    return:
        directory of folder to use
    """
    if path is None:
        dir_path = os.getcwd()
    else:
        dir_path = str(path)

    if folder is None:
        dir_name = 'datasets'
    else:
        dir_name = str(folder)

    if 'win' in sys.platform.lower():
        spacing = '\\'
    else:
        spacing = '/'
    dir = dir_path + spacing + dir_name

    if os.path.exists(dir) and over_write:
        try:
            shutil.rmtree(dir)
            os.makedirs(dir)
        except OSError:
            print("Error creating directory.")
    elif not os.path.exists(dir):
        try:
            os.makedirs(dir)
        except OSError:
            print("Error creating directory")
    # return location of data directory
    return dir
