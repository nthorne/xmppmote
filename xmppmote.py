#!/usr/bin/python -u

#Copyright (C) 2012 Niklas Thorne.
#
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

""" XMPPMote - XMPP remote administration framework

XMPPMote provides a basic remote administration facility, by means of the XMPP
protocol.  """

import sys
import logging
import logging.handlers
import locale
import codecs

from pyxmpp.all import JID

from bot.client import Client

def set_encoding():
    """ Convert unicode input to current locale. """
    locale.setlocale(locale.LC_CTYPE, "")
    encoding = locale.getlocale()[1]
    if not encoding:
        encoding = "us-ascii"
    sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
    sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")

def setup_logging():
    """ Set logging format and log level in order to get nicely written
    log statements from both PyXMPP and XMPPMote. """

    logging.basicConfig(format = '%(asctime)-15s %(message)s')

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logger.info(u"starting application..")

    syslog_handler = logging.handlers.SysLogHandler(
            facility = logging.handlers.SysLogHandler.LOG_DAEMON,
            address = "/dev/log")

    syslog_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)-15s %(message)s')
    syslog_handler.setFormatter(formatter)

    logger.addHandler(syslog_handler)

    logging.info(u"redirecting logs to syslog..")

    # remove the StreamHandler for syslog-only logging
    logger.removeHandler(logger.handlers[0])

    return logger

def display_usage(appname):
    """ Display the usage screen. """
    print u"Usage: %s JID [PASSWORD]" % (appname)
    print u"Connect the XMPPMote bot using JID and the optional password."
    print u"If no password is given, it will be read from stdin."

def parse_arguments(args):
    """ Parse command line arguments. """
    if not args:
        sys.stderr.write("error: invalid arguments list")
        sys.exit(1)
    elif 2 == len(args):
        if "-h" == args[1] or "--help" == args[1]:
            display_usage(args[0])
            sys.exit(0)

        usr = args[1]
        pwd = raw_input("Password:")
    elif 3 == len(args):
        usr = args[1]
        pwd = args[2]
    else:
        display_usage(args[0])
        sys.exit(1)

    return (usr, pwd)

def connect_client(usr, pwd, logger):
    """ Helper function used for connecting to the network. """
    client = Client(JID(usr), pwd)
    client.connect()

    try:
        client.loop(1)
    except KeyboardInterrupt:
        client.disconnect()
        logger.info(u"disconnecting..")

def main():
    """ main functionalities placed here in order to prevent pollution
        of the module-level namespace. """
    set_encoding()
    logger = setup_logging()

    usr, pwd = parse_arguments(sys.argv)

    connect_client(usr, pwd, logger)


if "__main__" == __name__:
    main()
