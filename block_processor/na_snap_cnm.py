#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Import python libraries
import os
import sys
import textwrap
import argparse
try:
    from pyrainbowterm import *
except ImportError:
    print('Can not import pyrainbowterm!', log_type='error')
    print('Try: pip install pyrainbowterm', log_type='hint')
    sys.exit(1)

# Import snap (Stanford SNAP python program for network analysis)
from sanppy import snap

# import graph_composer
import graph_composer

# Import file_operations
import file_operations

# Source code meta data
__author__ = 'Dalwar Hossain'
__email__ = 'dalwar.hossain@protonmail.com'


# Run Clauset-Newman-Moore algorithm
# @profile  # Uncomment to profile this function for memory usage with 'mprof'
def run_cnm(snap_graph, community_vector):
    """
    This functions will run CNM algorithm
    :param snap_graph: A snap created graph of input file
    :param community_vector: Detected communities
    :return: modularity of the network and community vector
    """
    modularity = snap.CommunityCNM(snap_graph, community_vector)

    # Return
    return modularity, community_vector


# Clauset-Newman-Moore community detection
# @profile  # Uncomment to profile this function for memory usage with 'mprof'
def cnm_find_communities(snap_graph):
    """
    This function detects community structures in a graph using Clauset-Newman-Moore algorithm
    :param snap_graph: A graph created with SNAP's snap.py module
    :return: Total number of community, a python dictionary with detected communities, modularity of the network
    """
    print('Finding communities with CNM.....', log_type='info')
    community_vector = snap.TCnComV()
    modularity, community_vector = run_cnm(snap_graph, community_vector)
    total_communities = len(community_vector)
    # Create python dictionary of communities
    community_id = 0
    cnm_communities = {}
    for community in community_vector:
        for NI in community:
            cnm_communities[NI] = community_id
        community_id += 1

    # Return
    return total_communities, cnm_communities, modularity


# Command Center
def command_center(input_file=None, delimiter=None, weighted=None):
    """
    This function controls the other functions
    :param input_file: Input file with edges of the graph
    :param delimiter: Field separator
    :param weighted: are the edges weighted?
    :return: <>
    """
    print('Initializing.....', log_type='info')
    # Create SNAP graph
    snap_graph = graph_composer.compose_snap_graph(input_file, delimiter, weighted)
    # Detect communities
    total_communities, cnm_communities, modularity = cnm_find_communities(snap_graph)

    print('Total communities found with CNM algorithm: ', color='green', log_type='info', end='')
    print('{}'.format(total_communities), color='cyan', text_format='bold')


if __name__ == '__main__':
    """
    Parse arguments and follow through to mission control
    """
    # Initial message
    file_operations.initial_message(os.path.basename(__file__), '(SNAP) Clauset-Newman-Moore algorithm')

    # Create parser
    parser = argparse.ArgumentParser(prog='na_cnm.py',
                                     usage='python %(prog)s <input_file> <options>',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent('''\
                                         This program uses Clauset-Newman-Moore(CNM) algorithm to detect communities in
                                         large-scale networks.
                                         For more please visit: https://github.com/taynaud/python-louvain
                                         '''),
                                     epilog='',
                                     add_help=True)

    parser.add_argument('-i', '--input-file', action='store', dest='input', required=True,
                        help='Input file absolute path. E.g. /home/user/data/input/file_name.txt/.csv/.dat etc.')
    parser.add_argument('-d', '--delimiter', action='store', dest='delimiter', required=False,
                        help='Separator for the input and output file. E.g. (,)/(";" need to be quoted)/tab/space.'
                             'Default is comma (,)')
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

    # Command Center
    command_center(input_file=args.input, delimiter=_delimiter, weighted=_weighted)
