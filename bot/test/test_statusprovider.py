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

""" This module tests the statusprovider module. """

import sys
import os

sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("../.."))

import mox
import unittest

from ConfigParser import SafeConfigParser
from ConfigParser import NoOptionError
from statusprovider import StatusProvider
from commandhandlers import CommandHandler
from configuration.configurationparser import ConfigurationParser
import threading
import subprocess
import logging

class StatusProviderTest(mox.MoxTestBase):
    """ This type provides test cases for the StatusProvider type. """

    def __setup_parser(self):
        mock_file = self.mox.CreateMockAnything()
        mock_file.closed = False
        mock_file.name = "foobar"

        config = ConfigurationParser()
        config.parse(mock_file)


    def test_existing_status_config_section(self):
        """ If we have an existing, properly configured status section,
        StatusProvider will, after having been started, execute the configured
        command after the configured timeout has elapsed, by starting a
        threading.Timer. """

        self.__setup_parser()

        self.mox.StubOutWithMock(SafeConfigParser, "has_section")
        self.mox.StubOutWithMock(SafeConfigParser, "get")
        self.mox.StubOutWithMock(threading, "Timer")
        self.mox.StubOutWithMock(threading.Thread, "start")
        self.mox.StubOutWithMock(subprocess.Popen, "__init__")
        self.mox.StubOutWithMock(subprocess.Popen, "communicate")
        self.mox.StubOutWithMock(CommandHandler, "change_status")

        SafeConfigParser.has_section("status").AndReturn(True)
        SafeConfigParser.get("status", "command").AndReturn("foobar")
        SafeConfigParser.get("status", "interval").AndReturn(3)

        threading.Timer(3, mox.IgnoreArg())
        threading.Thread.start()

        subprocess.Popen.__init__("foobar", stdout = subprocess.PIPE)
        subprocess.Popen.communicate().AndReturn("result")

        CommandHandler.change_status("result")

        threading.Timer(3, mox.IgnoreArg())
        threading.Thread.start()

        self.mox.ReplayAll()

        provider = StatusProvider()
        provider.start()
        # We'll have to emulate a timeout here..
        provider.timeout()

    def test_nonexisting_status_config_section(self):
        """ If there is no status section in the configuration file, no timer
        will be started, and no status updates will be performed. """

        self.__setup_parser()

        self.mox.StubOutWithMock(SafeConfigParser, "has_section")

        SafeConfigParser.has_section("status").AndReturn(False)

        self.mox.ReplayAll()

        provider = StatusProvider()
        provider.start()

    def test_existing_status_config_section_missing_interval(self):
        """ If the command execution frequency is missing from the
        configutation, no action will be taken (as with the case of missing
        status section). """

        self.__setup_parser()

        self.mox.StubOutWithMock(SafeConfigParser, "has_section")
        self.mox.StubOutWithMock(SafeConfigParser, "get")

        SafeConfigParser.has_section("status").AndReturn(True)
        SafeConfigParser.get("status", "command").AndReturn("uptime")
        SafeConfigParser.get("status",
                             "interval").AndRaise(NoOptionError("status",
                                                                "interval"))

        self.mox.ReplayAll()

        provider = StatusProvider()
        provider.start()

    def test_existing_status_config_section_missing_command(self):
        """ If the command itself is missing from the section, no action will be
        taken (as with the case of missing status section). """

        self.__setup_parser()

        self.mox.StubOutWithMock(SafeConfigParser, "has_section")
        self.mox.StubOutWithMock(SafeConfigParser, "get")

        SafeConfigParser.has_section("status").AndReturn(True)
        SafeConfigParser.get("status",
                             "command").AndRaise(NoOptionError("status",
                                                               "command"))

        self.mox.ReplayAll()

        provider = StatusProvider()
        provider.start()

    def test_existing_status_config_section_erroneous_command(self):
        """ If the command is configured, but does not exist, status will not be
        updated, but a log statement will be written to the syslog to indicate
        the configuration error. """

        self.__setup_parser()

        mock_logger = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(SafeConfigParser, "has_section")
        self.mox.StubOutWithMock(SafeConfigParser, "get")
        self.mox.StubOutWithMock(threading, "Timer")
        self.mox.StubOutWithMock(threading.Thread, "start")
        self.mox.StubOutWithMock(subprocess.Popen, "__init__")
        self.mox.StubOutWithMock(subprocess.Popen, "communicate")
        self.mox.StubOutWithMock(logging, "getLogger")
        self.mox.StubOutWithMock(CommandHandler, "change_status")

        SafeConfigParser.has_section("status").AndReturn(True)
        SafeConfigParser.get("status", "command").AndReturn("foobar")
        SafeConfigParser.get("status", "interval").AndReturn(3)

        threading.Timer(3, mox.IgnoreArg())
        threading.Thread.start()

        subprocess.Popen.__init__("foobar", stdout = subprocess.PIPE)
        subprocess.Popen.communicate().AndRaise(OSError)

        logging.getLogger().AndReturn(mock_logger)
        mock_logger.error("%s: error executing status command.")

        self.mox.ReplayAll()

        provider = StatusProvider()
        provider.start()
        # We'll have to emulate a timeout here..
        provider.timeout()


if "__main__" == __name__:
    unittest.main()
