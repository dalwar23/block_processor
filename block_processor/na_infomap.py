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


# Find communities
def find_communities(graph, _options):
    """
    Partition network with the Infomap algorithm.
    Annotates nodes with 'community' id and return number of communities found.
    :param graph: A networkx graph created using "networkx.Graph"
    :param _options: Options for infomap
    :rtype: Total number of communities
    """
    options = '--two-level'
    infomap_wrapper = infomap.Infomap(options)

    print("Building Infomap network from a NetworkX graph.....", log_type='info')
    for e in graph.edges():
        infomap_wrapper.addLink(*e)

    print("Finding communities with Infomap.....", log_type='info')
    infomap_wrapper.run()
    # Create tree from infomap_wrapper
    tree = infomap_wrapper.tree
    print("Found {} modules with code length: {}".format(tree.numTopModules(), tree.codelength()), log_type='info')

    # Find communities
    communities = {}
    for node in tree.leafIter():
        communities[node.originalLeafIndex] = node.moduleIndex()

    nx.set_node_attributes(graph, name='community', values=communities)
    # return number of modules found
    return tree.numTopModules(), communities


# Command Center
def command_center(input_file=None, delimiter=None, weighted=None, options=None, dest=None):
    # Create a graph from dataset
    ntx_graph = graph_composer.compose_graph(input_file, delimiter, weighted)
    # Find Communities from the graph
    # total_communities, communities = find_communities(ntx_graph, options)
    # print('Total communities found with INFOMAP algorithm: ', color='green', log_type='info', end='')
    # print('{}'.format(total_communities), color='cyan', text_format='bold')


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

    parser.add_argument('--input-file', action='store', dest='input', required=True,
                        help='Input file absolute path. E.g. /home/user/data/input/file_name.txt/.csv/.dat etc.')
    parser.add_argument('--delimiter', action='store', dest='delimiter', required=True,
                        help='Separator for the input and output file. E.g. (,)/(";" need to be quoted)/tab/space.'
                             'Default is comma (,)')
    parser.add_argument('--weighted', action='store', dest='weighted', required=True,
                        help='Boolean - yes/no if the file has weight column')
    parser.add_argument('--options', action='store', dest='options', required=True,
                        help='Options for the Infomap algorithm (in a quoted string [no spaces])')
    parser.add_argument('--output-file', action='store', dest='destination', required=True,
                        help='Output file destination')

    args = parser.parse_args()
    command_center(input_file=args.input, delimiter=args.delimiter, weighted=args.weighted, options=args.options,
                   dest=args.destination)
