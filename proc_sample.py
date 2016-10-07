"""
proc_sample
===========

Program to read radar data sample in CSV format and characterize positional and velocity errors of
radar objects relative to reference object.

.. autosummary::
    :toctree: generated/

    read_csv
    proc_radar
    _add_object_range
    _add_object_radial_velocity
    _parse_radar_objects
    _longest_tracked_object

"""

import csv
import ast
import argparse
import numpy as np
from collections import defaultdict

object_field = "aObject"
xdisp_field = ".Kinematic.fDistX"
ydisp_field = ".Kinematic.fDistY"
xvel_field = ".Kinematic.fVrelX"
yvel_field = ".Kinematic.fVrelY"
cycle_field = ".General.uiLifeCycles"

range_field = ".Kinematic.fRange"  # object range field name
vel_field = ".Kinematic.fVrel"  # object radial velocity field name


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
    with open(filename, mode="r") as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=None, quoting=csv.QUOTE_NONE, dialect="excel")
        for row in reader:
            for header, value in row.iteritems():
                radar[header].append(ast.literal_eval(value))

    # convert lists to arrays
    for header, values in radar.iteritems():
        radar[header] = np.asarray(values)

    if verbose:
        print("Number of headers: {}".format(len(radar)))
        print("Number of radar objects: {}".format(len(_parse_radar_objects(radar))))
        print("Number of time steps: {}".format(len(radar[header])))
        _longest_tracked_object(radar)

    _add_object_range(radar)
    _add_object_radial_velocity(radar)

    return radar


def proc_radar(radar, verbose=True):
    """
    Process all radar objects and determine object which closely matches reference given trajectory and velocity data.

    :param radar: dict
        Dictionary containing all original headers and values in CSV.
    :param verbose: bool, optional
        True to print useful information, False to suppress.
    """

    # process trajectory data
    for obj in _parse_radar_objects(radar):
        continue

    # process velocity data
    for obj in _parse_radar_objects(radar):
        continue

    return


def _add_object_range(radar):
    """ Add range from host vehicle for each radar object given (x, y) displacements. """

    for obj in _parse_radar_objects(radar):
        _range = np.sqrt(radar[obj + xdisp_field]**2.0 + radar[obj + ydisp_field]**2.0)
        radar[obj + range_field] = _range  # units of meters

    return


def _add_object_radial_velocity(radar):
    """
    Add host vehicle line-of-sight (radial) velocity for each radar object given (x, y) component velocities. Objects
    moving towards the host vehicle should have negative velocity. According to Steven Gerd, positive x is north and
    positive y is west.
    """

    for obj in _parse_radar_objects(radar):
        theta = np.arctan2(radar[obj + xdisp_field], radar[obj + ydisp_field])
        vrel = radar[obj + yvel_field] * np.cos(theta) + radar[obj + xvel_field] * np.sin(theta)  # units are mps
        radar[obj + vel_field] = 3600.0 * vrel / 1000.0  # convert mps to kph

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
    proc_radar(radar, verbose=args.verbose)