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

def get_command_handler(instance):
    """ Returns the command handler that is to parse incoming commands. """
    return UnsafeCommandHandler(instance)

def restricted_set():
    """ Returns the restricted command set to be allowed (if the
        RestrictedCommandHandler is to be used). The command set is defined
        as a List of tuples of (cmd, args, help), where cmd is the command
        to execute in a shell, args is the command arguments, and hlp
        is the help to display upon receiving the help command. """

    return [
        ("uptime", None, "List system uptime"),
        ("df", ["-h"], "Show disk usage"),
        ("bye", None, "Terminate XMPPMote")
    ]
    
