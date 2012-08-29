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

import __builtin__
import sys
import os
import logging

sys.path.append(os.path.abspath(".."))

import xmppmote
import mox

from bot.client import Client
from pyxmpp.all import JID

from configuration.configurationparser import ConfigurationParser

import unittest

class XMPPMoteTest(mox.MoxTestBase):
    """ Testing the trickier parts of the xmppmote module """

    __app = "xmppmote.py"
    __usr = "JID"
    __pwd = "PWD"

    def test_parse_arguments(self):
        """ Test the parse_arguments function with [0, 4] arguments
            as well as the help flags. """
        arguments = None
        with self.assertRaises(SystemExit) as context_manager:
            xmppmote.parse_arguments(arguments)
        self.assertEqual(context_manager.exception.code, 1)

        arguments = []
        with self.assertRaises(SystemExit) as context_manager:
            xmppmote.parse_arguments(arguments)
        self.assertEqual(context_manager.exception.code, 1)

        arguments = [self.__app]
        try:
            xmppmote.parse_arguments(arguments)
        except Exception:
            self.fail("Unexpected assertion")

        arguments = [self.__app, "-h"]
        with self.assertRaises(SystemExit) as context_manager:
            xmppmote.parse_arguments(arguments)
        self.assertEqual(context_manager.exception.code, 0)

        arguments = [self.__app, "--help"]
        with self.assertRaises(SystemExit) as context_manager:
            xmppmote.parse_arguments(arguments)
        self.assertEqual(context_manager.exception.code, 0)

        arguments = [self.__app, self.__usr, self.__pwd]
        with self.assertRaises(SystemExit) as context_manager:
            xmppmote.parse_arguments(arguments)
        self.assertEqual(context_manager.exception.code, 1)

        arguments = [self.__app, self.__usr, self.__pwd, "superfluous"]
        with self.assertRaises(SystemExit) as context_manager:
            xmppmote.parse_arguments(arguments)
        self.assertEqual(context_manager.exception.code, 1)


    def test_connect_client(self):
        """ Test the connect_client function, using Mox in order to verify
            proper connection procedure. """

        self.mox.StubOutWithMock(Client, "__init__")
        self.mox.StubOutWithMock(Client, "connect")
        self.mox.StubOutWithMock(Client, "loop")
        self.mox.StubOutWithMock(Client, "disconnect")
        Client.__init__(JID(self.__usr), self.__pwd)
        Client.connect()
        Client.loop(1).AndRaise(KeyboardInterrupt)
        Client.disconnect()
        self.mox.ReplayAll()

        xmppmote.connect_client(self.__usr, self.__pwd, logging.getLogger())

    def test_parse_config_file(self):
        """ Test parsing the configuration, when it exists. """

        mock_file = self.mox.CreateMockAnything()
        mock_file.name = "xmppmoterc"

        self.mox.StubOutWithMock(__builtin__, "open")
        self.mox.StubOutWithMock(ConfigurationParser, "parse")

        config = ConfigurationParser()
        open("xmppmoterc", "a+").AndReturn(mock_file)
        config.parse(mock_file)

        self.mox.ReplayAll()

        xmppmote.parse_config_file()
    

if "__main__" == __name__:
    unittest.main()
