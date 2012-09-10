#!/usr/bin/env python

#Copyright (C) 2012 Niklas Thorne.

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

""" This module tests the updatenotifyer module. """

import sys
import os

sys.path.append(os.path.abspath(".."))

import mox
import unittest

import updatenotifyer

class UpdateNotifyerTest(mox.MoxTestBase):
    def test_init_has_git(self):
        self.fail()

    def test_init_no_git(self):
        self.fail()

    def test_start(self):
        self.fail()

    def test_stop(self):
        self.fail()

    def test_check_version_not_defined(self):
        self.fail()

    def test_check_github_not_responding(self):
        self.fail()

    def test_check_no_newer_version_available(self):
        self.fail()

    def test_check_newer_version_available_git(self):
        self.fail()

    def test_check_newer_version_available_no_git(self):
        self.fail()


if "__main__" == __name__:
    unittest.main()
