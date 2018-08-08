#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Import python libraries
import os
import sys
import textwrap
import argparse
import time
import datetime
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

# Import file_operations
import file_operations

# Source code meta data
__author__ = 'Dalwar Hossain'
__email__ = 'dalwar.hossain@protonmail.com'


# Find communities
@profile  # Uncomment to profile this function for memory usage with 'mprof'
def louvain_find_communities(ntx_graph):
    """
    This function finds communities in a graph using louvain community detection algorithm
    :param ntx_graph: A networkx graph
    :return: A python dictionary of detected communities
    """
    print('Finding communities with louvain method.....', log_type='info')
    try:
        start_time = time.time()
        print('Louvain method started at: {}'.format(datetime.datetime.now().strftime("%H:%M:%S")), log_type='info')
        louvain_communities = community.best_partition(ntx_graph)
        end_time = time.time() - start_time
        print('Elapsed time: ', log_type='info', end='')
        print('{}'.format(time.strftime("%H:%M:%S", time.gmtime(end_time))), color='cyan', text_format='bold')
    except Exception as e:
        print('Can not detect communities with louvain method! ERROR: {}'.format(e))
        sys.exit(1)

    # Return
    return louvain_communities


# Create a function to run louvain method algorithm
def run_louvain(input_file=None, delimiter=None, weighted=None, output=None):
    """
    This function finds community structures in graphs using louvain method
    :param input_file: Input file path
    :param delimiter: Column separator
    :param weighted: Is the file has a weight column? (yes/no)
    :param output: Boolean, yes/no if the output file will be created or not
    :param output: yes/no, output will be created at the same directory
    :return: file object/stdIO
    """
    # Create a graph from dataset
    ntx_graph = graph_composer.compose_ntx_graph(input_file, delimiter, weighted)

    # Find Communities from the graph
    louvain_communities = louvain_find_communities(ntx_graph)

    # Create output files (.grp and .pkl)
    if output is None or output == 'Yes' or output == 'Y' or output == 'y' or output == 'yes':
        output_file = file_operations.generate_output_filename(input_file, prefix='Louvain')
        file_operations.create_community_file(louvain_communities, output_file)
    else:
        pass

    # Print information about detected communities
    total_communities = len(list(set(louvain_communities.values())))
    print('Total communities found with LOUVAIN method algorithm: ', color='green', log_type='info', end='')
    print('{}'.format(total_communities), color='cyan', text_format='bold')


# Command Center
def command_center(input_file=None, delimiter=None, weighted=None, output=None):
    """
    This function controls the other functions
    :param input_file: Input file path
    :param delimiter: Column separator
    :param weighted: Is the file has a weight column? (yes/no)
    :param output: Boolean, yes/no if the output file will be created or not
    :return: <>
    """
    print('Initializing.....', log_type='info')
    run_louvain(input_file, delimiter, weighted, output)


# Standard boilerplate for running this source code file as a standalone segment
if __name__ == '__main__':
    """
    Parse arguments and follow through to mission control
    """
    # Initial message
    file_operations.initial_message(os.path.basename(__file__), 'Louvain method')

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
    parser.add_argument('-o', '--output', action='store', dest='output', required=False,
                        help='Boolean - yes/no (To create output file or not)')

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
    if args.output:
        _output = args.output
    else:
        print('No output parameter provided! Using default (Yes).....', log_type='info')
        _output = 'Yes'

    # Command Center
    command_center(input_file=args.input, delimiter=_delimiter, weighted=_weighted, output=_output)
