#
# PyAlgo Project
# data/add_read
#
# functions to read/write from HDF5 files
#
# Andrew Edmonds - 2018
#

import tables as tb
import tstables as ts

from .data_helpers import ensure_datetime, ensure_hdf5


def append_to_datafile(symbol, data, file='data.h5'):
    """Append data (DataFrame) to HDF5 file"""
    try:
        if symbol.upper() not in ['BTC', 'ETH']:
            raise ValueError('Symbol must be BTC or ETH')
        file = ensure_hdf5(str(file))
        f = tb.open_file(file, 'a')
        if symbol.upper() == 'BTC':
            tseries = f.root.BTC._f_get_timeseries()
        else:
            tseries = f.root.ETH._f_get_timeseries()
        tseries.append(data)
        f.close()
    except:
        f.close()
        print("Error appending to {}".format(file))


def read_datafile(symbol, start, end, file='data.h5'):
    """Read historical data from HDF5 file
    into in-memory DataFrame"""
    # ensure datetime parameters are valid
    if not (ensure_datetime(start) | ensure_datetime(end)):
        raise ValueError('Must pass valid datetime arguments')
    # ensure start is prior to end
    if (start - end).total_seconds() >= 0:
        raise ValueError('Start time must be prior to end time')
    if symbol.upper() not in ['BTC', 'ETH']:
        raise ValueError('Symbol must be BTC or ETH')
    file = ensure_hdf5(str(file))

    try:
        f = tb.open_file(file, 'r')
        if symbol.upper() == 'BTC':
            ts = f.root.BTC._f_get_timeseries()
        else:
            ts = f.root.ETH._f_get_timeseries()
        dataset = ts.read_range(start, end)
        f.close()
        return dataset
    except:
        print("Error reading from to {}".format(file))
