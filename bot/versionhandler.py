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

""" XMPPMote VersionHandler module

This module implements a version query handler. """

from pyxmpp.interface import implements
from pyxmpp.interfaces import IIqHandlersProvider
from pyxmpp.interfaces import IFeaturesProvider

class VersionHandler(object):
    """Provides handler for a version query.
    
    This class will answer version query and announce 'jabber:iq:version' namespace
    in the client's disco#info results."""
    
    implements(IIqHandlersProvider, IFeaturesProvider)

    def __init__(self, client):
        """Just remember who created this."""
        self.client = client

    @classmethod
    def get_features(cls):
        """Return namespace which should the client include in its reply to a
        disco#info query."""
        return ["jabber:iq:version"]

    def get_iq_get_handlers(self):
        """Return list of tuples (element_name, namespace, handler) describing
        handlers of <iq type='get'/> stanzas"""
        return [
                ("query", "jabber:iq:version", self.get_version),
                ]

    @classmethod
    def get_iq_set_handlers(cls):
        """Return empty list, as this class provides no
           <iq type='set'/> stanza handler."""
        return []

    @classmethod
    def get_version(cls, iq_query):
        """Handler for jabber:iq:version queries.

        jabber:iq:version queries are not supported directly by PyXMPP, so the
        XML node is accessed directly through the libxml2 API.    This should be
        used very carefully!"""
        iq_query = iq_query.make_result_response()
        new_iq_query = iq_query.new_query("jabber:iq:version")
        new_iq_query.newTextChild(new_iq_query.ns(), "name", "Echo component")
        new_iq_query.newTextChild(new_iq_query.ns(), "version", "1.0")
        return iq_query
