#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Import python libraries
import sys
import argparse
import networkx as nx

# Import custom python libraries
try:
    from pyrainbowterm import *
except ImportError:
    print('Can not import pyrainbowterm!', log_type='error')
    print('Try: pip install pyrainbowterm', log_type='hint')
    sys.exit(1)

# Import file_operations
import file_operations

# Source code meta data
__author__ = 'Dalwar Hossain'
__email__ = 'dalwar.hossain@protonmail.com'


# Get data for value for graph
def is_weighted(weighted=None):
    """
    Gets the data value for networkx graph
    :param weighted: yes/no boolean
    :return: data value for networkx graph
    """
    # Assign data based on weighted or not
    if weighted == "yes" or weighted == "Yes" or weighted == "Y" or weighted == "y":
        data_ = True
    elif weighted == "no" or weighted == "No" or weighted == "N" or weighted == "n":
        data_ = False
    else:
        print('Please provide weighted (-w) argument with yes/no, y/n, Yes/No', log_type='error')
        sys.exit(1)
    # Return
    return data_


# Compose graph with networkx library
def compose_graph(input_file=None, delimiter=None, weighted=None):
    """

    :param input_file: Input file path
    :param delimiter: Optional separator for he column of the input file
    :param weighted: Simple yes/no if the input file is weighted or not
    :return: networkx graph
    """
    # Check for headers
    detected_delimiter, headers, n_cols, skip_n_rows = file_operations.check_header(input_file)

    # Header ?
    if headers:
        if headers[0].startswith('#'):
            pass
        else:
            print('Headers detected!', log_type='warn')
            print('Please comment [#] or delete header!', log_type='hint')

    print('Provided delimiter: {}'.format(delimiter), log_type='info')
    print('Detected delimiter: {}'.format(detected_delimiter), log_type='info')

    if detected_delimiter != delimiter:
        print('Delimiter mismatch!', log_type='warn')

    # Check the number of columns in the file
    print('Detected columns: {}'.format(n_cols), log_type='info')
    if n_cols < 2 or n_cols >= 4:
        print('Too less/many columns!', log_type='error')
        print('Hint: Check input file!', log_type='hint')
        sys.exit(1)

    # Get data for networkx graph
    file_is_weighted = is_weighted(weighted)

    # Create a networkx graph from the edgelist
    if file_is_weighted:
        try:
            ntx_graph = nx.read_weighted_edgelist(input_file, delimiter=delimiter)
        except Exception as e:
            print('Can not load input dataset. ERROR: {}'.format(e), color='red', log_type='error')
            sys.exit(1)
    else:
        try:
            ntx_graph = nx.read_edgelist(input_file, delimiter=delimiter)
        except Exception as e:
            print('Can not load input dataset. ERROR: {}'.format(e), color='red', log_type='error')
            sys.exit(1)
    # Return graph
    return ntx_graph


# Command Center
def command_center(input_file=None, delimiter=None, weighted=None):
    """
    This function controls rest of the functions
    :param input_file: Input file path
    :param delimiter: Optional separator for he column of the input file
    :param weighted: Simple yes/no if the input file is weighted or not
    :rtype: NULL
    """
    # Read edges
    ntx_graph = compose_graph(input_file, delimiter, weighted)
    print('Total nodes in Graph: {}'.format(len(ntx_graph.nodes())))
    print('Total edges in Graph: {}'.format(len(ntx_graph.edges())))


# Standard boilerplate for running this source code file as a standalone segment
if __name__ == '__main__':
    """
    Parse arguments and follow through to mission control
    """
    # Create parser
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument('-i', '--input-file', action='store', dest='input_file', required=True,
                        help='Input file absolute path. E.g. /home/user/data/input/file_name.txt/.csv/.dat etc.')
    parser.add_argument('-d', '--delimiter', action='store', dest='delimiter', required=False,
                        help='Separator for the input and output file. E.g. (,)/(";" need to be quoted)/tab/space.'
                             'Default is whitespace')
    parser.add_argument('-w', '--weighted', action='store', dest='weighted', required=False,
                        help='Boolean - yes/no if the file has weight column')

    args = parser.parse_args()
    # Double checking the arguments
    if args.delimiter:
        _delimiter = args.delimiter
    else:
        print('No delimiter provided! Using default (whitespace).....', log_type='info')
        _delimiter = None
    if args.weighted:
        _weighted = args.weighted
    else:
        print('No weighted parameter provided! Using default (No).....', log_type='info')
        _weighted = 'No'

    command_center(input_file=args.input_file, delimiter=_delimiter, weighted=_weighted)
