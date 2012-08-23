#!/usr/bin/python

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

""" This module tests the credentials module. """

# we import the builtin module here, since we need to refer to it explicitly,
# rather than by __builtins__ when we overload open and raw_input, since
# __builtins__ refers to the module when this script is a main script, and to a
# dict when this script is not a main script..
import __builtin__
import sys
import os

sys.path.append(os.path.abspath(".."))

import mox

import credentials

import unittest

class CredentialsTest(mox.MoxTestBase):
    """ Testing the credentials module """

    def test_get_credentials(self):
        """ Ensure proper behavior when the file-like credentials object
            containins a newline-separated username-password pair. """

        username, password = ("username@jabber.org", "password")

        credentials_file = ".credentials"


        self.mox.StubOutWithMock(__builtin__, "open")
        mock_file = self.mox.CreateMockAnything()

        open(credentials_file).AndReturn(mock_file)
        mock_file.readline().AndReturn(username)
        mock_file.readline().AndReturn(password)

        self.mox.ReplayAll()

        self.assertEquals((username, password),
                credentials.get_credentials(credentials_file))

    def test_get_credentials_nonexisting_file(self):
        """ In the credentials file does not exist, the user should be
            prompted for the credentials, and the input written to the
            credentials file. """

        username, password = ("username@jabber.org", "password")

        credentials_file = ".credentials"


        self.mox.StubOutWithMock(__builtin__, "open")
        self.mox.StubOutWithMock(__builtin__, "raw_input")
        mock_file = self.mox.CreateMockAnything()

        open(credentials_file).AndRaise(IOError)
        raw_input(mox.IgnoreArg()).AndReturn(username)
        raw_input(mox.IgnoreArg()).AndReturn(password)

        open(credentials_file, 'w').AndReturn(mock_file)
        mock_file.writelines([username, "\n", password, "\n"])
        mock_file.close()

        self.mox.ReplayAll()

        self.assertEquals((username, password),
                credentials.get_credentials(credentials_file))


    def test_get_credentials_incomplete_credentials(self):
        """ If the credentials file does not contain both username
            and password, the user should be prompted for the information, and
            any contents of the credentials file shall be overwritten. """

        ignored_username, none_password = ("foo@bar", "")
        username, password = ("username@jabber.org", "password")

        credentials_file = ".credentials"


        self.mox.StubOutWithMock(__builtin__, "open")
        self.mox.StubOutWithMock(__builtin__, "raw_input")
        mock_file = self.mox.CreateMockAnything()

        open(credentials_file).AndReturn(mock_file)
        mock_file.readline().AndReturn(ignored_username)
        mock_file.readline().AndReturn(none_password)

        raw_input(mox.IgnoreArg()).AndReturn(username)
        raw_input(mox.IgnoreArg()).AndReturn(password)

        open(credentials_file, 'w').AndReturn(mock_file)
        mock_file.writelines([username, "\n", password, "\n"])
        mock_file.close()

        self.mox.ReplayAll()

        self.assertEquals((username, password),
                credentials.get_credentials(credentials_file))


if "__main__" == __name__:
    unittest.main()
