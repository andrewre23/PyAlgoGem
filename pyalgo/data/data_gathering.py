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


def initialize_dataset_directory(path=None, folder=None, over_write=False):
    # Function to create local directory
    # to store data files for prices
    #
    # Returns directory of folder to use

    # determine path of folder to use
    if path is None:
        dir_path = os.getcwd()
    else:
        dir_path = path

    # determine folder name
    if folder is None:
        dir_name = 'datasets'
    else:
        dir_name = folder

    # determine spacing based on OS
    if 'win' in sys.platform.lower():
        spacing = '\\'
    else:
        spacing = '/'
    dir = dir_path + spacing + dir_name

    # check if folder to use exists
    # and overwrite if asked to
    if os.path.exists(dir):
        if over_write:
            shutil.rmtree(dir)
            os.makedirs(dir)
    else:
        os.makedirs(dir)

    # return location of data directory
    return dir
