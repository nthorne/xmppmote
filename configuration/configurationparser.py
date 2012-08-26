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

""" XMPPMote configuration parser module

This module is responsible for parsing the XMPPMote configuration file, and 
presenting its key-value pairs to the application.
"""

import os
from ConfigParser import SafeConfigParser


class FileNotFoundException(Exception):
    """ This exception is raised upon nonexisting configuration file. """
    pass


class Borg:
    """ Implements the Borg pattern (i.e. shared state between (sub)type
    instances, allowing us to keep away from the Singleton, which focuses on
    instance rather than state) """
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state


class ConfigurationParser(Borg):
    """ Implements the ConfigurationParser type, which is responsible for
    presenting the XMPPMote configuration file's key-value pairs to the
    application. """

    def __init__(self):
        Borg.__init__(self)
        self.__parser = SafeConfigParser()

    def parse(self, rcfile):
        """ Parse the configuration file named in _rcfile_. If the file does not
        exist, IOError will be raised. """
        
        # We do this simple open operation, just to test for file eistence
        if not os.path.isfile(rcfile):
            raise FileNotFoundException

        self.__parser.read(rcfile)

    def __getattr__(self, attrib):
        """ This implements the proxy pattern, effectively delegating any
        non-wrapped functions to the SafeConfigParser type. """
        return getattr(self.__parser, attrib)
