#
# PyAlgo Project
# data/helpers
#
# functions to assist in data tasks
#
# Andrew Edmonds - 2018
#

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
        return True
