""" Unit tests for proc_sample.read_csv function. """

# Currently there exists a few hacky bits of code because my directory structure is not designed to be a Python package.
# Therefore I can't use relative imports, and all nosetests must be run from the top-level directory.

import os
import sys
sys.path.append(os.getcwd())

import numpy as np
import proc_sample

def test_all_array(filename="motion_away_from_host.csv"):
    """ Test all CSV data are stored in `np.ndarray`. """
    path = os.path.join(os.getcwd(), 'tests')
    radar = proc_sample.read_csv(os.path.join(path, filename), verbose=False)
    assert all([isinstance(data, np.ndarray) for header, data in radar.items()])
    return
