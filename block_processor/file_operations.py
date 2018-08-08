#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Import python libraries
import os
import sys
import datetime
from itertools import islice

# Import custom python libraries
try:
    from pyrainbowterm import *
except ImportError:
    print('Can not import pyrainbowterm!', log_type='error')
    print('Try: pip install pyrainbowterm', log_type='hint')
    sys.exit(1)


# Source code meta data
__author__ = 'Dalwar Hossain'
__email__ = 'dalwar.hossain@protonmail.com'


# Check if the file has header or not
def file_sniffer(input_file=None):
    """
    This function checks if the first line of the file is a header or not
    :param input_file: Input file path
    :return: detected delimiter, headers (if available), number of columns, skip rows
    """
    try:
        import csv
    except ImportError:
        print('Can not import python csv library!', log_type='error')
        sys.exit(1)

    # Open the file and take a sniff
    with open(input_file) as f:
        first_five_lines = list(islice(f, 5))
        file_head = ''.join(map(str, first_five_lines))
        try:
            dialect = csv.Sniffer().sniff(file_head)
            _headers = csv.Sniffer().has_header(file_head)
            delimiter = dialect.delimiter
        except Exception as e:
            print('Can not detect delimiter or headers! ERROR: {}'.format(e), log_type='error')
            print('Please check input file!!', log_type='error')
        # Sniff into the file and see if there is a header or not
        if _headers:
            headers = file_head.split('\n')[0].split(delimiter)
            n_cols = len(headers)
            skip_rows = 1
        else:
            headers = None
            n_cols = len(file_head.split('\n')[0].split(delimiter))
            skip_rows = 0

    # Return
    return delimiter, headers, n_cols, skip_rows


# Check File Header
def check_file_header(headers=None):
    """
    This file checks if the file header is active or commented
    Limitation: Checks only First line of the file
    --------------------------------------
    =================
    == Attention!! ==
    =================
    File with header => 0
    File without/commented header=> 1
    --------------------------------------
    :param headers: File headers with column names
    :return: <>
    """
    if headers:
        print('Headers detected!', log_type='warn')
        if headers[0].startswith('#'):
            print('Found commented header!', log_type='info')
            header_status = 1
        else:
            header_status = 0
            print('Please comment [#] or delete header!', log_type='warn')
    else:
        print('No headers detected!', log_type='info')
        header_status = 1

    # Return header status
    return header_status


# Check Delimiter
def check_delimiter(detected_delimiter=None, provided_delimiter=None):
    """
    This function checks match between provided and detected delimiter
    ----------------------------------------------------------
    =================
    == Attention!! ==
    =================
    detected delimiter and provided delimiter - match => 1
    detected delimiter and provided delimiter - mismatch => 2
    -----------------------------------------------------------
    :param detected_delimiter: Delimiter that is detected from the input file
    :param provided_delimiter: Delimiter that was provided
    :return: <>
    """
    print('Provided delimiter: "{}"'.format(provided_delimiter), log_type='info')
    print('Detected delimiter: "{}"'.format(detected_delimiter), log_type='info')

    if detected_delimiter != provided_delimiter:
        delimiter_status = 2
        print('Delimiter mismatch!', log_type='warn', color='orange')
    elif detected_delimiter == provided_delimiter:
        delimiter_status = 1

    # Return
    return delimiter_status


# Check Columns
def check_columns(n_cols=None, weighted=None):
    """
    This function checks the number of columns detected from the input file
    also checks that it matches with the weighted argument. For example:
    A normal unweighted graph will have two column and weighted graph will have
    three columns.
    ------------------------------------
    =================
    == Attention!! ==
    =================
    If weighted and column == 3 =>1
    else => 0
    If unweighted and column == 2 => 1
    else => 0
    -------------------------------------
    :param n_cols: Number of columns detected from the input file
    :param weighted: Is the weighted argument provided yes or no
    :return: <>
    """
    # Check the number of columns in the file
    print('Detected columns: {}'.format(n_cols), log_type='info')
    weight_col = is_weighted(weighted)
    if weight_col:
        if n_cols == 3:
            column_status = 1
        else:
            column_status = 0
    else:
        if n_cols == 2:
            column_status = 1
        else:
            column_status = 0

    # Return
    return column_status


# Get data value for networkx graph (data = True) in read_edgelist()
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


# Generate appropriate sanity check status code
def generate_sanity_status(header_status=None, delimiter_status=None, column_status=None):
    """
    This function creates sanity check status codes
    :param header_status:
    :param delimiter_status:
    :param column_status:
    :return: status
    """
    status_code = 1
    print('Sanity check.....', log_type='info', end='')
    print('COMPLETE', color='green')
    print('--------------- Summary -------------------')

    # Header
    print('Headers.....', log_type='info', end='')
    if header_status == 1:
        print('OK', color='green')
        status_code = status_code and 1
    elif header_status == 0:
        print('NOT OK', color='red')
        status_code = status_code and 0

    # Delimiter
    print('Delimiter.....', log_type='info', end='')
    if delimiter_status == 1:
        print('OK', color='green')
        status_code = status_code and 1
    elif delimiter_status == 2:
        print('[!] OK', color='orange')
        print('Program might not detect nodes if input file does not have default (whitespace) delimiter',
              log_type='warn', color='orange')
        status_code = status_code and 1

    # Columns
    print('Columns.....', log_type='info', end='')
    if column_status == 1:
        print('OK', color='green')
        status_code = status_code and 1
    elif column_status == 0:
        print('NOT OK', color='red')
        status_code = status_code and 0

    print('-------------------------------------------')

    # Return
    return status_code


# Sanity Check for file operations
def sanity_check(input_file=None, delimiter=None, weighted=None):
    """
    This function checks the sanity of the input and returns a status with file is weighted or not
    :param input_file: Input file full path
    :param delimiter: Column separator in the input file
    :param weighted: Does the file contain edge weights or not
    :return: sanity status
    """
    # Get file information (Header, delimiter, number of columns etc.)
    detected_delimiter, headers, n_cols, skip_n_rows = file_sniffer(input_file)

    # Header?
    header_status = check_file_header(headers)

    # Delimiter?
    delimiter_status = check_delimiter(detected_delimiter, delimiter)

    # Number of columns?
    column_status = check_columns(n_cols, weighted)

    # Generate sanity status
    sanity_status = generate_sanity_status(header_status, delimiter_status, column_status)

    # Return
    return sanity_status


# Create initial message
def initial_message(script=None, algorithm=None):
    """
    This function creates initial message
    :param script: name of the script that will show the message
    :param algorithm: name of the algorithm of that particular script
    :return: <>
    """
    # Print a general help message
    date_time = datetime.datetime.now()
    print_string = "Network analysis and community detection with " + algorithm
    print_string += " [ " + date_time.strftime("%d-%B-%Y %H:%M:%S") + " ]"
    print('=' * len(print_string), print_string, "Need help?: python {} -h/--help".format(script),
          '=' * len(print_string), sep='\n')


# Get directory path for input/output data
def get_dir_path(input_file=None):
    """
    This function extracts the directory path of input file and creates a new file name for the output file
    :param input_file: A complete file path for input dataset
    :return: A directory path and a file name
    """
    # Get input file's directory
    input_dir = os.path.dirname(input_file)
    if os.path.isdir(input_dir):
        output_dir = input_dir
    else:
        print('Can not determine output directory!', log_type='error')
        sys.exit(1)

    # Return output path
    return output_dir


# Generate output file name
def generate_output_filename(input_file=None, prefix=None):
    """
    This function generates appropriate output file name
    :param input_file: A file path to input file
    :param prefix: Prefix of output file
    :return: output filename full path
    """
    splitter = '_'
    # Get file name
    input_file_name = os.path.basename(input_file)
    # Create new file name
    base_file_name, base_file_extension = os.path.splitext(input_file_name)
    output_file_name = prefix + splitter + base_file_name + base_file_extension

    # Get output directory
    output_directory = get_dir_path(input_file)

    # Output file full path
    output_file = os.path.join(output_directory, output_file_name)

    # Return
    return output_file


# Create a community file as output file
def create_community_file(dict_communities=None, output_file=None):
    """
    This function creates the output file
    :param dict_communities: A python dictionary with communities assigned to nodes
    :param output_file: name and location of the output files (.grp) and (.pkl)
    :return: <> file object <>
    """
    # Create pickled extension for saving data for further use
    pickled_file = output_file.rsplit('.', 1)[0] + '.pkl'

    # Create community extension for saving communities
    community_file = output_file.rsplit('.', 1)[0] + '.grp'

    # Put the dictionary data in a pickled jar for later use
    if sys.version_info[0] == 2:
        import cPickle as pickle
    if sys.version_info[0] == 3:
        import pickle

    try:
        print('Creating pickled jar of (.pkl) data.....', log_type='info')
        with open(pickled_file, 'w') as pickled_file:
            pickle.dump(dict_communities, pickled_file)
    except Exception as e:
        print('Can not create pickled data!!! ERROR: {}'.format(e), log_type='error')

    # import json
    #
    # communities = json.dumps(dict_communities, sort_keys=True, indent=4)
    #
    # print('Creating community file.....', log_type='info')
    # with open(output_file, 'w') as f:
    #     f.write(communities)

    # Import pandas
    try:
        import pandas as pd
    except ImportError as e:
        print('Can not import python pandas library! ERROR: {}'.format(e), log_type='error')
        sys.exit(1)

    # Create a pandas data frame from the dictionary
    communities = pd.DataFrame(dict_communities.items(), columns=['node', 'cluster'], dtype=int)

    # Generate list of nodes that belongs to same community
    groups = communities.groupby('cluster')['node'].apply(list)

    # Write to output file
    try:
        print('Creating community (.grp) file.....', log_type='info')
        groups.to_csv(community_file, header=False)
    except Exception as e:
        print('Can not create output file! ERROR: {}'.format(e), log_type='error')
        sys.exit(1)
