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

""" This module tests the ConfigurationParser module """
import sys
import os

sys.path.append(os.path.abspath(".."))


import mox
import unittest

from configurationparser import ConfigurationParser
from configurationparser import FileNotFoundException

from ConfigParser import SafeConfigParser


class ConfigurationParserTest(mox.MoxTestBase):
    """ Contains test cases for the ConfigurationParser type """

    def test_borg_pattern(self):
        """ Ensure proper Borg pattern implementation """
        fst_parser = ConfigurationParser()
        snd_parser = ConfigurationParser()

        # Assert that the two different instances shares __dict__
        # (i.e. correctly implements the Borg pattern)
        self.assertTrue(fst_parser.__dict__ is snd_parser.__dict__)

    def test_parsing_existing_configuration_file(self):
        """ Test the parsing of an 'existing' file """
        existing_config_file = "thisfilewillappeartoexist"

        self.mox.StubOutWithMock(os.path, "isfile")
        self.mox.StubOutWithMock(SafeConfigParser, "read")

        os.path.isfile(existing_config_file).AndReturn(True)
        SafeConfigParser.read(existing_config_file)

        self.mox.ReplayAll()

        config = ConfigurationParser()
        try:
            config.parse(existing_config_file)
        except FileNotFoundException:
            self.fail()

    def test_parsing_nonexisting_configuration_file(self):
        """ Test the parsing of a 'nonexisting' file """
        nonexisting_config_file = "thisfilewillappearnottoexist"

        self.mox.StubOutWithMock(os.path, "isfile")
        self.mox.StubOutWithMock(SafeConfigParser, "read")

        os.path.isfile(nonexisting_config_file).AndReturn(False)

        self.mox.ReplayAll()

        config = ConfigurationParser()
        self.assertRaises(FileNotFoundException, config.parse,
                          nonexisting_config_file)

    def test_proxy_pattern(self):
        """ Do a basic test of the Proxy pattern implementation (we'll just
        ensure that a single function call is delegated) """
        config = ConfigurationParser()
        # This asserts that the owning class of the call to config.get is in
        # fact SafeConfigParser (i.e. the call was delegated (gotta love
        # reflection))
        self.assertEqual(config.get.im_class, SafeConfigParser)


if "__main__" == __name__:
    unittest.main()
