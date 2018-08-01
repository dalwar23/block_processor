#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Import python libraries
import sys
import os
import argparse
import pandas as pd
import math
import time
import datetime
try:
    from pyrainbowterm import *
except ImportError:
    print('Can not import pyrainbowterm!', log_type='error')
    print('Try: pip install pyrainbowterm', log_type='hint')
    sys.exit(1)


# Source code meta data
__author__ = 'Dalwar Hossain'
__email__ = 'dalwar.hossain@protonmail.com'


# Numeric mapping of the entire data
def numeric_mapping(data_frame, mapping_dict):
    """
    This function maps every string values into a numeric values in pandas data frame
    :param data_frame: Python pandas data frame
    :param mapping_dict: Python dictionary with str -> number(int/long) mapping
    :return: Python pandas data frame
    """
    # Map source and target row according to mapping dictionary
    print('Mapping data frame.....', log_type='info')
    data_frame['source'] = data_frame['source'].map(mapping_dict)
    data_frame['target'] = data_frame['target'].map(mapping_dict)

    # Return mapped data frame
    return data_frame


# Create output file
def create_output_file(numeric_data_frame, output_dir_path, output_file_name):
    """
    This function creates a file from python pandas data frame
    :param numeric_data_frame: Python pandas data frame
    :param output_dir_path: A directory path
    :param output_file_name: A file name with extension
    :return: NULL
    """
    # Create numeric output file
    output_file = os.path.join(output_dir_path, output_file_name)
    print('Creating numerically mapped output file.....', log_type='info')
    try:
        numeric_data_frame.to_csv(output_file, index=False, header=False)
        print('Output file creation complete!', color='green', log_type='info')
    except Exception as e:
        print('Can not write output file. ERROR: {}'.format(e), log_type='error')
        sys.exit(1)


# Extract unique nodes/values for mapping
def extract_nodes(data_frame):
    """
    This function extracts unique values from a python pandas data frame given that first two columns have headers
    'source' and 'target'
    :param data_frame: Python pandas data frame
    :return: Python dictionary with unique values mapped to an integer
    """
    # Find unique values to create a look up table
    # Returns a numpy array
    print('Extracting unique values/nodes.....', log_type='info')
    unique_values = pd.unique(data_frame[['source', 'target']].values.ravel('K'))

    # Create a PANDAS data frame out of numpy array with unique nodes
    print('Converting values into pandas data frame.....', log_type='info')
    lookup_data = pd.DataFrame(unique_values, columns=['label'])
    lookup_data['id'] = lookup_data.index
    print('Total detected nodes/values: ', log_type='info', end='')
    print('{}'.format(len(lookup_data.index)), color='cyan', text_format='bold')

    # Create a mapping dictionary for the node labels
    print('Creating mapping table.....', log_type='info')
    mapping_dict = dict(zip(lookup_data.label, lookup_data.id))

    # Return mapping dictionary
    return mapping_dict


# Clean and convert weights into normalized form (rounded up to 6 decimal point)
def clean_convert_weight(x):
    """
    This function strips any white space and new lines. It also converts the value to a numpy 64 bit integer.
    Also normalizes big and small values using natural logarithm and rounding them up to 6 decimal points.
    :param x: Any number variable that can be converted into int/float/long/double
    :return: Natural logarithm of input value
    """
    x = x.replace(' ', '').replace('\n', '')
    x = int(x)
    log_x = round(math.log(1 + x), 6)
    return log_x


# Load input file in to pandas data frame
def load_file(input_dataset, column_separator, headers):
    """
    This function reads a text file and loads it into python pandas data frame
    :param input_dataset: A file path that contains row x column wise text data
    :param column_separator: A value that separates the columns in the input dataset
    :param headers: Names of the columns from input dataset
    :return: Python pandas data frame
    """
    if len(headers) == 3:
        convert_dict = {'weight': clean_convert_weight}
    else:
        convert_dict = {}

    # Load input file
    print('Loading input dataset.....', log_type='info')
    try:
        data_frame = pd.read_csv(input_dataset, delimiter=column_separator, names=headers, skipinitialspace=True,
                                 converters=convert_dict)
        print('Input dataset loaded successfully!', color='green', log_type='info')
    except Exception as e:
        print('Can not load input dataset. ERROR: {}'.format(e), color='red', log_type='error')
        sys.exit(1)

    # Drop rows that contains NaN/Blank column values
    print('Removing empty target/destination(s).....', log_type='info')
    data_frame = data_frame.dropna()

    # Filter out source and target column for values with valid length
    print('Cleaning data.....', log_type='info')
    data_frame = data_frame[~data_frame[['source', 'target']].applymap(lambda x: len(str(x)) < 34).any(axis=1)]

    # Reset index of the data frame
    print('Resetting data frame index.....', log_type='info')
    data_frame = data_frame.reset_index(drop=True)

    # Return pandas data frame
    return data_frame


# Sanity check
def sanity_check(input_file, weighted):
    """
    This function check input arguments and properties of input file
    :param input_file: A file path, Input file's full path
    :param weighted: Determines whether input data has a column that represents the weights of source -> target
    :return: A python list of headers for the input file's dataset
    """
    # Assign headers based on weighted or not
    if weighted == "yes" or weighted == "Yes" or weighted == "Y" or weighted == "y":
        headers = ['source', 'target', 'weight']
    elif weighted == "no" or weighted == "No" or weighted == "N" or weighted == "n":
        headers = ['source', 'target']
    else:
        print('Please provide weighted (-w) argument with yes/no, y/n, Yes/No', log_type='error')
        sys.exit(1)

    # Check input file's status (is a file?, has right permissions?)
    print('Checking input file status.....', log_type='info')
    if os.access(input_file, os.F_OK):
        print('Input file found!', log_type='info')
        if os.access(input_file, os.R_OK):
            print('Input file has read permission!', log_type='info')
        else:
            print('Input file does not has read permission!', log_type='error')
            sys.exit(1)
    else:
        print('Input file not found!', log_type='error')
        sys.exit(1)

    # Return headers
    return headers


# Get directory path for input/output data
def get_dir_path(input_file):
    """
    This function extracts the directory path of input file and creates a new file name for the output file
    :param input_file: A complete file path for input dataset
    :return: A directory path and a file name
    """
    # Get file name
    input_file_name = os.path.basename(input_file)
    # Create new file name
    base_file_name, base_file_extension = os.path.splitext(input_file_name)
    output_file_name = base_file_name + '_numeric' + base_file_extension

    # Get input file's directory
    input_dir = os.path.dirname(input_file)
    if os.path.isdir(input_dir):
        output_dir = input_dir
    else:
        print('Can not determine output directory!', log_type='error')
        sys.exit(1)

    # Return output path
    return output_dir, output_file_name


# Command Center
def command_center(input_file=None, separator=',', weighted=None):
    """
    This function controls rest of the functions
    :param input_file: Input file path
    :param separator: Optional separator for he column of the input file
    :param weighted: Simple yes/no if the input file is weighted or not
    :rtype: NULL
    """
    print('Initializing.....', color='green', log_type='info')
    headers = sanity_check(input_file, weighted)
    print('Sanity check complete!', color='green', log_type='info')

    output_dir_path, output_file_name = get_dir_path(input_file)
    data_frame = load_file(input_file, separator, headers)
    print('Data cleanup complete!', color='green', log_type='info')

    mapping_dict = extract_nodes(data_frame)
    print('Numeric mapping reference creation complete!', color='green', log_type='info')

    start_time = time.time()
    print('Numeric mapping started at: {}' .format(datetime.datetime.now().strftime("%H:%M:%S")), log_type='info')
    numeric_data_frame = numeric_mapping(data_frame, mapping_dict)
    mapping_end_time = time.time() - start_time
    print('Elapsed time for mapping: ', log_type='info', end='')
    print('{}'.format(time.strftime("%H:%M:%S", time.gmtime(mapping_end_time))), color='cyan', text_format='bold')
    print('Numeric mapping complete!', color='green', log_type='info')

    create_output_file(numeric_data_frame, output_dir_path, output_file_name)


# Standard boilerplate for running this source code file as a standalone segment
if __name__ == '__main__':
    """
    Parse arguments and follow through to mission control
    """
    # Create parser
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument('-i', '--input-file', action='store', dest='input_file', required=True,
                        help='Input file absolute path. E.g. /home/user/data/input/file_name.txt/.csv/.dat etc.')
    parser.add_argument('-s', '--separator', action='store', dest='separator', required=False,
                        help='Separator for the input and output file. E.g. (,)/(";" need to be quoted)/tab/space.'
                             'Default is comma (,)')
    parser.add_argument('-w', '--weighted', action='store', dest='weighted', required=True,
                        help='Boolean - yes/no if the file has weight column')

    # Parse arguments
    args = parser.parse_args()

    command_center(input_file=args.input_file, separator=args.separator, weighted=args.weighted)
