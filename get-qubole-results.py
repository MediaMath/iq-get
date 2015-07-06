#!/usr/bin/env python
import qds_sdk
from qds_sdk.commands import *
from cStringIO import StringIO
import os
import sys
import csv
import logging
import argparse

def main(args):
    api_token = args.Token
    Qubole.configure(api_token=args.Token)
    query_id = args.Query_ID
    if args.delimiter:
        if args.delimiter == 't':
            extension = '.tsv'
        else:
            extension = '.txt'
        delimiter = args.delimiter
    else:
        extension = '.csv'
        delimiter = ','
    if args.output:
        out_file_name = args.output
    else:
        out_file_name = str(query_id) + extension
    try:
        hc = HiveCommand.find(query_id)
    except qds_sdk.exception.ResourceNotFound:
        sys.stderr.write("Invalid query ID.\n")
        sys.exit(-1)
    tmp_out_path = os.path.expanduser('~/Desktop/') + out_file_name + '.tmp'
    with open(tmp_out_path, 'w') as out:
        hc.get_results(fp=out, delim='\t')
    out_file_path = os.path.expanduser('~/Desktop/') + out_file_name
    if os.path.exists(out_file_path):
        sys.stdout.write("File %s already exists.  Do you want to overwrite it? y/n\t" % out_file_path)
        choice = raw_input().lower()
        if choice == 'y':
            pass
        else:
            file_extension = out_file_path.split('.')[-1]
            out_file_path = out_file_path.split('.')[0] + '(1).' + file_extension
            out_file_name = out_file_name.split('.')[0] + '(1).' + file_extension
    else:
        pass
    with open(tmp_out_path) as result_txt, open(out_file_path, 'w+') as out_file:
        if delimiter == 't':
            writer = csv.writer(out_file, dialect='excel-tab',
                          quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        else:
            writer = csv.writer(out_file, delimiter=delimiter, dialect='excel',
                          quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        for line in result_txt:
            sl = line.strip().split('\t')
            writer.writerow(sl)
    os.remove(tmp_out_path)
    sys.stdout.write('Wrote file %s to desktop.\n' % out_file_name)
    sys.exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('Token', type=str,
                        help='API token of the account from which this query ran')
    parser.add_argument('Query_ID', type=int,
                        help='The ID of the query whose results you wish to download')
    parser.add_argument('-o', '--output',
                        help='The name of the file you wish to write to')
    parser.add_argument('-d', '--delimiter', type=str,
                        help='Custom delimiter you would like to use')
    args = parser.parse_args()
    main(args)
