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

""" This module contains a JabberClient subclass.

The Client type implements the initialization required for the network
connection, as well as the appropriate event logging. """

from pyxmpp.all import JID
from pyxmpp.jabber.client import JabberClient
from versionhandler import VersionHandler

import logging
import os
import sys

sys.path.append(os.path.abspath('..'))
import configuration.commands


class Client(JabberClient):
    """ This type subclasses the JabberClient type, in order to provde
        protocol-level setup. """

    def __init__(self, jid, password):
        self.__logger = logging.getLogger()

        # if bare JID is provided add a resource
        if not jid.resource:
            jid = JID(jid.node, jid.domain, "XMPPMote")

        JabberClient.__init__(self, jid, password,
            disco_name = "XMPPMote", disco_type = "bot",
            tls_settings = None)

        self.interface_providers = [
            VersionHandler(self),
            configuration.commands.get_command_handler(self),
        ]

    def stream_state_changed(self, state, arg):
        """ Called upon stream state changes. """
        self.__logger.info("%s %r" % (state, arg))

    def log_roster_item(self, item):
        """ Log a roster item on the logging interface. """
        if item.name:
            name = item.name
        else:
            name = u""
        self.__logger.info (u'%s "%s" subscription=%s groups=%s'
            % (unicode(item.jid), name, item.subscription,
            u",".join(item.groups)) )

    def roster_updated(self, item=None):
        """ This method is called upon roster updates. """
        if not item:
            self.__logger.info(u"My roster:")
            for item in self.roster.get_items():
                self.log_roster_item(item)
        else:
            self.__logger.info(u"Roster item updated:")
            self.log_roster_item(item)

