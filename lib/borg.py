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

""" This module provides Borg pattern functionality. """



def make_borg():
    """ This function creates a Borg type which is to be subclassed for shared
    state between subclass instances. """

    class Borg(object):
        """ This type implements the Borg pattern. """
        __shared_state = {}

        def __init__(self):
            self.__dict__ = self.__shared_state

    return Borg
