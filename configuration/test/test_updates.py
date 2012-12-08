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

""" This module provides unit tests for the updates module. """

import sys
import os

sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("../.."))

import mox
import unittest

import threading

from updates import *
from ConfigParser import SafeConfigParser
from ConfigParser import NoSectionError
from ConfigParser import NoOptionError
from configurationparser import ConfigurationParser

from lib.guf.updatenotifyer import UpdateNotifyer
from lib.guf.stableupdater import StableUpdater
from lib.guf.bleedingedgeupdater import BleedingEdgeUpdater

class GetUpdateHandlerTest(mox.MoxTestBase):
    """ Provides test cases for the get_update_handler function. """

    def test_notify_on_stable_interval(self):
        """ Make sure that an UpdateNotifyer, with a StableUpdater, for the
        configured interval is constructed when the configuration data indicates
        so. """

        mock_file = self.mox.CreateMockAnything()
        mock_timer = self.mox.CreateMockAnything()
        mock_file.closed = False
        mock_file.name = "foobar"

        action, model, interval = ("notify", "stable", "43200")

        self.mox.StubOutWithMock(SafeConfigParser, "get")
        self.mox.StubOutWithMock(StableUpdater, "__init__")
        self.mox.StubOutWithMock(threading, "Timer")

        config = ConfigurationParser()
        config.parse(mock_file)
        config.get("updates", "action").AndReturn(action)
        config.get("updates", "model").AndReturn(model)
        config.get("updates", "interval").AndReturn(interval)

        StableUpdater.__init__(REPO)

        threading.Timer(int(interval), mox.IgnoreArg()).AndReturn(mock_timer)
        mock_timer.start()

        self.mox.ReplayAll()

        update_handler = get_update_handler()
        update_handler.start()

        self.assertTrue(isinstance(update_handler, UpdateNotifyer))

    def test_notify_on_stable_no_interval(self):
        """ Make sure that the default interval is used for the StableUpdater,
        if no default interval is given in the configuration. """

        mock_file = self.mox.CreateMockAnything()
        mock_timer = self.mox.CreateMockAnything()
        mock_file.closed = False
        mock_file.name = "foobar"

        action, model = ("notify", "stable")

        self.mox.StubOutWithMock(SafeConfigParser, "get")
        self.mox.StubOutWithMock(StableUpdater, "__init__")
        self.mox.StubOutWithMock(threading, "Timer")

        config = ConfigurationParser()
        config.parse(mock_file)
        config.get("updates", "action").AndReturn(action)
        config.get("updates", "model").AndReturn(model)
        config.get("updates", "interval").AndRaise(NoOptionError("updates",
                                                                 "interval"))

        StableUpdater.__init__(REPO)

        threading.Timer(DEFAULT_INTERVAL,
                        mox.IgnoreArg()).AndReturn(mock_timer)
        mock_timer.start()

        self.mox.ReplayAll()

        update_handler = get_update_handler()
        update_handler.start()

        self.assertTrue(isinstance(update_handler, UpdateNotifyer))

    def test_notify_on_bleeding_edge_interval(self):
        """ Make sure that a BleedingEdgeUpdater is constructed if the
        configuration details it. """

        mock_file = self.mox.CreateMockAnything()
        mock_timer = self.mox.CreateMockAnything()
        mock_file.closed = False
        mock_file.name = "foobar"

        action, model, interval = ("notify", "bleeding", "43200")

        self.mox.StubOutWithMock(SafeConfigParser, "get")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "__init__")
        self.mox.StubOutWithMock(threading, "Timer")

        config = ConfigurationParser()
        config.parse(mock_file)
        config.get("updates", "action").AndReturn(action)
        config.get("updates", "model").AndReturn(model)
        config.get("updates", "interval").AndReturn(interval)

        BleedingEdgeUpdater.__init__(REPO)

        threading.Timer(int(interval), mox.IgnoreArg()).AndReturn(mock_timer)
        mock_timer.start()

        self.mox.ReplayAll()

        update_handler = get_update_handler()
        update_handler.start()

        self.assertTrue(isinstance(update_handler, UpdateNotifyer))

    def test_notify_on_bleeding_edge_no_interval(self):
        """ Make sure that the default interval is used for the
        BleedingEdgeUpdater, as for the StableUpdater. """

        mock_file = self.mox.CreateMockAnything()
        mock_timer = self.mox.CreateMockAnything()
        mock_file.closed = False
        mock_file.name = "foobar"

        action, model = ("notify", "bleeding")

        self.mox.StubOutWithMock(SafeConfigParser, "get")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "__init__")
        self.mox.StubOutWithMock(threading, "Timer")

        config = ConfigurationParser()
        config.parse(mock_file)
        config.get("updates", "action").AndReturn(action)
        config.get("updates", "model").AndReturn(model)
        config.get("updates", "interval").AndRaise(NoOptionError("updates",
                                                                 "interval"))

        BleedingEdgeUpdater.__init__(REPO)

        threading.Timer(DEFAULT_INTERVAL,
                        mox.IgnoreArg()).AndReturn(mock_timer)
        mock_timer.start()

        self.mox.ReplayAll()

        update_handler = get_update_handler()
        update_handler.start()

        self.assertTrue(isinstance(update_handler, UpdateNotifyer))

    def test_no_update_section(self):
        """ If there is no configured update section, no update handler should
        be constructed. """

        mock_file = self.mox.CreateMockAnything()
        mock_file.closed = False
        mock_file.name = "foobar"

        self.mox.StubOutWithMock(SafeConfigParser, "get")
        self.mox.StubOutWithMock(StableUpdater, "__init__")
        self.mox.StubOutWithMock(threading, "Timer")

        config = ConfigurationParser()
        config.parse(mock_file)
        config.get("updates", "action").AndRaise(NoSectionError("updates"))

        self.mox.ReplayAll()

        self.assertEqual(None, get_update_handler())

    def test_update_section_no_action(self):
        """ If there is no configured action, no update handler should be
        constructed. """

        mock_file = self.mox.CreateMockAnything()
        mock_file.closed = False
        mock_file.name = "foobar"

        self.mox.StubOutWithMock(SafeConfigParser, "get")
        self.mox.StubOutWithMock(StableUpdater, "__init__")

        config = ConfigurationParser()
        config.parse(mock_file)
        config.get("updates", "action").AndRaise(NoOptionError("updates",
                                                               "action"))
        self.mox.ReplayAll()

        self.assertEqual(None, get_update_handler())

    def test_update_section_unknown_action(self):
        """ If the configured action string does not match a known action, an
        UnknownAction exception should be raised. """

        mock_file = self.mox.CreateMockAnything()
        mock_file.closed = False
        mock_file.name = "foobar"

        action, model, interval = ("nottify", "stable", "43200")

        self.mox.StubOutWithMock(SafeConfigParser, "get")
        self.mox.StubOutWithMock(StableUpdater, "__init__")

        config = ConfigurationParser()
        config.parse(mock_file)
        config.get("updates", "action").AndReturn(action)
        config.get("updates", "model").AndReturn(model)
        config.get("updates", "interval").AndReturn(interval)
        self.mox.ReplayAll()

        self.assertRaises(UnknownAction, get_update_handler)

    def test_update_section_unknown_model(self):
        """ If the configured model string does not match a known model, an
        UnknownModel exception should be raised. """

        mock_file = self.mox.CreateMockAnything()
        mock_file.closed = False
        mock_file.name = "foobar"

        action, model, interval = ("notify", "stabble", "43200")

        self.mox.StubOutWithMock(SafeConfigParser, "get")
        self.mox.StubOutWithMock(StableUpdater, "__init__")

        config = ConfigurationParser()
        config.parse(mock_file)
        config.get("updates", "action").AndReturn(action)
        config.get("updates", "model").AndReturn(model)
        config.get("updates", "interval").AndReturn(interval)
        self.mox.ReplayAll()

        self.assertRaises(UnknownModel, get_update_handler)

    def test_notify_on_stable_malformed_interval(self):
        """ A malformed interval in the configuration (i.e. non-integer) should
        result in the default interval being used. """

        mock_file = self.mox.CreateMockAnything()
        mock_timer = self.mox.CreateMockAnything()
        mock_file.closed = False
        mock_file.name = "foobar"

        action, model, interval = ("notify", "stable", "FOO")

        self.mox.StubOutWithMock(SafeConfigParser, "get")
        self.mox.StubOutWithMock(StableUpdater, "__init__")
        self.mox.StubOutWithMock(threading, "Timer")

        config = ConfigurationParser()
        config.parse(mock_file)
        config.get("updates", "action").AndReturn(action)
        config.get("updates", "model").AndReturn(model)
        config.get("updates", "interval").AndReturn(interval)

        StableUpdater.__init__(REPO)

        threading.Timer(DEFAULT_INTERVAL, mox.IgnoreArg()).AndReturn(mock_timer)
        mock_timer.start()

        self.mox.ReplayAll()

        update_handler = get_update_handler()
        update_handler.start()

        self.assertTrue(isinstance(update_handler, UpdateNotifyer))


if "__main__" == __name__:
    unittest.main()
