#
# PyAlgoGem Project
# data/data_helpers
#
# functions to assist in data tasks
#
# Andrew Edmonds - 2018
#

import datetime as dt

from numpy import NaN
from pandas import DataFrame
from tstables import TsTable
from datetime import date, datetime


def convert_to_datetime(input_date):
    """
    Convert dt.date arguments to datetime
    """
    if type(input_date) == date:
        input_date = dt.datetime(year=input_date.year,
                           month=input_date.month,day=input_date.day)
    return input_date

def ensure_hdf5(name):
    """Ensure file is HDF5 file-type"""
    if not isinstance(name, str):
        raise ValueError('Please enter a valid name')
    if name[-3:] != '.h5':
        name += '.h5'
    return name


def ensure_datetime(dt):
    """
    Ensure datetime file is compatible
    for HDF5 timeseries read/write
    """
    if type(dt) in [datetime, date]:
        return True
    else:
        return False


def ensure_timeseries(timeseries):
    """
    Ensure timeseries object is non-blank
    for HDF5 timeseries read/write
    """
    if isinstance(timeseries, TsTable):
        try:
            timeseries.min_dt()
        except TypeError:
            return False
        return True
    else:
        return False


def get_minmax_timeseries(timeseries):
    """Get min and max of timeseries on HDF5 file"""
    if isinstance(timeseries, TsTable):
        try:
            tsmin, tsmax = timeseries.min_dt(), timeseries.max_dt()
        except TypeError:
            return None, None
        return tsmin, tsmax
    else:
        return None, None


def get_minmax_dataframe(dataframe):
    """Get min and max of datetime index of DataFrame object"""
    if isinstance(dataframe, DataFrame):
        dfmin = convert_timestamp_to_datetime(dataframe.index.min())
        dfmax = convert_timestamp_to_datetime(dataframe.index.max())
        if dfmin is NaN or dfmax is NaN:
            return None, None
        return dfmin, dfmax
    else:
        return None, None


def convert_timestamp_to_datetime(timestamp):
    """Convert timestamps to UTC local datetime objects"""
    return timestamp.tz_localize('UTC').to_pydatetime()


def select_new_values(dataframe, old_min, old_max):
    """
    Select subset of DataFrame that resides outside
    of the old min/max range
    """
    # add function to return nothing when new values occur
    # before old values, as cannot append retoractively
    new_min, new_max = get_minmax_dataframe(dataframe)
    # check if no timeseries exists (blank old min/max)
    # or if all new data comes after old data
    if (old_min is None or old_max is None) or (new_min > old_max):
        return dataframe
    # select only values newer than previous old max
    elif new_max > old_max:
        return dataframe[dataframe.index > old_max]
    # return None if no new data is more recent than old max
    else:
        return None
