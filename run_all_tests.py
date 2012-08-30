#!/usr/bin/env python

#Copyright (C) 2012 Niklas Thörne.

#This file is part of XMPPMote.
#
#XMPPMote is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#XMPPMote is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with XMPPMote.  If not, see <http://www.gnu.org/licenses/>.

""" This module provides functionality for running all of XMPPMote's unit tests

In order to achieve automatic test execution, unittest.TestLoader.discover is
used, in conjunction with dynamic path expansion - this should allow for this
module to be able to run any discovered unit test without requiring any further
modifications. """

import os
import sys
import unittest


def construct_path(topdir):
    """ This function automatically expands the path to contain all the XMPPMote
    subdirectories in order for the imported unit tests, and their imports to,
    be valid. """

    subdirs = [t[0] for t in os.walk(topdir) if t[0].find('.git/') == -1]

    for subdir in subdirs:
        sys.path.append(subdir)


def discover_unit_tests(topdir):
    """ This function utilises the unittest.TestLoader.discover function in
    order to discover and execute any unit tests in the project root and below.
    """
    loader = unittest.TestLoader()
    suite = loader.discover(topdir)

    runner = unittest.TextTestRunner(verbosity = 1)
    runner.run(suite)


if '__main__' == __name__:
    PWD = os.path.dirname(os.path.abspath(__file__))

    construct_path(PWD)
    discover_unit_tests(PWD)

