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

""" This module provides unit tests for the commands module. """

import sys
import os

sys.path.append(os.path.abspath("../.."))

import mox
import unittest

from ConfigParser import SafeConfigParser
from ConfigParser import NoSectionError
from ConfigParser import NoOptionError

from configuration.commands import get_command_handler
from configuration.commands import UnknownHandler
from configuration.commands import restricted_set
from configuration.commands import MalformedCommand

from configuration.configurationparser import ConfigurationParser
from bot import commandhandlers

class GetCommandHandlerTest(mox.MoxTestBase):
    """ Provides test cases for the get_command_handler function. """

    def test_getting_existing_commandhandlers(self):
        """ If any of the two known command handlers are configured, an instance
        of the named command handler should be returned by get_command_handler
        """

        mock_file = self.mox.CreateMockAnything()
        mock_file.closed = False
        mock_file.name = "foobar"

        mock_client = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(SafeConfigParser, "get")

        config = ConfigurationParser()
        config.parse(mock_file)

        # case this one wierdly just to make sure that character casing is taken
        # into consideration when parsing the string..
        config.get("general", "handler").AndReturn("rEstrIctEd")

        config.get("general", "handler").AndReturn("pAssthrU")

        self.mox.ReplayAll()

        expected_type = commandhandlers.RestrictedCommandHandler(mock_client)
        self.assertEquals(type(get_command_handler(mock_client)),
                          type(expected_type))

        expected_type = commandhandlers.UnsafeCommandHandler(mock_client)
        self.assertEquals(type(get_command_handler(mock_client)),
                          type(expected_type))

    def test_getting_nonexisting_commandhandler(self):
        """ If the command handler returned by the configuration is unknown to
        get_command_handler, an UnknownHandler exception should be raised. """

        mock_file = self.mox.CreateMockAnything()
        mock_file.closed = False
        mock_file.name = "foobar"

        mock_client = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(SafeConfigParser, "get")

        config = ConfigurationParser()
        config.parse(mock_file)

        config.get("general", "handler").AndReturn("foobar")

        self.mox.ReplayAll()

        self.assertRaises(UnknownHandler, get_command_handler, mock_client)

    def test_getting_commandhandler_undefined_in_config(self):
        """ If either the section or the option that details the command handler
        is missing, an UnknownHandler exception should be raised. """

        mock_file = self.mox.CreateMockAnything()
        mock_file.closed = False
        mock_file.name = "foobar"

        mock_client = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(SafeConfigParser, "get")

        config = ConfigurationParser()
        config.parse(mock_file)

        config.get("general", "handler").AndRaise(NoSectionError("general"))
        config.get("general", "handler").AndRaise(NoOptionError("general",
                                                                "handler"))

        self.mox.ReplayAll()

        self.assertRaises(UnknownHandler, get_command_handler, mock_client)
        self.assertRaises(UnknownHandler, get_command_handler, mock_client)

class GetRestrictedSetTest(mox.MoxTestBase):
    """ Provides test cases for the restricted_set function. """

    def test_getting_defined_restricted_set(self):
        """ Make sure that properly formed commands are parsed into a list of
        command tuples. """

        mock_file = self.mox.CreateMockAnything()
        mock_file.closed = False
        mock_file.name = "foobar"

        self.mox.StubOutWithMock(SafeConfigParser, "has_section")
        self.mox.StubOutWithMock(SafeConfigParser, "items")

        config = ConfigurationParser()
        config.parse(mock_file)

        config.has_section("commands").AndReturn(True)
        config.items("commands").AndReturn([
            ("foo", "ls::List files"),
            ("bar", "df:-h:Disk space usage (human readable)"),
            ("baz", "du:-sh .:"),
            ("foz", "pwd")
        ])

        self.mox.ReplayAll()

        self.assertEquals(restricted_set(), [
            ("ls", None, "List files"),
            ("df", ["-h"], "Disk space usage (human readable)"),
            ("du", ["-sh ."], ""),
            ("pwd", None, "")
        ])



    def test_restricted_set_missing_section(self):
        """ If there is no commands section in the configuration file, an empty
        list should be returned. """

        mock_file = self.mox.CreateMockAnything()
        mock_file.closed = False
        mock_file.name = "foobar"

        self.mox.StubOutWithMock(SafeConfigParser, "has_section")
        self.mox.StubOutWithMock(SafeConfigParser, "items")

        config = ConfigurationParser()
        config.parse(mock_file)

        config.has_section("commands").AndReturn(False)

        self.mox.ReplayAll()

        self.assertEquals(restricted_set(), [])


    def test_restricted_set_undefined_set(self):
        """ If there is a command section defined, but no commands in it, an
        empty list should be returned. """

        mock_file = self.mox.CreateMockAnything()
        mock_file.closed = False
        mock_file.name = "foobar"

        self.mox.StubOutWithMock(SafeConfigParser, "has_section")
        self.mox.StubOutWithMock(SafeConfigParser, "items")

        config = ConfigurationParser()
        config.parse(mock_file)

        config.has_section("commands").AndReturn(True)
        config.items("commands").AndReturn([])

        self.mox.ReplayAll()

        self.assertEquals(restricted_set(), [])


    def test_getting_malformed_restricted_set(self):
        """ If there is a malformed command defined in the commands section, a
        MalformedCommand should be raised. """

        mock_file = self.mox.CreateMockAnything()
        mock_file.closed = False
        mock_file.name = "foobar"

        self.mox.StubOutWithMock(SafeConfigParser, "has_section")
        self.mox.StubOutWithMock(SafeConfigParser, "items")

        config = ConfigurationParser()
        config.parse(mock_file)

        config.has_section("commands").AndReturn(True)
        config.items("commands").AndReturn([("foo", "")])

        self.mox.ReplayAll()

        self.assertRaises(MalformedCommand, restricted_set)


if "__main__" == __name__:
    unittest.main()
