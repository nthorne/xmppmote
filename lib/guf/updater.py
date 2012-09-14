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

""" This module contains the Updater type.

Updater is the supertype for the StableUpdater and BleedingEdgeUpdater, and
provides common methods (e.g. extracting downloaded tarball, replacing
software). """

class Updater(object):
    """ Updater contains common methods used by the StableUpdater and
    BleedingEdgeUpdater. """

    # TODO: Drop this method (implemented for unit test purposes, until the
    # implementation is in place in the subtypes)
    def check(self):
        """ Perform a version check. """

        pass
