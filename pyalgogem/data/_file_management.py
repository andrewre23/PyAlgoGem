#
# PyAlgo Project
# data/file_management
#
# functions to manage HDF5 files
#
# Andrew Edmonds - 2018
#

import os
import shutil
import tables as tb
import tstables as ts

from ._data_helpers import ensure_datetime, ensure_hdf5


class CryptoCompareTable(tb.IsDescription):
    """
    Description of table to be used in HDF5 file
    Same structure for BTC and ETH
    """
    timestamp = tb.Int64Col(pos=0)
    close = tb.Float64Col(pos=1)
    high = tb.Float64Col(pos=2)
    low = tb.Float64Col(pos=3)
    open = tb.Float64Col(pos=4)
    vol_from = tb.Float64Col(pos=5)
    vol_to = tb.Float64Col(pos=6)


def create_datafile(name='data.h5'):
    """Create HDF5 file for data storage"""
    name = ensure_hdf5(str(name))
    if not os.path.isfile(name):
        h5 = tb.open_file(name, 'w')
        h5.create_ts('/', 'BTC', CryptoCompareTable)
        h5.create_ts('/', 'ETH', CryptoCompareTable)
        h5.close()
    return name


def copy_datafile(source, copy):
    """Duplicate HDF5 files"""
    source = ensure_hdf5(str(source))
    copy = ensure_hdf5(str(copy))
    try:
        shutil.copy(source, copy)
    except OSError:
        print('Error copying {}'.format(source))


def remove_datafile(name):
    """Delete HDF5 file"""
    name = ensure_hdf5(str(name))
    try:
        os.remove(name)
    except OSError:
        print('Error deleting {}'.format(name))
