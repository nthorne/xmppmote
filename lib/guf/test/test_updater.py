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

""" This module tests the updater module. """

import sys
import os

sys.path.append(os.path.abspath(".."))

import mox
import unittest

from updater import Updater

class UpdaterTest(mox.MoxTestBase):
    """ This type provides test cases for Updater. """ 

    __repo = "foo/bar"

    def test_download_update(self):
        """ download_update should default to calling download_tarball. This
        allows for nifty override, e.g. pullin with Git by subtype. """

        self.mox.StubOutWithMock(Updater, "download_tarball")

        Updater.download_tarball()
        
        self.mox.ReplayAll()

        updater = Updater(self.__repo)
        updater.download_update()

#    def test_download_tarball(self):
#        """ download_tarball should download the tarball found at
#        get_tarball_url, to get_target_directory """
#
#        self.mox.StubOutWithMock(Updater, "get_tarball_url")
#
#    def test_download_tarball_invalid_url(self):
#        self.fail("Test case not implemented")
#
#    def test_download_tarball_download_fails(self):
#        self.fail("Test case not implemented")


if "__main__" == __name__:
    unittest.main()
