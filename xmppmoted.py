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


from bot.client import Client
from bot.statusprovider import StatusProvider
from ConfigParser import NoOptionError
from ConfigParser import NoSectionError
from configuration.configurationparser import ConfigurationParser
from configuration import credentials
from configuration import updates
from lib.daemon import Daemon
from pyxmpp.all import JID
import codecs
import locale
import logging
import logging.handlers
import sys


class XMPPMoteDaemon(Daemon):
    """ This type subclasses the Daemon type in order to implement the XMPPMote
    daemon. """

    def __init__(self):
        self.__usr = self.__pwd =  None

        self.__parse_config_file()

        Daemon.__init__(self, self.__get_pidfile())

    def start(self):
        """ This method overrides Daemon.start in order to read the credentials
        when attempting to start a session. """

        # we need to read the credentials here, so that we won't attempt access
        # stdin and/or stdout after having daemonized..
        self.__usr, self.__pwd = credentials.get_credentials()
        Daemon.start(self)

    def stop(self):
        """ This method overrides Daemon.stop in order to disconnect the session
        when stopping the daemon. """

        client = Client()
        client.disconnect()

        Daemon.stop(self)

    def run(self):
        """ This method provides the main function of the daemon, i.e.
        connecting the XMPP client, and entering the application message loop.
        """

        try:
            self.__setup_logging()

            client = Client(JID(self.__usr), self.__pwd)
            client.connect()

            provider = StatusProvider()
            provider.start()

            update_handler = updates.get_update_handler()
            if update_handler:
                update_handler.start()

            client.loop(1)
        except Exception, exc:
            logger = logging.getLogger()
            logger.critical(u"encountered exception %s. terminating XMPPMote." %
                           repr(exc))

        client.disconnect()

    @staticmethod
    def __parse_config_file():
        """ Helper method that sets up the ConfigurationParser. """

        config = ConfigurationParser()

        fil = open("xmppmoterc", "a+")
        config.parse(fil)

    @staticmethod
    def __get_pidfile():
        """ Helper method that reads an (optionally) configured pidfile from the
        configuration file. """

        config = ConfigurationParser()

        try:
            pidfile = config.get("general", "pidfile")
        except (NoOptionError, NoSectionError):
            pidfile = None

        if not pidfile:
            pidfile = "/tmp/xmppmote.pid"

        return pidfile

    @staticmethod
    def __setup_logging():
        """ Set logging format and log level in order to get nicely written
        log statements from both PyXMPP and XMPPMote. """

        logging.basicConfig(format = '%(asctime)-15s %(message)s')

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

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


def set_encoding():
    """ Convert unicode input to current locale. """

    locale.setlocale(locale.LC_CTYPE, "")
    encoding = locale.getlocale()[1]
    if not encoding:
        encoding = "us-ascii"
    sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
    sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")


def display_usage(appname):
    """ Display the usage screen. """

    print u"Usage: %s -h | --help | start | stop | restart" % (appname)
    print u"Connect the XMPPMote bot."


def parse_arguments(args):
    """ Parse command line arguments. """

    if None == args or 0 == len(args):
        print u"Error: argv is None or empty"
        sys.exit(1)
    elif 2 == len(args):
        if "-h" == args[1] or "--help" == args[1]:
            display_usage(args[0])
            sys.exit(0)
        elif "start" == args[1]:
            daemon = XMPPMoteDaemon()
            daemon.start()
        elif "stop" == args[1]:
            daemon = XMPPMoteDaemon()
            daemon.stop()
        elif "restart" == args[1]:
            daemon = XMPPMoteDaemon()
            daemon.restart()
    else:
        print u"Error: unknown argument"
        print
        display_usage(args[0])
        sys.exit(1)


def main():
    """ main functionalities placed here in order to prevent pollution
        of the module-level namespace. """

    set_encoding()

    parse_arguments(sys.argv)


if "__main__" == __name__:
    main()
