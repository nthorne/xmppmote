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
sys.path.append(os.path.abspath("../.."))


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
        existing_config_file = self.mox.CreateMockAnything()
        existing_config_file.closed = False
        existing_config_file.name = "foobar"

        self.mox.StubOutWithMock(SafeConfigParser, "read")

        SafeConfigParser.read(existing_config_file.name)

        self.mox.ReplayAll()

        config = ConfigurationParser()
        try:
            config.parse(existing_config_file)
        except FileNotFoundException:
            self.fail()

    def test_parsing_closed_configuration_file(self):
        """ Test the parsing of an closed file """
        existing_config_file = self.mox.CreateMockAnything()
        existing_config_file.closed = True

        self.mox.ReplayAll()

        config = ConfigurationParser()
        self.assertRaises(FileNotFoundException, config.parse,
                          existing_config_file)

    def test_parsing_nonexisting_configuration_file(self):
        """ Test the parsing of a 'nonexisting' file """
        self.mox.StubOutWithMock(SafeConfigParser, "read")

        self.mox.ReplayAll()

        config = ConfigurationParser()
        self.assertRaises(FileNotFoundException, config.parse,
                          None)

    def test_proxy_pattern(self):
        """ Do a basic test of the Proxy pattern implementation (we'll just
        ensure that a single function call is delegated) """
        config = ConfigurationParser()
        # This asserts that the owning class of the call to config.get is in
        # fact SafeConfigParser (i.e. the call was delegated (gotta love
        # reflection))
        self.assertEqual(config.get.__name__, 'save_state_wrapper')


    def test_setting_option(self):
        """ Test setting an option - this should be a simple delegate to
        SafeConfigParser.set, with a write upon successful set. """

        mock_file = self.mox.CreateMockAnything()
        mock_file.closed = False
        mock_file.name = "foobar"

        self.mox.StubOutWithMock(SafeConfigParser, "read")
        self.mox.StubOutWithMock(SafeConfigParser, "set")
        self.mox.StubOutWithMock(SafeConfigParser, "write")

        SafeConfigParser.read(mock_file.name)
        SafeConfigParser.set("credentials", "username", "foo")
        mock_file.truncate(0)
        mock_file.flush()
        SafeConfigParser.write(mock_file)

        self.mox.ReplayAll()
        
        config = ConfigurationParser()
        config.parse(mock_file)
        config.set("credentials", "username", "foo")

    def test_adding_section(self):
        """ Test adding a section - this should be a simple delegate to
        SafeConfigParser.add_section, with a write upon successful set. """

        mock_file = self.mox.CreateMockAnything()
        mock_file.closed = False
        mock_file.name = "foobar"

        self.mox.StubOutWithMock(SafeConfigParser, "read")
        self.mox.StubOutWithMock(SafeConfigParser, "add_section")
        self.mox.StubOutWithMock(SafeConfigParser, "write")

        SafeConfigParser.read(mock_file.name)
        SafeConfigParser.add_section("credentials")
        mock_file.truncate(0)
        mock_file.flush()
        SafeConfigParser.write(mock_file)

        self.mox.ReplayAll()
        
        config = ConfigurationParser()
        config.parse(mock_file)
        config.add_section("credentials")


if "__main__" == __name__:
    unittest.main()
