"""Test IQ-Get"""

from __future__ import print_function
import argparse
import csv
import os
import time
import subprocess
import qds_sdk
from qds_sdk.commands import Qubole, HiveCommand

TEST_QUERY = """
select * from default.default_qubole_memetracker limit 100;
"""

def setup():
    """
    Execute a test query and return the HiveCommand object
    """
    hc = HiveCommand.run(query=TEST_QUERY)
    return hc

def teardown(files):
    """
    Remove any files created as part of the test
    :params files: List[String] List of files to delete
    """
    print('Removing created files')
    for f in files:
        print(f)
        os.remove(f)
    return

def test_download_without_filename(token, command_id):
    s = subprocess.check_call(['iq-get', token, str(command_id)])
    output_filename = 'full_result_%s.csv' % (str(command_id),)
    output_path = '%s%s' % (os.path.expanduser('~/Desktop/'), output_filename,)
    assert os.path.exists(output_path)
    return output_path

def test_download_no_overwrite(token, command_id):
    s = subprocess.Popen(['iq-get', token, str(command_id)], stdout=subprocess.PIPE,
                                                            stdin=subprocess.PIPE)
    s.communicate("n")
    output_filename = 'full_result_%s(1).csv' % (str(command_id),)
    output_path = '%s%s' % (os.path.expanduser('~/Desktop/'), output_filename,)
    assert os.path.exists(output_path)
    return output_path

def test_download_overwrite(token, command_id):
    s = subprocess.Popen(['iq-get', token, str(command_id)], stdout=subprocess.PIPE,
                                                            stdin=subprocess.PIPE)
    s.communicate("y")
    output_filename = 'full_result_%s(2).csv' % (str(command_id),)
    output_path = '%s%s' % (os.path.expanduser('~/Desktop/'), output_filename,)
    assert not os.path.exists(output_path)
    return

def download_with_filename(token, command_id):
    output_filename = 'iq-get-custom-filename.csv'
    s = subprocess.check_call(['iq-get', token, str(command_id), '-o', output_filename])
    output_path = '%s%s' % (os.path.expanduser('~/Desktop/'), output_filename,)
    assert os.path.exists(output_path)
    with open(output_path) as f:
        reader = csv.reader(f)
        l = reader.next()
        assert len(l) == 5
    return output_path

def download_with_tabs(token, command_id):
    s = subprocess.check_call(['iq-get', token, str(command_id), '-d', '\t'])
    output_filename = 'full_result_%s.tsv' % (str(command_id),)
    output_path = '%s%s' % (os.path.expanduser('~/Desktop/'), output_filename,)
    assert os.path.exists(output_path)
    with open(output_path) as f:
        reader = csv.reader(f, delimiter='\t')
        l = reader.next()
        assert len(l) == 5
    return output_path


def main(args):
    """
    Set up the testing environment and then run all of the tests
    :params args: Namespace Command-line arguments
    """
    Qubole.configure(api_token=args.Token)
    command_id = args.q
    if args.q is None:
        hc = setup()
        command_id = hc.id
    print('Running tests with token %s and query ID %d' % (args.Token, command_id,))
    created_files = []
    created_files.append(test_download_without_filename(args.Token, command_id))
    created_files.append(test_download_no_overwrite(args.Token, command_id))
    test_download_overwrite(args.Token, command_id)
    created_files.append(download_with_filename(args.Token, command_id))
    created_files.append(download_with_tabs(args.Token, command_id))
    teardown(created_files)
    print('All tests passed!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('Token', type=str,
                        help='API token of the account from which this query ran')
    parser.add_argument('-q', type=int,
                        help='Query ID')
    args = parser.parse_args()
    main(args)
