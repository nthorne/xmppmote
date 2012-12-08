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

""" This module tests the updatenotifyer module. """

import sys
import os

sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("../../.."))

import mox
import unittest

from bot.client import Client
from updatenotifyer import UpdateNotifyer
from stableupdater import StableUpdater
from bleedingedgeupdater import BleedingEdgeUpdater

import threading

class UpdateNotifyerTest(mox.MoxTestBase):
    """ Provides test cases for the UpdateNotifyer type. """
    __repo = "foo/bar"
    __remote_url = "not a real url"

    def test_init_stable_update(self):
        """ Make sure that the StableUpdater is used if no updater is detailed.
        """

        self.mox.StubOutWithMock(StableUpdater, "__init__")

        StableUpdater.__init__(self.__repo)

        self.mox.ReplayAll()

        notifyer = UpdateNotifyer(self.__repo)

    def test_init_bleeding_egde_update(self):
        """ Make sure that the BleedingEdgeUpdater is used, if detailed. """

        self.mox.StubOutWithMock(BleedingEdgeUpdater, "__init__")

        BleedingEdgeUpdater.__init__(self.__repo)

        self.mox.ReplayAll()

        notifyer = UpdateNotifyer(self.__repo, True)

    def test_start(self):
        """ Make sure that a timer for the proper interval is started when the
        UpdateNotifyer.start method is called. """

        mock_timer = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(StableUpdater, "__init__")
        self.mox.StubOutWithMock(threading, "Timer")

        StableUpdater.__init__(self.__repo)

        threading.Timer(3600, mox.IgnoreArg()).AndReturn(mock_timer)
        mock_timer.start()

        self.mox.ReplayAll()

        notifyer = UpdateNotifyer(self.__repo)
        notifyer.start()

    def test_stop(self):
        """ Ensure that the timer is cancelled if UpdateNotifyer.stop is called.
        """

        mock_timer = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(StableUpdater, "__init__")
        self.mox.StubOutWithMock(threading, "Timer")

        StableUpdater.__init__(self.__repo)

        threading.Timer(3600, mox.IgnoreArg()).AndReturn(mock_timer)
        mock_timer.start()

        mock_timer.cancel()

        self.mox.ReplayAll()

        notifyer = UpdateNotifyer(self.__repo)
        notifyer.start()
        notifyer.stop()

    def test_timeout_update_available(self):
        """ Make sure that we get a status update if the selected updater
        indicates that an update is available. """

        mock_timer = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(StableUpdater, "__init__")
        self.mox.StubOutWithMock(StableUpdater, "check")
        self.mox.StubOutWithMock(StableUpdater, "get_update_version")
        self.mox.StubOutWithMock(threading, "Timer")
        self.mox.StubOutWithMock(threading.Thread, "start")
        self.mox.StubOutWithMock(Client, "change_status")

        StableUpdater.__init__(self.__repo)

        threading.Timer(3600, mox.IgnoreArg()).AndReturn(mock_timer)
        mock_timer.start()

        StableUpdater.check().AndReturn(True)
        StableUpdater.get_update_version().AndReturn("1.0")
        Client.change_status(mox.IgnoreArg())

        threading.Timer(3600, mox.IgnoreArg()).AndReturn(mock_timer)
        mock_timer.start()

        self.mox.ReplayAll()

        notifyer = UpdateNotifyer(self.__repo)
        notifyer.start()
        notifyer.timeout()

    def test_timeout_no_update_available(self):
        """ Make sure that nothing happens (i.e. no status updates) when the
        updater indicates that there are no updates available. """

        mock_timer = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(StableUpdater, "__init__")
        self.mox.StubOutWithMock(StableUpdater, "check")
        self.mox.StubOutWithMock(threading, "Timer")
        self.mox.StubOutWithMock(threading.Thread, "start")
        self.mox.StubOutWithMock(Client, "change_status")

        StableUpdater.__init__(self.__repo)

        threading.Timer(3600, mox.IgnoreArg()).AndReturn(mock_timer)
        mock_timer.start()

        StableUpdater.check().AndReturn(False)

        threading.Timer(3600, mox.IgnoreArg()).AndReturn(mock_timer)
        mock_timer.start()

        self.mox.ReplayAll()

        notifyer = UpdateNotifyer(self.__repo)
        notifyer.start()
        notifyer.timeout()

    def test_timeout_update_still_available(self):
        """ Make sure that we do not spam with software update notices. Once
        there has been an update notification, updates found thereafter should
        not be indicated. """

        mock_timer = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(StableUpdater, "__init__")
        self.mox.StubOutWithMock(StableUpdater, "check")
        self.mox.StubOutWithMock(StableUpdater, "get_update_version")
        self.mox.StubOutWithMock(threading, "Timer")
        self.mox.StubOutWithMock(threading.Thread, "start")
        self.mox.StubOutWithMock(Client, "change_status")

        StableUpdater.__init__(self.__repo)

        threading.Timer(3600, mox.IgnoreArg()).AndReturn(mock_timer)
        mock_timer.start()

        StableUpdater.check().AndReturn(True)
        Client.change_status(mox.IgnoreArg())

        threading.Timer(3600, mox.IgnoreArg()).AndReturn(mock_timer)
        mock_timer.start()

        StableUpdater.check().AndReturn(True)
        StableUpdater.get_update_version().AndReturn("1.0")

        threading.Timer(3600, mox.IgnoreArg()).AndReturn(mock_timer)
        mock_timer.start()

        self.mox.ReplayAll()

        notifyer = UpdateNotifyer(self.__repo)
        notifyer.start()
        notifyer.timeout()
        notifyer.timeout()

    def test_toggle_update_availability(self):
        """ Make sure that the update indicaiton is reset if an update all of a
        sudden is not available. """

        mock_timer = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(StableUpdater, "__init__")
        self.mox.StubOutWithMock(StableUpdater, "check")
        self.mox.StubOutWithMock(StableUpdater, "get_update_version")
        self.mox.StubOutWithMock(threading, "Timer")
        self.mox.StubOutWithMock(threading.Thread, "start")
        self.mox.StubOutWithMock(Client, "change_status")

        StableUpdater.__init__(self.__repo)

        threading.Timer(3600, mox.IgnoreArg()).AndReturn(mock_timer)
        mock_timer.start()

        StableUpdater.check().AndReturn(True)
        StableUpdater.get_update_version().AndReturn("1.0")
        Client.change_status(mox.IgnoreArg())

        threading.Timer(3600, mox.IgnoreArg()).AndReturn(mock_timer)
        mock_timer.start()

        StableUpdater.check().AndReturn(True)
        StableUpdater.get_update_version().AndReturn("1.0")

        threading.Timer(3600, mox.IgnoreArg()).AndReturn(mock_timer)
        mock_timer.start()

        StableUpdater.check().AndReturn(False)

        threading.Timer(3600, mox.IgnoreArg()).AndReturn(mock_timer)
        mock_timer.start()

        StableUpdater.check().AndReturn(True)
        Client.change_status(mox.IgnoreArg())

        threading.Timer(3600, mox.IgnoreArg()).AndReturn(mock_timer)
        mock_timer.start()

        self.mox.ReplayAll()

        notifyer = UpdateNotifyer(self.__repo)
        notifyer.start()
        notifyer.timeout()
        notifyer.timeout()
        notifyer.timeout()
        notifyer.timeout()


if "__main__" == __name__:
    unittest.main()
