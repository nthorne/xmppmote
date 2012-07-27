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

""" This module tests the client module. """

import sys
import os

sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("../.."))

import mox

from pyxmpp.jabber.client import JabberClient
from pyxmpp.all import JID
from versionhandler import VersionHandler

from client import Client
from configuration import commands

import unittest

class ClientTest(mox.MoxTestBase):
    """ Testing the trickier parts of the Client module """

    __usr = "JID"
    __pwd = "PWD"

    def test__init__(self):
        """ Ensure that the proper superclass methods are called and
            that the interface providers are set. """
        jid = JID(self.__usr)
        jid = JID(jid.node, jid.domain, "XMPPMote")

        self.mox.StubOutWithMock(JabberClient, "__init__")
        self.mox.StubOutWithMock(commands, "get_command_handler")
        self.mox.StubOutWithMock(VersionHandler, "__init__")
        JabberClient.__init__(mox.IgnoreArg(), jid, self.__pwd,
                disco_name = "XMPPMote", disco_type = "bot",
                tls_settings = None)
        VersionHandler.__init__(mox.IgnoreArg())
        commands.get_command_handler(mox.IgnoreArg()).AndReturn("foobar")
        self.mox.ReplayAll()

        cli = Client(JID(self.__usr), self.__pwd)

        self.assertTrue(isinstance(cli.interface_providers[0], VersionHandler))
        self.assertEquals("foobar", cli.interface_providers[1])


if "__main__" == __name__:
    unittest.main()
