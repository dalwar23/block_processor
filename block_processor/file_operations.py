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
def check_header(input_file):
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
        dialect = csv.Sniffer().sniff(file_head)
        delimiter = dialect.delimiter
        # Sniff into the file and see if there is a header or not
        _headers = csv.Sniffer().has_header(file_head)
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
