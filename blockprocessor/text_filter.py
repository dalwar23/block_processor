#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Import python libraries
import os
import sys
import argparse
import subprocess
try:
    from pyrainbowterm import *
except ImportError:
    print('Can not import pyrainbowterm!', log_type='error')
    print('Try: pip install pyrainbowterm', log_type='hint')
    sys.exit(1)


# Create awk command
def create_command(input_file, columns_to_use, column_separator, output_file):
    """
    This function creates the linux command to filter the columns and creating the output file
    :param input_file: A valid file path to raw data file
    :param columns_to_use: Indexes of the columns that needs to be filtered out (index starts from 1)
    :param column_separator: Column separator in input/output file (default is ',' [comma])
    :param output_file: A valid file path where the output will be stored
    :return: A linux shell command
    """
    print('Creating text filter command.....', log_type='info')
    prefix, command_segment = ('$', '')
    count = 1
    index_length = len(columns_to_use)
    for item in columns_to_use:
        if count < index_length:
            segment = prefix + item + '","'
            command_segment += segment
            count += 1
        else:
            segment = prefix + item
            command_segment += segment
    if column_separator is None:
        delimiter = ''
    else:
        delimiter = ' -F "' + column_separator + '"'
    command = "awk" + delimiter + " '{print " + command_segment + "}' " + input_file + " > " + output_file

    # Return command
    # print(command)
    return command


# Create output file with filtered data from input file
def create_output_file(command):
    """
    This function uses python subprocess module to read input file, filter with AWK and store data in a output file
    :param command: A linux AWK command
    :return: Data stored in output file
    """
    print('Reading input file.....', log_type='info')
    try:
        print('Creating output file.....', log_type='info')
        subprocess.check_output(command, shell=True, universal_newlines=True).strip()
        print('Output file creation complete!', color='green', log_type='info')
    except Exception as e:
        print('Output file creation error. ERROR: {}'.format(e), color='red', log_type='error')
        sys.exit(1)


# Sanity check
def sanity_check(input_file, column_indexes, column_separator, output_file):
    """
    This function verifies input(s)
    :param input_file: A file path to raw data file
    :param column_indexes: Indexes of the columns that needs to be filtered out (index starts from 1)
    :param column_separator: Column separator in input/output file (default is ',' [comma])
    :param output_file: A file path where the output will be stored
    :return: input_file, python list of column(s), column_separator, output_file
    """
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

    # Check column indexes (is numeric?)
    print('Checking column indexes.....', log_type='info')
    try:
        columns_to_use = column_indexes.split(',')
    except Exception as e:
        print('-c/--columns argument does not match input criteria! ERROR: {}'.format(e), log_type='error')
        print('Try -c 1,4,6,3 or --columns 1,4,6,3 [Index starts from 1, separated by comma (,)]', log_type='hint')
        sys.exit(1)

    # Check column separator
    if column_separator is None:
        # column_separator = ','
        print('No column separator detected! Using default value.', log_type='warn')
        # print('Column separator: {}'.format(column_separator), log_type='info')

    # Check output file
    print('Checking output file.....', log_type='info')
    if os.access(output_file, os.F_OK):
        print("Output file already exists! Removing old file.....", log_type='warn')
        os.remove(output_file)
    else:
        print('Output file does not exists yet! It will be created!', log_type='warn')

    # Return checked values
    return input_file, columns_to_use, column_separator, output_file


# Command Center
def command_center(input_file=None, column_indexes=None, separator=",", output_file=None):
    """
    This function controls rest of the functions
    :param input_file: A file path to raw data file
    :param column_indexes: Indexes of the columns that needs to be filtered out (index starts from 1)
    :param separator: Column separator in input/output file (default is ',' [comma])
    :param output_file: A file path where the output will be stored
    :return: NULL
    """
    print('Initializing.....', color='green', log_type='info')
    input_file, columns_to_use, column_separator, output_file = sanity_check(input_file, column_indexes, separator,
                                                                             output_file)
    print('Sanity check complete!', color='green', log_type='info')

    command = create_command(input_file, columns_to_use, column_separator, output_file)
    print('Command creation complete!', color='green', log_type='info')

    create_output_file(command)


# Standard boilerplate for running this source code file as a standalone segment
if __name__ == "__main__":
    """
    Parse given arguments and follow through to mission control
    """
    # Create parser
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument('-i', '--input-file', action='store', dest='input_file', required=True,
                        help='Input file absolute path. E.g. /home/user/data/input/file_name.txt/.csv/.dat etc.')
    parser.add_argument('-c', '--columns', action='store', dest='columns', required=True,
                        help='Index of the columns (comma separated, index starting from 1) E.g. 1,4,2,5.')
    parser.add_argument('-s', '--separator', action='store', dest='separator', required=False,
                        help='Separator for the input and output file. E.g. (,)/(";" need to be quoted)/tab/space.'
                             'Default is comma (,)')
    parser.add_argument('-o', '--output-file', action='store', dest='output_file', required=True,
                        help='Output file absolute path. E.g. /home/user/data/output/file_name.txt/.csv/.dat etc.')

    args = parser.parse_args()
    command_center(input_file=args.input_file, column_indexes=args.columns, separator=args.separator,
                    output_file=args.output_file)
