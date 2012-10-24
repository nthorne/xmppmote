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

""" This module contains the UpdateNotifyer type.

UpdateNotifyer is responsible for performing regular checks for software
updates, and if any are found, the user is notified of the update via bot status
update. """

import sys
import os

sys.path.append(os.path.abspath("../.."))

from bot.client import Client
from stableupdater import StableUpdater
from bleedingedgeupdater import BleedingEdgeUpdater

import threading

class UpdateNotifyer(object):
    """ UpdateNotifyer is responsible for querying the selected updater at the
    desired interval, and if an update is found, the bot status is updated to
    reflect this. """

    def __init__(self, repo, api_url, bleeding_edge = False, interval = 3600):
        self.has_update = False
        self.__timer = None

        if not bleeding_edge:
            self.__updater = StableUpdater(repo, api_url)
        else:
            self.__updater = BleedingEdgeUpdater(repo, api_url)

        self.__interval = interval

    def start(self):
        """ Start the UpdateNotifyer service. """

        self.__timer = threading.Timer(self.__interval, self.timeout)
        self.__timer.start()

    def stop(self):
        """ Stop the UpdateNotifyer service. """

        self.__timer.cancel()

    def timeout(self):
        """ Called upon by the Timer when self.__interval has elapsed. """

        had_update = self.has_update

        self.has_update = self.__updater.check()

        if self.has_update and not had_update:
            cli = Client()
            
            new_version = self.__updater.get_update_version()
            if new_version:
                cli.change_status(u"update available: %s" % new_version[:7])

        self.start()
