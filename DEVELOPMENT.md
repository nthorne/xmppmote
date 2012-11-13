XMPPMote development
====================

Notes
-----
This development setup guide uses virtualenv(http://www.virtualenv.org/en/latest/index.html)
and pip(http://pypi.python.org/pypi/pip).

Dependencies
------------
    $ pip freeze
    coverage==3.5.3
    dnspython==1.10.0
    gitpy==0.6.0
    libxml2-python==2.6.9
    mox==0.5.3
    pyxmpp==1.1.2
    wsgiref==0.1.2

Setting up environment
----------------------
    $ virtualenv xmppmote
    $ cd xmppmote
    $ source bin/activate

    $ pip install coverage
    $ pip install dnspython
    $ pip install gitpy
    $ pip install ftp://xmlsoft.org/libxml2/python/libxml2-python-2.6.9.tar.gz
    $ pip install mox
    $ pip install pyxmpp

    $ git clone https://github.com/nthorne/xmppmote

Running unit tests
------------------
    $ ./run_all_tests.sh

Getting code coverage
---------------------
    $ ./get_test_coverage.sh

or, if you want branch coverage (will launch firefox after having generated
coverage files):

    $ ./get_test_coverage.sh -b

Linting all modules
-------------------
    $ ./lint_all_modules.sh
