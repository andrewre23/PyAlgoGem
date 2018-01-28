#
# PyAlgo Project
# data/helpers
#
# functions to assist in data tasks
#
# Andrew Edmonds - 2018
#


def ensure_hdf5(name):
    """Ensure file is HDF5 file-type"""
    if name[-3:] != '.h5':
        name += '.h5'
    return name


def ensure_datetime(datetime):
    """Ensure datetime file is compatible
    for HDF5 timeseries read/write"""
    if type(datetime) not in [dt.datetime, dt.date]:
        return False
    else:
        return True
