#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Import python libraries
import sys
import textwrap
import argparse
# Import custom python library
import networkx as nx
try:
    from pyrainbowterm import *
except ImportError:
    print('Can not import pyrainbowterm!', log_type='error')
    print('Try: pip install pyrainbowterm', log_type='hint')
    sys.exit(1)

# Import infomap library
from infomap import infomap

# Import graph_composer
import graph_composer

# Source code meta data
__author__ = 'Dalwar Hossain'
__email__ = 'dalwar.hossain@protonmail.com'


# Run Infomap algorithm
@profile
def run_infomap(infomap_wrapper):
    print("Finding communities with Infomap.....", log_type='info')
    infomap_wrapper.run()
    # Create tree from infomap_wrapper
    tree = infomap_wrapper.tree
    print("Found {} modules with code length: {}".format(tree.numTopModules(), tree.codelength()), log_type='info')

    # Return
    return tree


# Find communities
@profile
def infomap_find_communities(graph, n_trials):
    """
    Partition network with the Infomap algorithm.
    Annotates nodes with 'community' id and return number of communities found.
    :param graph: A networkx graph created using "networkx.Graph"
    :param n_trials: Number of trials options for infomap
    :rtype: Total number of communities, python dictionary of detected communities
    """
    options = '--two-level' + ' -N ' + n_trials
    print('Number of trials: {}'.format(n_trials), log_type='info')

    # Create Infomap wrapper
    infomap_wrapper = infomap.Infomap(options)

    print("Building Infomap network from a NetworkX graph.....", log_type='info')
    for e in graph.edges():
        infomap_wrapper.addLink(*e)

    tree = run_infomap(infomap_wrapper)

    # Find communities
    communities = {}
    for node in tree.leafIter():
        communities[node.originalLeafIndex] = node.moduleIndex()

    nx.set_node_attributes(graph, name='community', values=communities)

    # return number of modules found
    return tree.numTopModules(), communities


# Command Center
def command_center(input_file=None, delimiter=None, weighted=None, trials=None, dest=None):
    """
    This function controls the other functions
    :param input_file: Input file with edges of the graph
    :param delimiter: Field separator
    :param weighted: are the edges weighted?
    :param trials: number of trials/run to find out community
    :param dest: destination folder
    :return: NULL
    """
    # Create a graph from dataset
    ntx_graph = graph_composer.compose_ntx_graph(input_file, delimiter, weighted)
    # Find Communities from the graph
    total_communities, infomap_communities = infomap_find_communities(ntx_graph, trials)
    print('Total communities found with INFOMAP algorithm: ', color='green', log_type='info', end='')
    print('{}'.format(total_communities), color='cyan', text_format='bold')


# Standard boilerplate for running this source code file as a standalone segment
if __name__ == '__main__':
    """
    Parse arguments and follow through to mission control
    """
    # Create parser
    parser = argparse.ArgumentParser(prog='na_infomap.py',
                                     usage='python %(prog)s <input_file> <options>',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent('''\
                                     This program uses Infomap algorithm to detect communities in large-scale networks.
                                     For more please visit: http://www.mapequation.org
                                     To find out available <options> for this program please visit:
                                     http://www.mapequation.org/code.html#Options
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
    parser.add_argument('-t', '--trials', action='store', dest='trials', required=False,
                        help='Options for the Infomap algorithm (in a quoted string [no spaces])')
    parser.add_argument('-o', '--output-file', action='store', dest='destination', required=False,
                        help='Output file destination')

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
    if args.trials:
        n = args.trials
    else:
        print('No trials parameters passed! Using defaults (1).....', log_type='info')
        n = str(1)
    # Command Center
    command_center(input_file=args.input, delimiter=_delimiter, weighted=_weighted, trials=n, dest=args.destination)
