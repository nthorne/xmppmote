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


def get_credentials(credentials_file):
    """ Returns a tuple containing the user credentials, as read from the
        credentials file. """

    (username, password) = ('', '')

    try:
        fil = open(credentials_file)
    
        username = fil.readline()
        password = fil.readline()
    except IOError:
        pass


    if 0 == len(password):
        print "Error reading credentials file (%s). Please enter credentials."\
            %credentials_file
        username = raw_input("username: ")
        password = raw_input("password: ")

        fil = open(credentials_file, 'w')
        fil.writelines([username, "\n", password, "\n"])
        fil.close()

    return (username.strip(), password.strip())

