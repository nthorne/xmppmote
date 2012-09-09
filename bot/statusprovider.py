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

""" This module contains the StatusProvider type.

StatusProvider is responsible for providing the current XMPPMote status, as sent
to the chat counterpart. """

import sys
import os

sys.path.append(os.path.abspath(".."))

from configuration.configurationparser import ConfigurationParser
from ConfigParser import NoOptionError
from bot.client import Client

import threading
import subprocess
import logging

class StatusProvider(object):
    """ This type provides configurable status updates to the XMPPMote bot. """

    def __init__(self):
        self.__command = None
        self.__interval = None

        self.__previous_result = None

        parser = ConfigurationParser()

        logger = logging.getLogger()

        if parser.has_section("status"):
            try:
                logger.info("reading configured status command")

                self.__command = parser.get("status", "command")
                self.__interval = int(parser.get("status", "interval"))

                logger.info("executing '%s' every %d sec" % (self.__command,
                                                             self.__interval))
            except NoOptionError:
                pass


    def start(self):
        """ This method is responsible for setting a timer that, when having
        expired after the configured interval, executes the timeout method. """

        if self.__command and self.__interval:
            timer = threading.Timer(self.__interval, self.timeout)
            timer.start()

    def timeout(self):
        """ This method is responsible for executing the configured command. """

        try:
            subproc = subprocess.Popen(self.__command, stdout = subprocess.PIPE)
            stdout = subproc.communicate()[0]
        except OSError:
            logger = logging.getLogger()
            logger.error("%s: error executing status command.")
            return

        if self.__previous_result != stdout:
            client = Client()
            client.change_status(stdout)
            self.start()

            self.__previous_result = stdout
