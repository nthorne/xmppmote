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

""" This module tests the commandhandlers module. """

import sys
import os

sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("../.."))

import mox
import unittest

from commandhandlers import CommandHandler
from commandhandlers import RestrictedCommandHandler
from commandhandlers import UnsafeCommandHandler
from pyxmpp.all import Message

import configuration.commands
import client


class CommandHandlerTest(mox.MoxTestBase):
    """ This type provides test cases for the CommandHandler type. """
    def test_get_message_handlers(self):
        """ Make sure that we've got one normal message handler, and
            that the handler is callable. """
        self.mox.ReplayAll()

        cmdhandler = CommandHandler()

        normal_handler = \
            [(typ, handler)
            for (typ, handler) in cmdhandler.get_message_handlers()
            if "normal" == typ]

        self.assertEquals(1, len(normal_handler))

        (typ, handler) = normal_handler[0]

        self.assertTrue(callable(handler))
        

    def test_get_presence_handlers(self):
        """ Make sure that the handler of eache presence type
           is in fact callable. """ 
        self.mox.ReplayAll()

        cmdhandler = CommandHandler()

        self.assertNotEquals([], cmdhandler.get_presence_handlers())

        for (typ, handler) in cmdhandler.get_presence_handlers():
            self.assertTrue(callable(handler))


    def test_message_headline(self):
        """ Ensure proper handling of a headline stanza. """
        mock_stanza = self.mox.CreateMockAnything()
        mock_subject = self.mox.CreateMockAnything()
        mock_body = self.mox.CreateMockAnything()
        mock_type = self.mox.CreateMockAnything()
        mock_client = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(CommandHandler, "__init__")
        self.mox.StubOutWithMock(CommandHandler, "parse_body")
        self.mox.StubOutWithMock(CommandHandler, "log_message")

        CommandHandler.__init__(mock_client)

        mock_stanza.get_subject().AndReturn(mock_subject)
        mock_stanza.get_body().AndReturn(mock_body)
        mock_stanza.get_type().AndReturn(mock_type)
        
        CommandHandler.log_message(
                mock_stanza,
                mock_subject,
                mock_body,
                mock_type)

        mock_stanza.get_type().AndReturn("headline")

        self.mox.ReplayAll()

        cmdhandler = CommandHandler(mock_client)
        self.assertEqual(True, cmdhandler.message(mock_stanza))

    def test_message_subject(self):
        """ Ensure proper handling of a subject stanza. """
        mock_stanza = self.mox.CreateMockAnything()
        mock_body = self.mox.CreateMockAnything()
        mock_client = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(CommandHandler, "__init__")
        self.mox.StubOutWithMock(CommandHandler, "parse_body")
        self.mox.StubOutWithMock(CommandHandler, "log_message")

        self.mox.StubOutWithMock(Message, "__init__")
        self.mox.StubOutWithMock(Message, "__del__")

        CommandHandler.__init__(mock_client)

        mock_stanza.get_subject().AndReturn("subject")
        mock_stanza.get_body().AndReturn(mock_body)
        mock_stanza.get_type().AndReturn("body")
        
        CommandHandler.log_message(mock_stanza, "subject", mock_body, "body")

        mock_stanza.get_type().AndReturn("body")

        CommandHandler.parse_body(mock_body).AndReturn("response")

        mock_stanza.get_from().AndReturn("from")
        mock_stanza.get_to().AndReturn("to")

        Message.__init__(
                to_jid = "from",
                from_jid = "to",
                stanza_type = "body",
                subject = u"Re: subject",
                body = "response")

        Message.__del__()

        self.mox.ReplayAll()

        cmdhandler = CommandHandler(mock_client)
        self.assertNotEqual(None, cmdhandler.message(mock_stanza))

    def test_message_no_subject(self):
        """ Ensure proper handling of a message without subject. """
        mock_stanza = self.mox.CreateMockAnything()
        mock_body = self.mox.CreateMockAnything()
        mock_client = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(CommandHandler, "__init__")
        self.mox.StubOutWithMock(CommandHandler, "parse_body")
        self.mox.StubOutWithMock(CommandHandler, "log_message")

        self.mox.StubOutWithMock(Message, "__init__")
        self.mox.StubOutWithMock(Message, "__del__")

        CommandHandler.__init__(mock_client)

        mock_stanza.get_subject()
        mock_stanza.get_body().AndReturn(mock_body)
        mock_stanza.get_type().AndReturn("body")
        
        CommandHandler.log_message(mock_stanza, None, mock_body, "body")

        mock_stanza.get_type().AndReturn("body")

        CommandHandler.parse_body(mock_body).AndReturn("response")

        mock_stanza.get_from().AndReturn("from")
        mock_stanza.get_to().AndReturn("to")

        Message.__init__(
                to_jid = "from",
                from_jid = "to",
                stanza_type = "body",
                subject = None,
                body = "response")

        self.mox.ReplayAll()

        cmdhandler = CommandHandler(mock_client)
        self.assertNotEqual(None, cmdhandler.message(mock_stanza))

    def test_message_no_response(self):
        """ Test a mesage that does not yield a parse result. """
        mock_stanza = self.mox.CreateMockAnything()
        mock_body = self.mox.CreateMockAnything()
        mock_client = self.mox.CreateMockAnything()
        self.mox.StubOutWithMock(CommandHandler, "__init__")
        self.mox.StubOutWithMock(CommandHandler, "parse_body")
        self.mox.StubOutWithMock(CommandHandler, "log_message")

        self.mox.StubOutWithMock(Message, "__init__")
        self.mox.StubOutWithMock(Message, "__del__")

        CommandHandler.__init__(mock_client)

        mock_stanza.get_subject()
        mock_stanza.get_body().AndReturn(mock_body)
        mock_stanza.get_type().AndReturn("body")
        
        CommandHandler.log_message(mock_stanza, None, mock_body, "body")

        mock_stanza.get_type().AndReturn("body")

        CommandHandler.parse_body(mock_body).AndReturn(None)

        mock_stanza.get_from().AndReturn("from")
        mock_stanza.get_to().AndReturn("to")

        Message.__init__(
                to_jid = "from",
                from_jid = "to",
                stanza_type = "body",
                subject = None,
                body = "unknown command")

        self.mox.ReplayAll()

        cmdhandler = CommandHandler(mock_client)
        self.assertNotEqual(None, cmdhandler.message(mock_stanza))

    def test_message_no_body(self):
        """ Ensure proper handling of a bodiless message. """
        mock_stanza = self.mox.CreateMockAnything()
        mock_client = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(CommandHandler, "__init__")
        self.mox.StubOutWithMock(CommandHandler, "parse_body")
        self.mox.StubOutWithMock(CommandHandler, "log_message")

        self.mox.StubOutWithMock(Message, "__init__")
        self.mox.StubOutWithMock(Message, "__del__")

        CommandHandler.__init__(mock_client)

        mock_stanza.get_subject()
        mock_stanza.get_body().AndReturn(None)
        mock_stanza.get_type().AndReturn("body")
        
        CommandHandler.log_message(mock_stanza, None, None, "body")

        mock_stanza.get_type().AndReturn("body")

        mock_stanza.get_from().AndReturn("from")
        mock_stanza.get_to().AndReturn("to")

        Message.__init__(
                to_jid = "from",
                from_jid = "to",
                stanza_type = "body",
                subject = None,
                body = None)

        self.mox.ReplayAll()

        cmdhandler = CommandHandler(mock_client)
        self.assertNotEqual(None, cmdhandler.message(mock_stanza))

    def test_presence_control(self):
        """ Test the handling of presence stanzas. """
        mock_stanza = self.mox.CreateMockAnything()
        mock_client = self.mox.CreateMockAnything()
        self.mox.StubOutWithMock(CommandHandler, "__init__")
        self.mox.StubOutWithMock(CommandHandler, "log_presence_control")

        CommandHandler.__init__(mock_client)
        CommandHandler.log_presence_control(mock_stanza)
        mock_stanza.make_accept_response().AndReturn(True)

        self.mox.ReplayAll()

        cmdhandler = CommandHandler(mock_client)
        self.assertTrue(cmdhandler.presence_control(mock_stanza))
        
    def test_parse_body(self):
        """ Test the default message body parsing. """
        mock_body = self.mox.CreateMockAnything()
        mock_client = self.mox.CreateMockAnything()
        self.mox.StubOutWithMock(CommandHandler, "__init__")

        CommandHandler.__init__(mock_client)

        self.mox.ReplayAll()

        cmdhandler = CommandHandler(mock_client)
        self.assertEqual(mock_body, cmdhandler.parse_body(mock_body))

    def test_parse_none_body(self):
        """ Ensure proper behavior when parsing a nonexisting message body. """
        mock_client = self.mox.CreateMockAnything()
        self.mox.StubOutWithMock(CommandHandler, "__init__")

        CommandHandler.__init__(mock_client)

        self.mox.ReplayAll()

        cmdhandler = CommandHandler(mock_client)
        self.assertEqual(None, cmdhandler.parse_body(None))

    def test_do_command_no_args(self):
        """ Test handling of commands with no arguments. """
        mock_command = self.mox.CreateMockAnything()
        mock_client = self.mox.CreateMockAnything()
        self.mox.StubOutWithMock(CommandHandler, "__init__")

        CommandHandler.__init__(mock_client)

        self.mox.ReplayAll()

        cmdhandler = CommandHandler(mock_client)
        cmdhandler.do_command(mock_command)

    def test_do_command(self):
        """ Test handling of commands with arguments. """
        mock_command = self.mox.CreateMockAnything()
        mock_args = self.mox.CreateMockAnything()
        mock_client = self.mox.CreateMockAnything()
        self.mox.StubOutWithMock(CommandHandler, "__init__")

        CommandHandler.__init__(mock_client)

        self.mox.ReplayAll()

        cmdhandler = CommandHandler(mock_client)
        cmdhandler.do_command(mock_command, mock_args)

    def test_do_command_no_command_no_args(self):
        """ Ensure proper behavior when when a None command. """
        mock_client = self.mox.CreateMockAnything()
        self.mox.StubOutWithMock(CommandHandler, "__init__")

        CommandHandler.__init__(mock_client)

        self.mox.ReplayAll()

        cmdhandler = CommandHandler(mock_client)
        cmdhandler.do_command(None)


class RestrictedCommandHandlerTest(mox.MoxTestBase):
    """ Test cases that tests the RestrictedCommandHandler type. """
    def test_parse_body_command_in_set_no_args(self):
        """ Test for an allowed command without arguments. """
        command = "foobar"
        args = None
        hlp = "command help"

        command_set = [(command, args, hlp)]

        response = "a response"

        self.mox.StubOutWithMock(RestrictedCommandHandler, "__init__")
        self.mox.StubOutWithMock(RestrictedCommandHandler, "do_command")
        self.mox.StubOutWithMock(configuration.commands, "restricted_set")

        RestrictedCommandHandler.__init__()
        configuration.commands.restricted_set().AndReturn(command_set)
        RestrictedCommandHandler.do_command(command, args).AndReturn(response)

        self.mox.ReplayAll()

        restricted_handler = RestrictedCommandHandler()
        self.assertEquals(response, restricted_handler.parse_body(command))

    def test_parse_body_command_in_set_args(self):
        """ Test for an allowed command with arguments. """
        command = "foobar"
        args = "some command arguments"
        hlp = "command help"

        command_set = [(command, args, hlp)]

        response = "a response"

        self.mox.StubOutWithMock(RestrictedCommandHandler, "__init__")
        self.mox.StubOutWithMock(RestrictedCommandHandler, "do_command")
        self.mox.StubOutWithMock(configuration.commands, "restricted_set")

        RestrictedCommandHandler.__init__()
        configuration.commands.restricted_set().AndReturn(command_set)
        RestrictedCommandHandler.do_command(command, args).AndReturn(response)

        self.mox.ReplayAll()

        restricted_handler = RestrictedCommandHandler()
        self.assertEquals(response, restricted_handler.parse_body(command))

    def test_parse_body_disallowed_command(self):
        """ Test for a disallowed command with some arguments. """
        command = "foobar"
        args = "some command arguments"
        hlp = "command help"

        command_set = [(command, args, hlp)]

        self.mox.StubOutWithMock(RestrictedCommandHandler, "__init__")
        self.mox.StubOutWithMock(configuration.commands, "restricted_set")

        RestrictedCommandHandler.__init__()
        configuration.commands.restricted_set().AndReturn(command_set)

        self.mox.ReplayAll()

        restricted_handler = RestrictedCommandHandler()
        self.assertEquals(None,
                restricted_handler.parse_body("disallowed command"))

    def test_parse_body_help_existing_command(self):
        """ Test the help function for an existing command. """
        command = "foobar"
        args = "some command arguments"
        hlp = "command help"

        command_set = [(command, args, hlp)]

        self.mox.StubOutWithMock(RestrictedCommandHandler, "__init__")
        self.mox.StubOutWithMock(configuration.commands, "restricted_set")

        RestrictedCommandHandler.__init__()
        configuration.commands.restricted_set().AndReturn(command_set)
        configuration.commands.restricted_set().AndReturn(command_set)
        configuration.commands.restricted_set().AndReturn(command_set)
        configuration.commands.restricted_set().AndReturn(command_set)

        self.mox.ReplayAll()

        restricted_handler = RestrictedCommandHandler()
        self.assertEquals("foobar - command help",
                restricted_handler.parse_body("help foobar"))
        self.assertEquals("foobar - command help",
                restricted_handler.parse_body("help	foobar"))
        self.assertEquals("foobar - command help",
                restricted_handler.parse_body("help	foobar	"))
        self.assertEquals("foobar - command help",
                restricted_handler.parse_body("help foobar "))

    def test_parse_body_help_nonexisting_command(self):
        """ Test the help function for a nonexisting command. """
        command = "foobar"
        args = "some command arguments"
        hlp = "command help"

        command_set = [(command, args, hlp)]

        self.mox.StubOutWithMock(RestrictedCommandHandler, "__init__")
        self.mox.StubOutWithMock(configuration.commands, "restricted_set")

        RestrictedCommandHandler.__init__()
        configuration.commands.restricted_set().AndReturn(command_set)

        self.mox.ReplayAll()

        restricted_handler = RestrictedCommandHandler()
        self.assertEquals(None, restricted_handler.parse_body("help spam"))

    def test_parse_body_empty_body(self):
        """ Ensure proper behavior on a None command. """
        self.mox.StubOutWithMock(RestrictedCommandHandler, "__init__")

        RestrictedCommandHandler.__init__()

        self.mox.ReplayAll()

        restricted_handler = RestrictedCommandHandler()
        self.assertEquals(None, restricted_handler.parse_body(None))

    def test_do_command_bye(self):
        """ Test executing the bye command. """
        command = "bye"

        client_mock = self.mox.CreateMockAnything()
        mock_stream = self.mox.CreateMockAnything()

        client_mock.get_stream().AndReturn(mock_stream)
        mock_stream.send(mox.IgnoreArg())
        client_mock.disconnect()

        self.mox.ReplayAll()

        restricted_handler = RestrictedCommandHandler()
    
        self.assertEquals(u"terminating", restricted_handler.do_command(command))

    def test_do_command_no_args(self):
        """ Test executing a command without arguments. """
        command = "ls"
        args = None

        method_args = [command]

        response = "foobar"

        self.mox.StubOutWithMock(RestrictedCommandHandler, "make_syscall")

        RestrictedCommandHandler.make_syscall(method_args).AndReturn(response)

        self.mox.ReplayAll()

        restricted_handler = RestrictedCommandHandler()
        self.assertEquals(response,
                restricted_handler.do_command(command, args))

    def test_do_command_args(self):
        """ Test executing a command with arguments. """
        command = "ls"
        args = "-al"

        method_args = [command]
        method_args.extend(args)

        response = "foobar"

        self.mox.StubOutWithMock(RestrictedCommandHandler, "make_syscall")

        RestrictedCommandHandler.make_syscall(method_args).AndReturn(response)

        self.mox.ReplayAll()

        restricted_handler = RestrictedCommandHandler()
        self.assertEquals(response,
                restricted_handler.do_command(command, args))

    def test_do_command_popen_raises(self):
        """ Ensure proper behavior when Popen raises an assertion upon command
            execution. """
        command = "ls"
        args = "-al"

        method_args = [command]
        method_args.extend(args)

        self.mox.StubOutWithMock(RestrictedCommandHandler, "make_syscall")

        RestrictedCommandHandler.make_syscall(method_args).AndRaise(
                OSError(2, None, 'File not found'))

        self.mox.ReplayAll()

        restricted_handler = RestrictedCommandHandler()
        self.assertEqual(type(""),
                type(restricted_handler.do_command(command, args)))


class UnsafeCommandHandlerTest(mox.MoxTestBase):
    """ Provides test cases for the UnsafeCommandHandler type. """
    def test_parse_body(self):
        """ Test parsing of a message body. """
        body = "c"

        args = body.split()
        command = args.pop(0)

        response = "a response"

        self.mox.StubOutWithMock(UnsafeCommandHandler, "do_command")

        UnsafeCommandHandler.do_command(command, args).AndReturn(response)

        self.mox.ReplayAll()

        unsafe_handler = UnsafeCommandHandler()
        self.assertEquals(response, unsafe_handler.parse_body(body))


    def test_parse_body_empty_body(self):
        """ Test parsing of an empty message body. """
        body = None

        response = None

        self.mox.ReplayAll()

        unsafe_handler = UnsafeCommandHandler()
        self.assertEquals(response, unsafe_handler.parse_body(body))


if "__main__" == __name__:
    unittest.main()
