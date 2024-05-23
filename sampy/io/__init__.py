"""
Module containing common sampy io tools.

# NOTES
# ----------------------------------------------------------------------------|


written March 2024
by Samuel Thorpe
"""


# # Imports
# -----------------------------------------------------|
from os.path import splitext
import dill
import json
import pandas as pd
import numpy as np
from sampy import SampyException


# # Common Loading/Munging/Saving/Path-Manipulation
# -----------------------------------------------------|
def batch_saver(dat, fout, **kargs):
    """General wrapper for saving data."""
    ext = splitext(fout)[-1]
    if ext == '.csv':
        dat.to_csv(fout, **kargs)
    elif ext == '.pkl':
        with open(fout, 'wb') as pkl:
            dill.dump(dat, pkl, **kargs)
    elif ext == '.txt':
        with open(fout, 'w') as txt:
            for lin in dat:
                txt.write('{}\n'.format(lin))
    elif ext == '.json':
        with open(fout, 'w') as jsn:
            json.dump(dat, jsn, indent=4, **kargs)
    elif ext == '.npy':
        np.save(fout, dat, **kargs)
    else:
        raise CommonIOException('Unrecognized Batch Extention')


def batch_loader(fin):
    """General wrapper for loading data."""
    ext = splitext(fin)[-1]
    if ext == '.csv':
        return pd.read_csv(fin)
    if ext == '.pkl':
        with open(fin, 'rb') as pkl:
            return dill.load(pkl)
    if ext == '.json':
        with open(fin, 'rb') as jsn:
            return json.load(jsn)
    # # else treat as text file
    with open(fin, 'rb') as txt:
        return txt.readlines()


# # General Exception Class
# -----------------------------------------------------|
CommonIOException = type('CommonIOException', (SampyException,), {})


# # Main Entry
# -----------------------------------------------------|
if __name__ == '__main__':
    pass
