#!/usr/bin/python

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

""" This module tests the versionhandler module. """

import sys
import os

sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("../.."))

import mox
import unittest

from versionhandler import VersionHandler


class VersionHandlerTest(mox.MoxTestBase):
    """ This type provides tests cases for the VersionHandler type. """ 
    def test_get_features(self):
        """ Make sure that we have a handler for each feature. """
        mock_client = self.mox.CreateMockAnything()
        mock_iq = self.mox.CreateMockAnything()
        new_mock_iq = self.mox.CreateMockAnything()
        mock_query = self.mox.CreateMockAnything()

        mock_iq.make_result_response().AndReturn(new_mock_iq)
        new_mock_iq.new_query(mox.IgnoreArg()).AndReturn(mock_query)
        mock_query.ns()
        mock_query.newTextChild(
                mox.IgnoreArg(),
                mox.IgnoreArg(),
                mox.IgnoreArg())
        mock_query.ns()
        mock_query.newTextChild(
                mox.IgnoreArg(),
                mox.IgnoreArg(),
                mox.IgnoreArg())

        self.mox.ReplayAll()

        version_handler = VersionHandler(mock_client)
        features = version_handler.get_features()

        for feat in features:
            got_handler = False
            for (element, namespace, handler) in \
                version_handler.get_iq_get_handlers():
                if namespace == feat:
                    got_handler = True
                    self.assertNotEqual(None, handler(mock_iq))
                    break
            self.assertTrue(got_handler)

    def test_set_features(self):
        """ Testing the set handlers of the Client. """
        mock_client = self.mox.CreateMockAnything()
        self.mox.ReplayAll()

        version_handler = VersionHandler(mock_client)
        self.assertEquals([], version_handler.get_iq_set_handlers())


if "__main__" == __name__:
    unittest.main()
