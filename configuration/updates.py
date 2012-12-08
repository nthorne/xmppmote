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

""" This module contains functions used to construct a update handler from the
configuration data. """

import sys
import os

sys.path.append(os.path.abspath(".."))

from lib.guf.updatenotifyer import UpdateNotifyer

from configurationparser import ConfigurationParser

from ConfigParser import NoSectionError
from ConfigParser import NoOptionError


REPO = "nthorne/xmppmote"
DEFAULT_MODEL = "stable"
DEFAULT_INTERVAL = 3600


class UnknownModel(Exception):
    """ Exception raised upon unknown model encountered in configuration. """

    def __init__(self, msg):
        super(UnknownModel, self).__init__("Unknown update model: %s" % msg)

class UnknownAction(Exception):
    """ Exception raised upon unknown action encountered in configuration. """

    def __init__(self, msg):
        super(UnknownAction, self).__init__("Unknown update action: %s" % msg)

def __parse_model(model):
    """ Internal helper function that parses the model as read from the
    configuration, and returns a tuple consisting of a boolean indicating if
    bleeding edge, and an url used by the appropriate updater. """

    if not model or "stable" == model.lower():
        bleeding_edge = False
    elif "bleeding" == model.lower():
        bleeding_edge = True
    else:
        raise UnknownModel(model)

    return bleeding_edge


def get_update_handler():
    """ Construct and return an update handler from the configuration data. """

    action, model, interval = (None, DEFAULT_MODEL, DEFAULT_INTERVAL)

    try:
        config = ConfigurationParser()

        action = config.get("updates", "action")

        try:
            model = config.get("updates", "model")
        except NoOptionError:
            pass

        try:
            str_interval = config.get("updates", "interval")
            interval = int(str_interval)
        except (NoOptionError, ValueError):
            pass
    except (NoSectionError, NoOptionError):
        pass

    bleeding_edge = __parse_model(model)

    if not action:
        notifyer = None
    elif "notify" == action.lower():
        notifyer = UpdateNotifyer(REPO, bleeding_edge, interval)
    else:
        raise UnknownAction(action)

    return notifyer
