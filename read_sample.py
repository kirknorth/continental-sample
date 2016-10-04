"""
read_sample
===========

"""

import argparse
import csv
from collections import defaultdict

def read_csv(filename, verbose=True):
    """
    Read CSV file of sample data.

    :param filename: str
        File name including path of CSV.
    :param verbose: bool, optional
        True to print useful information, False to suppress.
    :return: dict
        Dictionary containing original headers and values of CSV.
    """

    radar = defaultdict(list)
    with open(filename, mode='rb') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=None, restkey=None, restval=None, dialect='excel')
        for row in reader:
            for header, value in row.iteritems():
                radar[header].append(value)

    if verbose:
        print('Number of headers: {}'.format(len(radar)))
        print('Number of time steps: {}'.format(len(radar[header])))

    return radar


if __name__ == '__main__':

    # parse command line arguments
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('file', type=str)
    parser.add_argument('-v', '--verbose', nargs='?', const=True, default=False, type=bool)
    args = parser.parse_args()

    radar = read_csv(args.file, verbose=args.verbose)






