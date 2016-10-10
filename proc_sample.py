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
import matplotlib.pyplot as plt
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
            for header, value in row.items():
                radar[header].append(ast.literal_eval(value))

    # convert lists to arrays
    for header, values in radar.items():
        radar[header] = np.asarray(values)

    if verbose:
        print("Number of headers: {}".format(len(radar)))
        print("Number of radar objects: {}".format(len(_parse_radar_objects(radar))))
        print("Number of time steps: {}".format(len(radar[header])))

    _add_object_range(radar)
    _add_object_radial_velocity(radar)

    return radar


def proc_radar(radar, use_longest_tracked=True, verbose=True):
    """
    Process radar and determine object which closely matches reference given trajectory and velocity data.

    :param radar: dict
        Dictionary containing all original headers and values in CSV.
    :param use_longest_tracked: bool
        True to process longest tracked radar object. Currently this is the only method available.
    :param verbose: bool, optional
        True to print useful information, False to suppress.
    """

    if use_longest_tracked:
        obj = _longest_tracked_object(radar, verbose=verbose)
    else:
        raise ValueError("Currently only the longest tracked radar object should be processed.")

    # plot trajectory and velocity data
    _plot_object_trajectory_and_velocity(radar, obj)

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


def _longest_tracked_object(radar, verbose=True):
    """ Determine longest tracked radar object given LifeCycles info. """

    cycle_max = []
    for obj in _parse_radar_objects(radar):
        cycle_max.append(max(radar[obj + cycle_field]))
    obj = _parse_radar_objects(radar)[np.argmax(cycle_max)]
    if verbose:
        print("Longest tracked radar object: {}".format(obj))

    return obj


def _plot_object_trajectory_and_velocity(radar, obj):
    """ Plot radar object trajectory and velocity, overlaid with reference data. """

    fig, (axa, axb) = plt.subplots(nrows=2, ncols=1, sharex=True, **{"figsize": (6, 10)})
    fig.subplots_adjust(hspace=0.2)

    # (a) radar object and reference trajectory
    axa.plot(radar["CycleCount"], radar["CAN Global.Range_tg1"], "k-", lw=2, alpha=0.5, label="ref")
    axa.plot(radar["CycleCount"], radar[obj + range_field], "b-", lw=1, label=obj)
    axa.set_ylim(0, 120)
    axa.set_title("ref vs {} trajectory".format(obj))
    axa.set_ylabel("range (m)")
    axa.grid(which="major")

    # (b) radar object and reference velocity
    axb.plot(radar["CycleCount"], radar["CAN Global.RelSpd_tg1"], "k-", lw=2, alpha=0.5, label="ref")
    axb.plot(radar["CycleCount"], radar[obj + vel_field], "b-", lw=1, label=obj)
    axb.set_ylim(-20, 20)
    axb.set_title("ref vs {} velocity".format(obj))
    axb.set_ylabel("velocity (kph)")
    axb.set_xlabel("CycleCount")
    axb.grid(which="major")

    plt.show()
    fig.savefig("reference_vs_object.png", format="png", dpi=300, bbox_inches="tight")  # saves figure in cwd

    return


if __name__ == "__main__":

    # parse command line arguments
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument("file", type=str)
    parser.add_argument("-v", "--verbose", nargs="?", const=True, default=False, type=bool)
    args = parser.parse_args()

    radar = read_csv(args.file, verbose=args.verbose)
    proc_radar(radar, verbose=args.verbose)