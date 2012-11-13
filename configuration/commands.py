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

""" XMPPMote configuration module

This module is used to control the basic settings of XMPPMote, such as
which CommandHandler to use and, if to be used, the restricted command
set to be used by that command handler. """

import sys
import os

sys.path.append(os.path.abspath('..'))

from bot.commandhandlers import UnsafeCommandHandler
from bot.commandhandlers import RestrictedCommandHandler

from configurationparser import ConfigurationParser
from ConfigParser import NoSectionError
from ConfigParser import NoOptionError


class UnknownHandler(Exception):
    """ This exception is raised whenever XMPPMote cannot locate a known command
    handler in the configuration file. """
    pass


class MalformedCommand(Exception):
    """ This exception is raised whenever a malformed command is encountered in
    the configuration file. """
    pass


def get_command_handler():
    """ Returns the command handler that is to parse incoming commands. """

    config = ConfigurationParser()
    handlers = {
        "restricted":   RestrictedCommandHandler(),
        "passthru":     UnsafeCommandHandler()
    }

    try:
        configured_handler = config.get("general", "handler").lower()
    except NoSectionError:
        raise UnknownHandler("[general] section not found in configuration")
    except NoOptionError:
        raise UnknownHandler("handler option not found under [general] section")

    result = handlers.get(configured_handler)

    if not result:
        raise UnknownHandler("unknown handler (valid are restricted/passthru")

    return result

def restricted_set():
    """ Returns the restricted command set to be allowed (if the
        RestrictedCommandHandler is to be used). The command set is defined
        as a List of tuples of (cmd, args, help), where cmd is the command
        to execute in a shell, args is the command arguments, and hlp
        is the help to display upon receiving the help command. """

    result = []

    config = ConfigurationParser()
    if config.has_section("commands"):
        options = config.items("commands")

        result = map(__transform_set, 
                     [tuple(value.split(':')) for (_, value) in options])

    return result
    

def __transform_set(tupl):
    """ Helper function used to transform a command tuple read from the
    configuration file. """

    fst, snd, thrd = (None, None, "")

    try:
        fst = tupl[0]
        snd = tupl[1]

        if 0 == len(snd):
            snd = None

        thrd = tupl[2]
    except IndexError:
        pass

    if not fst:
        raise MalformedCommand

    if snd:
        snd = [snd]

    return (fst, snd, thrd)
