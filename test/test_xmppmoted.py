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

""" This module tests the xmppmote module. """

import sys
import os

sys.path.append(os.path.abspath(".."))

from bot.client import Client
from bot.statusprovider import StatusProvider
from ConfigParser import SafeConfigParser
from configuration.configurationparser import ConfigurationParser
from configuration import credentials
from lib.daemon import Daemon
from pyxmpp.all import JID
import __builtin__
import mox
import unittest
import xmppmoted

class XMPPMoteTest(mox.MoxTestBase):
    """ Testing the trickier parts of the xmppmote module """

    __app = "xmppmoted.py"
    __usr = "JID"
    __pwd = "PWD"

    def test_parse_arguments(self):
        """ Test the parse_arguments function with [0, 4] arguments
            as well as the help flags.

            NOTE: daemon control is not tested here"""
        arguments = None
        with self.assertRaises(SystemExit) as context_manager:
            xmppmoted.parse_arguments(arguments)
        self.assertEqual(context_manager.exception.code, 1)

        arguments = []
        with self.assertRaises(SystemExit) as context_manager:
            xmppmoted.parse_arguments(arguments)
        self.assertEqual(context_manager.exception.code, 1)

        arguments = [self.__app]
        with self.assertRaises(SystemExit) as context_manager:
            xmppmoted.parse_arguments(arguments)
        self.assertEqual(context_manager.exception.code, 1)

        arguments = [self.__app, "-h"]
        with self.assertRaises(SystemExit) as context_manager:
            xmppmoted.parse_arguments(arguments)
        self.assertEqual(context_manager.exception.code, 0)

        arguments = [self.__app, "--help"]
        with self.assertRaises(SystemExit) as context_manager:
            xmppmoted.parse_arguments(arguments)
        self.assertEqual(context_manager.exception.code, 0)

        arguments = [self.__app, self.__usr, self.__pwd]
        with self.assertRaises(SystemExit) as context_manager:
            xmppmoted.parse_arguments(arguments)
        self.assertEqual(context_manager.exception.code, 1)

        arguments = [self.__app, self.__usr, self.__pwd, "superfluous"]
        with self.assertRaises(SystemExit) as context_manager:
            xmppmoted.parse_arguments(arguments)
        self.assertEqual(context_manager.exception.code, 1)


    def test_xmppmotedaemon_run(self):
        """ Test the run method of the XMPPMoteDaemon, using Mox in order to
        verify proper connection procedure. """

        self.mox.StubOutWithMock(StatusProvider, "__init__")
        self.mox.StubOutWithMock(StatusProvider, "start")
        self.mox.StubOutWithMock(Client, "__init__")
        self.mox.StubOutWithMock(Client, "connect")
        self.mox.StubOutWithMock(Client, "loop")
        self.mox.StubOutWithMock(Client, "disconnect")

        self.mox.StubOutWithMock(Daemon, "start")

        self.mox.StubOutWithMock(xmppmoted.XMPPMoteDaemon,
                                 "_XMPPMoteDaemon__parse_config_file")
        self.mox.StubOutWithMock(xmppmoted.XMPPMoteDaemon,
                                 "_XMPPMoteDaemon__get_pidfile")
        self.mox.StubOutWithMock(credentials, "get_credentials")

        xmppmoted.XMPPMoteDaemon._XMPPMoteDaemon__parse_config_file()
        xmppmoted.XMPPMoteDaemon._XMPPMoteDaemon__get_pidfile().AndReturn(None)

        Daemon.start(mox.IgnoreArg())

        credentials.get_credentials().AndReturn((self.__usr, self.__pwd))

        StatusProvider.__init__()
        StatusProvider.start()

        Client.__init__(JID(self.__usr), self.__pwd)

        Client.connect()
        Client.loop(1)
        Client.disconnect()
        self.mox.ReplayAll()

        daemon = xmppmoted.XMPPMoteDaemon()
        daemon.start()
        daemon.run()

    def test_parse_config_file(self):
        """ Test parsing the configuration, when it exists. """

        mock_file = self.mox.CreateMockAnything()
        mock_file.name = "xmppmoterc"

        self.mox.StubOutWithMock(__builtin__, "open")
        self.mox.StubOutWithMock(ConfigurationParser, "parse")
        self.mox.StubOutWithMock(xmppmoted.XMPPMoteDaemon,
                                 "_XMPPMoteDaemon__get_pidfile")
        self.mox.StubOutWithMock(Daemon, "__init__")

        config = ConfigurationParser()
        open("xmppmoterc", "a+").AndReturn(mock_file)
        config.parse(mock_file)
        xmppmoted.XMPPMoteDaemon._XMPPMoteDaemon__get_pidfile().AndReturn(None)
        Daemon.__init__(mox.IgnoreArg(), None)

        self.mox.ReplayAll()
    
        daemon = xmppmoted.XMPPMoteDaemon()


    def test_daemon_control(self):
        """ Ensure that the daemon is started, stopped and restarted properly
        when given the appropriate command line arguments. """

        self.mox.StubOutWithMock(xmppmoted.XMPPMoteDaemon, "__init__")
        self.mox.StubOutWithMock(xmppmoted.XMPPMoteDaemon, "start")
        self.mox.StubOutWithMock(xmppmoted.XMPPMoteDaemon, "stop")
        self.mox.StubOutWithMock(xmppmoted.XMPPMoteDaemon, "restart")

        xmppmoted.XMPPMoteDaemon.__init__()
        xmppmoted.XMPPMoteDaemon.start()

        xmppmoted.XMPPMoteDaemon.__init__()
        xmppmoted.XMPPMoteDaemon.stop()

        xmppmoted.XMPPMoteDaemon.__init__()
        xmppmoted.XMPPMoteDaemon.restart()

        self.mox.ReplayAll()

        arguments = [self.__app, "start"] 
        try:
            xmppmoted.parse_arguments(arguments)
        except Exception, e:
            self.fail("Unknown exception raised %s" % e)

        arguments = [self.__app, "stop"] 
        try:
            xmppmoted.parse_arguments(arguments)
        except Exception:
            self.fail("Unknown exception raised")
    
        arguments = [self.__app, "restart"] 
        try:
            xmppmoted.parse_arguments(arguments)
        except Exception:
            self.fail("Unknown exception raised")

    def test_getting_pidfile(self):
        """ Make sure that we read the pidfile option properly. """

        self.mox.StubOutWithMock(SafeConfigParser, "get")

        SafeConfigParser.get("general", "pidfile").AndReturn("foobar")
        SafeConfigParser.get("general", "pidfile").AndReturn("foobar")

        self.mox.ReplayAll()

        daemon = xmppmoted.XMPPMoteDaemon()
        self.assertEqual("foobar", daemon._XMPPMoteDaemon__get_pidfile())

    def test_getting_pidfile_pidfile_not_defined(self):
        """ Make sure that we read the pidfile option properly. """

        self.mox.StubOutWithMock(SafeConfigParser, "get")

        SafeConfigParser.get("general", "pidfile").AndReturn(None)
        SafeConfigParser.get("general", "pidfile").AndReturn(None)

        self.mox.ReplayAll()

        daemon = xmppmoted.XMPPMoteDaemon()
        self.assertEqual("/tmp/xmppmote.pid",
                         daemon._XMPPMoteDaemon__get_pidfile())


if "__main__" == __name__:
    unittest.main()
