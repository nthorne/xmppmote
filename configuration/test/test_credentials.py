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

""" This module tests the credentials module. """

# we import the builtin module here, since we need to refer to it explicitly,
# rather than by __builtins__ when we overload open and raw_input, since
# __builtins__ refers to the module when this script is a main script, and to a
# dict when this script is not a main script..
import __builtin__
import sys
import os

sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("../.."))

import mox

import credentials
from ConfigParser import SafeConfigParser
from ConfigParser import NoSectionError
from ConfigParser import NoOptionError
from configurationparser import ConfigurationParser

import unittest

class CredentialsTest(mox.MoxTestBase):
    """ Testing the credentials module """

    def test_get_credentials(self):
        """ Ensure proper behavior when the configuration file contains the
        username-password pair. """

        mock_file = self.mox.CreateMockAnything()
        mock_file.closed = False
        mock_file.name = "foobar"

        username, password = ("username@jabber.org", "password")

        self.mox.StubOutWithMock(SafeConfigParser, "get")

        config = ConfigurationParser()
        config.parse(mock_file)
        config.get("credentials", "username").AndReturn(username)
        config.get("credentials", "password").AndReturn(password)

        self.mox.ReplayAll()

        self.assertEquals((username, password), credentials.get_credentials())


    def test_get_credentials_missing_section(self):
        """ Test reading the credentials from a configuration file where the
        credentials section is missing (uninitialized). """

        mock_file = self.mox.CreateMockAnything()
        mock_file.closed = False
        mock_file.name = "foobar"

        username, password = ("username@jabber.org", "password")

        self.mox.StubOutWithMock(SafeConfigParser, "get")
        self.mox.StubOutWithMock(SafeConfigParser, "add_section")
        self.mox.StubOutWithMock(SafeConfigParser, "set")
        self.mox.StubOutWithMock(__builtin__, "raw_input")

        config = ConfigurationParser()
        config.parse(mock_file)
        error = NoSectionError("credentials")
        config.get("credentials", "username").AndRaise(error)

        config.add_section("credentials")

        raw_input(mox.IgnoreArg()).AndReturn(username)
        raw_input(mox.IgnoreArg()).AndReturn(password)

        config.set("credentials", "username", username)
        config.set("credentials", "password", password)

        self.mox.ReplayAll()

        self.assertEquals((username, password), credentials.get_credentials())


    def test_get_credentials_missing_username(self):
        """ Test reading the credentials from a configuration file where the
        username option is missing. """

        mock_file = self.mox.CreateMockAnything()
        mock_file.closed = False
        mock_file.name = "foobar"

        username, password = ("username@jabber.org", "password")

        self.mox.StubOutWithMock(SafeConfigParser, "get")
        self.mox.StubOutWithMock(SafeConfigParser, "set")
        self.mox.StubOutWithMock(SafeConfigParser, "write")
        self.mox.StubOutWithMock(__builtin__, "raw_input")

        config = ConfigurationParser()
        config.parse(mock_file)
        error = NoOptionError("credentials", "username")
        config.get("credentials", "username").AndRaise(error)

        raw_input(mox.IgnoreArg()).AndReturn(username)
        raw_input(mox.IgnoreArg()).AndReturn(password)

        config.set("credentials", "username", username)
        config.set("credentials", "password", password)

        self.mox.ReplayAll()

        self.assertEquals((username, password), credentials.get_credentials())


    def test_get_credentials_missing_password(self):
        """ Test reading the credentials from a configuration file where the
        password option is missing. """

        mock_file = self.mox.CreateMockAnything()
        mock_file.closed = False
        mock_file.name = "foobar"

        username, password = ("username@jabber.org", "password")

        self.mox.StubOutWithMock(SafeConfigParser, "get")
        self.mox.StubOutWithMock(SafeConfigParser, "set")
        self.mox.StubOutWithMock(__builtin__, "raw_input")

        config = ConfigurationParser()
        config.parse(mock_file)
        error = NoOptionError("credentials", "password")
        config.get("credentials", "username").AndReturn(username)
        config.get("credentials", "password").AndRaise(error)

        raw_input(mox.IgnoreArg()).AndReturn(username)
        raw_input(mox.IgnoreArg()).AndReturn(password)

        config.set("credentials", "username", username)
        config.set("credentials", "password", password)

        self.mox.ReplayAll()

        self.assertEquals((username, password), credentials.get_credentials())


if "__main__" == __name__:
    unittest.main()
