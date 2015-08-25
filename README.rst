IQ-Get
======
A way to retrieve large Hive results from Qubole Data Service (QDS), made for clients of `Interactive Query <https://kb.mediamath.com/wiki/pages/viewpage.action?pageId=10651642>`_.

Installation
------------

-------------
Windows Users
-------------
To get Python, we recommend either the `Anaconda Python Shell <http://continuum.io/downloads>`_ or `Cygwin <https://www.cygwin.com/>`_. If using Cygwin, you may first need to run the command ``easy_install pip`` before installing this project.

From PyPI
---------
IQ-Get is available on `PyPI <https://pypi.python.org/pypi/IQ-Get>`_.

``pip install iq-get``


From Source
-----------

* Download the source code: ``git clone git@github.com:MediaMath/iq-get.git``
* Run the following commands (installing the project may require root)
  ::
    $ cd iq-get
    $ python setup.py install



Usage
-----
This is a command-line utility and can be used as follows:
::
    $ iq-get -h
        | usage: iq-get [-h] [-o OUTPUT] [-d DELIMITER] Token Query_ID
        |
        | positional arguments:
        |   Token                 API token of the account from which this query ran
        |   Query_ID              The ID of the query whose results you wish to download
        |
        | optional arguments:
        |   -h, --help            show this help message and exit
        |   -o OUTPUT, --output OUTPUT
        |                         The name of the file you wish to write to test
        |   -d DELIMITER, --delimiter DELIMITER
        |                         Custom delimiter you would like to use

    $ iq-get QDS_API_TOKEN 1234567                      # Will write a comma-delimited file with results of query with ID 1234567 to ~/Desktop/full_result_1234567.csv
    $ iq-get QDS_API_TOKEN 1234567 -o my_filename.csv   # Will write a comma-delimited file with results of query with ID 1234567 to ~/Desktop/my_filename.csv
    $ iq-get QDS_API_TOKEN 1234567 -d $'\t'             # Will write a tab-delimited file with results of query with ID 1234567 to ~/Desktop/full_result_1234567.tsv
