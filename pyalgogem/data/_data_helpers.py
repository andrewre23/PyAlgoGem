#
# PyAlgo Project
# data/helpers
#
# functions to assist in data tasks
#
# Andrew Edmonds - 2018
#

from numpy import NaN
from pandas import DataFrame

import datetime as dt
import tables as tb
import tstables as ts


def ensure_hdf5(name):
    """Ensure file is HDF5 file-type"""
    if not isinstance(name, str):
        raise ValueError('Please enter a valid name')
    if name[-3:] != '.h5':
        name += '.h5'
    return name


def ensure_datetime(datetime):
    """Ensure datetime file is compatible
    for HDF5 timeseries read/write"""
    if type(datetime) in [dt.datetime, dt.date]:
        return True
    else:
        return False


def ensure_timeseries(timeseries):
    """Ensure timeseries object is non-blank
    for HDF5 timeseries read/write"""
    if isinstance(timeseries, ts.TsTable):
        try:
            timeseries.min_dt()
        except TypeError:
            return False
        return True
    else:
        return False


def get_minmax_timeseries(timeseries):
    """Get min and max of timeseries on HDF5 file"""
    if isinstance(timeseries, ts.TsTable):
        try:
            min, max = timeseries.min_dt(), timeseries.max_dt()
        except TypeError:
            return None, None
        return min, max
    else:
        return None, None


def get_minmax_dataframe(dataframe):
    """Get min and max of datetime index of DataFrame object"""
    if isinstance(dataframe, DataFrame):
        min = convert_timestamp_to_datetime(dataframe.index.min())
        max = convert_timestamp_to_datetime(dataframe.index.max())
        if min is NaN or max is NaN:
            return None, None
        return min, max
    else:
        return None, None


def convert_timestamp_to_datetime(timestamp):
    """Convert timestamps to UTC local datetime objects"""
    return timestamp.tz_localize('UTC').to_pydatetime()
