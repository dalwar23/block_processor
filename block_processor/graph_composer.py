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

# Import snap (Stanford SNAP python program for network analysis)
from sanppy import snap

# Source code meta data
__author__ = 'Dalwar Hossain'
__email__ = 'dalwar.hossain@protonmail.com'


# Compose graph with stanford SNAP python snap.py
# @profile  # Uncomment to profile this function for memory usage with 'mprof'
def compose_snap_graph(input_file=None, delimiter=None, weighted=None):
    """
    This function creates a snap graph from provided file
    :param input_file:  Input file path
    :param delimiter: Column separator in the file
    :param weighted: Simple yes/no if the input file is weighted or not
    :return: snap graph
    """
    # Check sanity status of input
    sanity_status = file_operations.sanity_check(input_file, delimiter, weighted)

    # Create a snap graph
    if sanity_status == 1:
        if delimiter is None:
            delimiter = ' '  # Using default (whitespace) delimiter
        # Load edges list from input file
        print('Creating SNAP graph.....', log_type='info')
        # snap.LoadEdgeList(snap.PUNGraph = snap graph type, input file, source column, destination column, delimiter)
        snap_graph = snap.LoadEdgeList(snap.PUNGraph, input_file, 0, 1, delimiter)
        # print('Trying to delete self edges.....', log_type='info')
        # Making sure there are no self-edges
        # snap_graph = snap.DelSelfEdges(snap_graph)

        # Return
        return snap_graph
    else:
        print('Sanity check failed!', log_type='error', color='red')
        sys.exit(1)


# Compose graph with networkx library
@profile  # Uncomment to profile this function for memory usage with 'mprof'
def compose_ntx_graph(input_file=None, delimiter=None, weighted=None):
    """
    This function creates a networkx graph from provided file
    :param input_file: Input file path
    :param delimiter: separator for the column of the input file
    :param weighted: Simple yes/no if the input file is weighted or not
    :return: networkx graph
    """
    # Check sanity status of input
    sanity_status = file_operations.sanity_check(input_file, delimiter, weighted)

    # Get data for weighted networkx graph
    file_is_weighted = file_operations.is_weighted(weighted)

    # Create a networkx graph from the edgelist
    if sanity_status == 1:
        if file_is_weighted:
            print('Creating Networkx weighted graph.....', log_type='info')
            try:
                ntx_graph = nx.read_weighted_edgelist(input_file, delimiter=delimiter, nodetype=int)
            except Exception as e:
                print('Can not create weighted networkx graph. ERROR: {}'.format(e), color='red', log_type='error')
                sys.exit(1)
        else:
            print('Creating Networkx unweighted graph.....', log_type='info')
            try:
                ntx_graph = nx.read_edgelist(input_file, delimiter=delimiter, nodetype=int)
            except Exception as e:
                print('Can not create unweighted networkx graph. ERROR: {}'.format(e), color='red', log_type='error')
                sys.exit(1)

        # Return graph
        return ntx_graph
    else:
        print('Sanity check failed!', log_type='error', color='red')
        sys.exit(1)


# Command Center
def command_center(input_file=None, delimiter=None, weighted=None):
    """
    This function controls rest of the functions
    :param input_file: Input file path
    :param delimiter: Optional separator for he column of the input file
    :param weighted: Simple yes/no if the input file is weighted or not
    :rtype: NULL
    """
    print('Initializing.....', log_type='info')
    # Read edges
    ntx_graph = compose_ntx_graph(input_file, delimiter, weighted)
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

    # Parse arguments
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
