#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Import python libraries
import sys
import textwrap
import argparse
try:
    from pyrainbowterm import *
except ImportError:
    print('Can not import pyrainbowterm!', log_type='error')
    print('Try: pip install pyrainbowterm', log_type='hint')
    sys.exit(1)

# Import fast greedy community detection algorithm
from networkx.algorithms.community import modularity_max

# import graph_composer
import graph_composer

# Source code meta data
__author__ = 'Dalwar Hossain'
__email__ = 'dalwar.hossain@protonmail.com'


# Clauset-Newman-Moore community detection
# @profile
def fast_greedy_find_communities(ntx_graph):
    """
    This function detects community structures in a graph using Clauset-Newman-Moore algorithm
    :param ntx_graph: A graph created with networkx
    :return: Total number of community, a python dictionary with detected communities, modularity of the network
    """
    print('Finding communities with fast-greedy (Clauset-Newman-Moore) algorithm.....', log_type='info')
    communities = modularity_max.greedy_modularity_communities(ntx_graph, weight=None)

    # Return
    return communities


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
    ntx_graph = graph_composer.compose_ntx_graph(input_file, delimiter, weighted)
    # Detect communities
    fast_greedy_communities_list = fast_greedy_find_communities(ntx_graph)

    # Create a dictionary of detected communities
    fast_greedy_communities = {}
    community_id = 1
    for community in fast_greedy_communities_list:
        for node in community:
            fast_greedy_communities[node] = community_id
        community_id += 1

    print('Total communities found with fast greedy (CNM) algorithm: ', color='green', log_type='info', end='')
    print('{}'.format(len(fast_greedy_communities_list)), color='cyan', text_format='bold')


if __name__ == '__main__':
    """
    Parse arguments and follow through to mission control
    """
    # Create parser
    parser = argparse.ArgumentParser(prog='na_fast_greedy.py',
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
