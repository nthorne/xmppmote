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
import sys
sys.path.append(os.path.abspath(".."))

from lib import borg

from ConfigParser import SafeConfigParser


class FileNotFoundException(Exception):
    """ This exception is raised upon nonexisting configuration file. """
    pass


class ConfigurationParser(borg.make_borg()):
    """ Implements the ConfigurationParser type, which is responsible for
    presenting the XMPPMote configuration file's key-value pairs to the
    application. """

    def __init__(self):
        super(ConfigurationParser, self).__init__()

    def parse(self, rcfile):
        """ Parse the configuration file retrieved as given by the file-like
        object _rcfile_. """

        self.__parser = SafeConfigParser()

        if None == rcfile or rcfile.closed:
            raise FileNotFoundException

        self.__parser.read(rcfile.name)
        self.__fp = rcfile

    def __getattr__(self, attrib):
        """ This implements the proxy pattern, effectively delegating any
        non-wrapped functions to the SafeConfigParser type. """

        wrapped_attr = getattr(self.__parser, attrib)

        def save_state_wrapper(*args):
            """ This function wraps getattr calls in such a way that any state
            modifying call will result in the parser state being written to
            disk. """
            result = wrapped_attr(*args)

            # if a modifying call was performed, save the parser state to disk
            if 'set' == attrib or attrib.startswith('add_') or attrib.startswith('remove_'):
                self.__save_state()

            return result

        return save_state_wrapper

    def __save_state(self):
        """ Tiny helper function for saving the configuration state to disk. """

        self.__fp.truncate(0)
        self.__parser.write(self.__fp)
        self.__fp.flush()
