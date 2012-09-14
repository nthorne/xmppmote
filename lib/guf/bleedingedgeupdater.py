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

""" This module contains the BleedingEdgeUpdater type.

BleedingEdgeUpdater is responsible for performing bleeding edge version checks
and updates of the software, against github. """

from updater import Updater


class BleedingEdgeUpdater(Updater):
    """ BleedingEdgeUpdater queries github for current commit id, and if that
    differs from the commit id of the installed software (if available), it
    attempts to update the installed version by pulling from github, if
    possible; otherwise a tarball of HEAD of origin/master is downloaded. """

    pass
