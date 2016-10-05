"""
proc_sample
===========

"""

import csv
import ast
import argparse
import numpy as np
from collections import defaultdict

object_field = "aObject"
xdisp_field = ".Kinematic.fDistX"
ydisp_field = ".Kinematic.fDistY"
cycle_field = ".General.uiLifeCycles"

def read_csv(filename, verbose=True):
    """
    Read CSV file of sample data.

    :param filename: str
        File name including path of CSV.
    :param verbose: bool, optional
        True to print useful information, False to suppress.
    :return: dict
        Dictionary containing all original headers and values of CSV.
    """

    radar = defaultdict(list)
    with open(filename, mode="rb") as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=None, quoting=csv.QUOTE_NONE,
                                restkey=None, restval=None, dialect="excel")
        for row in reader:
            for header, value in row.iteritems():
                radar[header].append(ast.literal_eval(value))

    if verbose:
        print("Number of headers: {}".format(len(radar)))
        print("Number of radar objects: {}".format(len(_parse_radar_objects(radar))))
        print("Number of time steps: {}".format(len(radar[header])))
        _longest_tracked_object(radar)

    _add_object_range(radar)

    return radar


def _add_object_range(radar, range_field=".Kinematic.fRange"):
    """ Add range from host vehicle for each radar object given (x, y) displacements. """

    for obj in _parse_radar_objects(radar):
        _range = np.sqrt(np.power(radar[obj + xdisp_field], 2.0) + np.power(radar[obj + ydisp_field], 2.0))
        radar[obj + range_field] = _range

    return


def _parse_radar_objects(radar):
    """ Parse all radar objects and return list of names, e.g., 'aObject[3]'. """

    nobj = len([header for header in radar if xdisp_field in header])
    radar_objects = ["{}[{}]".format(object_field, i) for i in range(nobj)]
    return radar_objects


def _longest_tracked_object(radar):
    """ Determine longest tracked radar object given LifeCycles info. """

    cycle_max = []
    for obj in _parse_radar_objects(radar):
        cycle_max.append(max(radar[obj + cycle_field]))
    print("Longest tracked radar object: {}".format(_parse_radar_objects(radar)[np.argmax(cycle_max)]))
    return


if __name__ == "__main__":

    # parse command line arguments
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument("file", type=str)
    parser.add_argument("-v", "--verbose", nargs="?", const=True, default=False, type=bool)
    args = parser.parse_args()

    radar = read_csv(args.file, verbose=args.verbose)






