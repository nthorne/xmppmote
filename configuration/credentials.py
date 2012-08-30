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

""" XMPPMote credentials configuration module

This module supplies the credentials handling functionalities of
XMPPMote; i.e. reading the credentials from a configuration file.
"""

from configurationparser import ConfigurationParser
from ConfigParser import NoSectionError
from ConfigParser import NoOptionError


def get_credentials():
    """ Returns a tuple containing the user credentials, as read from the
    credentials section of the configuration file. """

    (username, password) = ('', '')

    try:
        config = ConfigurationParser()

        username = config.get("credentials", "username")
        password = config.get("credentials", "password")
    except NoSectionError:
        # We'll just allow for NoSectionError to pass through, since this one
        # (usually) indicates missing section
        config.add_section("credentials")
    except NoOptionError:
        # Allow missing options to slide by as well, since we'll just query the
        # user for the credentials
        pass


    if 0 == len(password):
        print "Error reading credentials from the configuration file.",
        print "Please enter credentials."

        username = raw_input("username: ")
        password = raw_input("password: ")

        config = ConfigurationParser()
        config.set("credentials", "username", username)
        config.set("credentials", "password", password)

    return (username.strip(), password.strip())

