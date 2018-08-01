#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Import python libraries
import sys
import textwrap
import argparse
# Import custom libraries
try:
    from pyrainbowterm import *
except ImportError:
    print('Can not import pyrainbowterm!', log_type='error')
    print('Try: pip install pyrainbowterm', log_type='hint')
    sys.exit(1)

# Import python-louvain library
import community

# Import graph composer
import graph_composer

# Source code meta data
__author__ = 'Dalwar Hossain'
__email__ = 'dalwar.hossain@protonmail.com'


# Find communities
def louvain_find_communities(ntx_graph):
    """
    This function finds communities in a graph using louvain community detection algorithm
    :param ntx_graph: A networkx graph
    :return: A python dictionary of detected communities
    """
    print('Finding communities with louvain method.....', log_type='info')
    try:
        louvain_communities = community.best_partition(ntx_graph)
    except Exception as e:
        print('Can not detect communities with louvain method! ERROR: {}'.format(e))
        sys.exit(1)

    # Return
    return louvain_communities


# Command Center
def command_center(input_file=None, delimiter=None, weighted=None):
    # Create a graph from dataset
    ntx_graph = graph_composer.compose_ntx_graph(input_file, delimiter, weighted)
    # Find Communities from the graph
    louvain_communities = louvain_find_communities(ntx_graph)
    print(louvain_communities)
    total_communities = max(louvain_communities.values())
    print('Total communities found with LOUVAIN method algorithm: ', color='green', log_type='info', end='')
    print('{}'.format(total_communities), color='cyan', text_format='bold')


# Standard boilerplate for running this source code file as a standalone segment
if __name__ == '__main__':
    """
    Parse arguments and follow through to mission control
    """
    # Create parser
    parser = argparse.ArgumentParser(prog='na_louvain.py',
                                     usage='python %(prog)s <input_file> <options>',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent('''\
                                     This program uses Louvain method algorithm to detect communities in large-scale
                                     networks. For more please visit: https://github.com/taynaud/python-louvain
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
