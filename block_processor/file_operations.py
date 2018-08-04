#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Import python libraries
import sys
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
