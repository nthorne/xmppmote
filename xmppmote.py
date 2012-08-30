#!/usr/bin/env python

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

from configuration import credentials
from configuration.configurationparser import ConfigurationParser

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

    formatter = logging.Formatter('%(asctime)-15s XMPPMote: %(message)s')
    syslog_handler.setFormatter(formatter)

    logger.addHandler(syslog_handler)

    logging.info(u"redirecting logs to syslog..")

    # remove the StreamHandler for syslog-only logging
    logger.removeHandler(logger.handlers[0])

    return logger

def display_usage(appname):
    """ Display the usage screen. """
    print u"Usage: %s [-h|--help]" % (appname)
    print u"Connect the XMPPMote bot."

def parse_arguments(args):
    """ Parse command line arguments. """
    if None == args or 0 == len(args):
        print u"Error: argv is None or empty"
        sys.exit(1)
    elif 2 == len(args) and ("-h" == args[1] or "--help" == args[1]):
        display_usage(args[0])
        sys.exit(0)
    elif 1 != len(args):
        print u"Error: unknown argument"
        print
        display_usage(args[0])
        sys.exit(1)

def connect_client(usr, pwd, logger):
    """ Helper function used for connecting to the network. """
    client = Client(JID(usr), pwd)
    client.connect()

    try:
        client.loop(1)
    except KeyboardInterrupt:
        client.disconnect()
        logger.info(u"disconnecting..")

def parse_config_file():
    """ Helper function that sets up the ConfigurationParser. """
    config = ConfigurationParser()

    fil = open("xmppmoterc", "a+")
    config.parse(fil)


def main():
    """ main functionalities placed here in order to prevent pollution
        of the module-level namespace. """
    set_encoding()

    parse_arguments(sys.argv)

    parse_config_file()
    usr, pwd = credentials.get_credentials()

    logger = setup_logging()

    connect_client(usr, pwd, logger)


if "__main__" == __name__:
    main()
