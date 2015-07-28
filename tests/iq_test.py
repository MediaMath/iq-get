"""Test IQ-Get"""

import argparse
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

def test_download_without_filename(token, command_id):
    s = subprocess.check_call(['iq-get', token, str(command_id)])
    output_filename = 'full_result_%s.csv' % (str(command_id),)
    output_path = '%s%s' % (os.path.expanduser('~/Desktop/'), output_filename,)
    assert os.path.exists(output_path)


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
    print args.Token, command_id
    test_download_without_filename(args.Token, command_id)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('Token', type=str,
                        help='API token of the account from which this query ran')
    parser.add_argument('-q', type=int,
                        help='Query ID')
    args = parser.parse_args()
    main(args)
