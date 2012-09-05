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

""" This module contains the command handlers available to the bot.

These command handlers are responsible for handling the commands
received from a remote cllient, by means of eg. executing the
command, or comparing it to a list of allowed commands. """

from pyxmpp.all import Message, Presence
from pyxmpp.interface import implements
from pyxmpp.interfaces import IMessageHandlersProvider
from pyxmpp.interfaces import IPresenceHandlersProvider

import logging
import re
import subprocess
import sys
import os
sys.path.append(os.path.abspath('..'))

import configuration.commands
from bot.client import Client

class CommandHandler(object):
    """Provides the actual command functionality.

    Handlers for presence and message stanzas are implemented here.
    """

    implements(IMessageHandlersProvider, IPresenceHandlersProvider)
    
    def get_message_handlers(self):
        """Return list of (message_type, message_handler) tuples.

        The handlers returned will be called when matching message is received
        in a client session."""
        return [
                ("normal", self.message),
            ]

    def get_presence_handlers(self):
        """Return list of (presence_type, presence_handler) tuples.

        The handlers returned will be called when matching presence stanza is
        received in a client session."""
        return [
                (None, self.presence),
                ("unavailable", self.presence),
                ("subscribe", self.presence_control),
                ("subscribed", self.presence_control),
                ("unsubscribe", self.presence_control),
                ("unsubscribed", self.presence_control),
                ]

    def message(self, stanza):
        """Message handler for the component.

        Echoes the message back if its type is not 'error' or
        'headline', also sets own presence status to the message body. Please
        note that all message types but 'error' will be passed to the handler
        for 'normal' message unless some dedicated handler process them.

        :returns: `True` to indicate, that the stanza should not be processed
        any further."""
        subject = stanza.get_subject()
        body = stanza.get_body()
        typ = stanza.get_type()

        self.log_message(stanza, subject, body, typ)
        
        if stanza.get_type() == "headline":
            # 'headline' messages should never be replied to
            return True
        if subject:
            subject = u"Re: " + subject

        if body:
            response = self.parse_body(body)
    
            if not response:
                response = "unknown command"
        else:
            response = None
                
        msg = Message(
                to_jid = stanza.get_from(),
                from_jid = stanza.get_to(),
                stanza_type = typ,
                subject = subject,
                body = response)
        return msg

    def change_status(self, msg = u"awaiting command", available = True):
        """ Helper function to change the bot availability status. """
        if available:
            presence_stanza = Presence(
                stanza_type = u"available",
                status = msg
            )
        else:
            presence_stanza = Presence(
                stanza_type = u"unavailable",
                status = msg
            )

        self.client.get_stream().send(presence_stanza)

    def presence(self, stanza):
        """Handle 'available' (without 'type') and 'unavailable' <presence/>."""
        msg = u"%s has become " % (stanza.get_from())
        typ = stanza.get_type()
        if typ == "unavailable":
            msg += u"unavailable"
        else:
            msg += u"available"

        show = stanza.get_show()
        if show:
            msg += u"(%s)" % (show, )

        status = stanza.get_status()
        if status:
            msg += u": " + status

        logger = logging.getLogger()
        logger.info(msg)

    def presence_control(self, stanza):
        """Handle subscription control <presence/> stanzas -- acknowledge
        them."""

        self.log_presence_control(stanza)

        return stanza.make_accept_response()

    def parse_body(self, body):
        """ Override this for altered command parsing. """

        return body

    def do_command(self, command, args = None):
        """ Override this one for altered command handling. """
        pass

    def log_message(self, stanza, subject, body, typ):
        """ Construct a log message from a received message. """
        msg = u'Message from %s received.' % (unicode(stanza.get_from(), ))
        if subject:
            msg = msg + u'Subject: "%s".' % (subject, )
        if body:
            msg = msg + u'Body: "%s".' % (body, )
        if typ:
            msg = msg + u'Type: "%s".' % (typ, )
        else:
            msg = msg + u'Type: "normal".'

        logger = logging.getLogger()
        logger.info(msg)

    def log_presence_control(self, stanza):
        """ Construct a log message from a <presence/> stanza. """
        msg = unicode(stanza.get_from())
        typ = stanza.get_type()
        if typ == "subscribe":
            msg += u" has requested presence subscription."
        elif typ == "subscribed":
            msg += u" has accepted our presence subscription request."
        elif typ == "unsubscribe":
            msg += u" has canceled his subscription of our."
        elif typ == "unsubscribed":
            msg += u" has canceled our subscription of his presence."

        logger = logging.getLogger()
        logger.info(msg)


class RestrictedCommandHandler(CommandHandler):
    """ This type implements a restricted command feature.

        Any command parsed by this type is tested for existence in the
        list returned by the restricted_set function in the commands module,
        and if the command exists within that set, it is executed as a
        system command. """
    def parse_body(self, body):
        """ Overridden in order to provide for help requests. """
        response = None
        if body:
            for (command, args, hlp) in configuration.commands.restricted_set():
                if re.match("^help((\s+" + command + "\s*)|(\s*))$", body):
                    if response:
                        response = "%s\n%s - %s" % (response, command, hlp)
                    else:
                        response = "%s - %s" % (command, hlp)
                if command == body:
                    response = self.do_command(command, args)

        return response

    def do_command(self, command, args = None):
        """ Overridden in order to provide the restricted command set
            feature. """
        if "bye" == command:
            client = Client()
            client.disconnect()
            return u"terminating.."


        cmd = [command]
        if args:
            cmd.extend(args)
        try:
            body = self.make_syscall(cmd)
        except OSError as ex:
            body = "%s: %s (%d)" % (type(ex), ex.strerror, ex.errno)

        return body

    def make_syscall(self, command):
        """ Execute command in a subprocess. """
        subp = subprocess.Popen(command, stdout=subprocess.PIPE)
        stdoutdata = subp.communicate()[0]
        return "%s (%d):\n%s" % (command, subp.returncode, stdoutdata)


class UnsafeCommandHandler(RestrictedCommandHandler):
    """ This type implements a pass-thru command handler.

        Any command passed to this type is passed for execution in a subprocess,
        so use this type with care. """
    def parse_body(self, body): 
        response = None

        if body:
            args = body.split()
            command = args.pop(0)

            response = self.do_command(command, args)

        return response

