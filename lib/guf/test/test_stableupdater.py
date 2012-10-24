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

""" This module tests the stableupdater module. """

import sys
import os

sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("../../.."))

import mox
import unittest

import urllib2
import json
import base64

import version

from stableupdater import StableUpdater


class StableUpdaterTest(mox.MoxTestBase):
    """ This type provides test cases for StableUpdater. """

    __repo = "foo/bar"
    __remote_url = "there is no url"
    __mocked_remote_version = "1.3.3.7"
    __mock_file_with_proper_version = """
# This is a properly formed version file.

version = %s
""" % __mocked_remote_version
    __mock_file_without_version = """
# This one just contains
# a couple of lines of
# comments.
"""
    __mock_file_with_multiple_versions = """
# .. and this one contains a whole bunch of version definitions
version = "1.3.3.7"
version = "1.3.3.8"
"""
    __mock_file_with_malformed_version = """
version =
"""

    def test_github_has_new_version(self):
        """ Ensure proper behavior when we receive a remote version file that
        details a version newer than the current one. """

        version.version = "0.0"

        mock_response = self.mox.CreateMockAnything()
        mock_html = self.mox.CreateMockAnything()
        mock_json_dict = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(urllib2, "urlopen")
        self.mox.StubOutWithMock(json, "loads")
        self.mox.StubOutWithMock(base64, "b64decode")

        urllib2.urlopen(self.__remote_url).AndReturn(mock_response)
        mock_response.read().AndReturn(mock_html)

        json.loads(mock_html).AndReturn(mock_json_dict)

        base64.b64decode(mock_json_dict["content"].AndReturn(
            self.__mock_file_with_proper_version)).AndReturn(
                self.__mock_file_with_proper_version)

        self.mox.ReplayAll()

        stable_updater = StableUpdater(self.__repo, self.__remote_url)

        self.assertTrue(stable_updater.check())
        self.assertEquals(self.__mocked_remote_version,
                          stable_updater.remote_version)

    def test_github_does_not_have_new_version(self):
        """ Make sure that no update is indicated if the remote version euqals
        the local one. """

        version.version = self.__mocked_remote_version

        mock_response = self.mox.CreateMockAnything()
        mock_html = self.mox.CreateMockAnything()
        mock_json_dict = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(urllib2, "urlopen")
        self.mox.StubOutWithMock(json, "loads")
        self.mox.StubOutWithMock(base64, "b64decode")

        urllib2.urlopen(self.__remote_url).AndReturn(mock_response)
        mock_response.read().AndReturn(mock_html)

        json.loads(mock_html).AndReturn(mock_json_dict)

        base64.b64decode(mock_json_dict["content"].AndReturn(
            self.__mock_file_with_proper_version)).AndReturn(
                self.__mock_file_with_proper_version)

        self.mox.ReplayAll()

        stable_updater = StableUpdater(self.__repo, self.__remote_url)

        self.assertTrue(not stable_updater.check())
        self.assertEquals(version.version,
                          stable_updater.remote_version)

    def test_github_not_responding(self):
        """ Make sure that the updater handles unresponsive remote servers
        properly. """

        version.version = "0.0"

        self.mox.StubOutWithMock(urllib2, "urlopen")

        urllib2.urlopen(self.__remote_url).AndRaise(urllib2.URLError("Timeout"))

        self.mox.ReplayAll()

        stable_updater = StableUpdater(self.__repo, self.__remote_url)

        self.assertTrue(not stable_updater.check())
        self.assertEquals(None, stable_updater.remote_version)

    def test_github_response_no_content(self):
        """ Make sure that a request response without any JSON content is
        handled gracefully. """

        version.version = "0.0"

        mock_response = self.mox.CreateMockAnything()
        mock_html = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(urllib2, "urlopen")
        self.mox.StubOutWithMock(json, "loads")

        urllib2.urlopen(self.__remote_url).AndReturn(mock_response)
        mock_response.read().AndReturn(mock_html)

        json.loads(mock_html).AndRaise(ValueError("No JSON object"))

        self.mox.ReplayAll()

        stable_updater = StableUpdater(self.__repo, self.__remote_url)

        self.assertTrue(not stable_updater.check())
        self.assertEquals(None, stable_updater.remote_version)

    def test_no_version_version_defined(self):
        """ Make sure that the updater handles an erroneous (missing) local
        version gracefully. """

        del version.version

        mock_response = self.mox.CreateMockAnything()
        mock_html = self.mox.CreateMockAnything()
        mock_json_dict = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(urllib2, "urlopen")
        self.mox.StubOutWithMock(json, "loads")
        self.mox.StubOutWithMock(base64, "b64decode")

        urllib2.urlopen(self.__remote_url).AndReturn(mock_response)
        mock_response.read().AndReturn(mock_html)

        json.loads(mock_html).AndReturn(mock_json_dict)

        base64.b64decode(mock_json_dict["content"].AndReturn(
            self.__mock_file_with_proper_version)).AndReturn(
                self.__mock_file_with_proper_version)

        self.mox.ReplayAll()

        stable_updater = StableUpdater(self.__repo, self.__remote_url)

        self.assertTrue(not stable_updater.check())

    def test_no_remote_version(self):
        """ If there is no remote version to be found, ensure that no updates
        are indicated. """

        version.version = "0.0"

        mock_response = self.mox.CreateMockAnything()
        mock_html = self.mox.CreateMockAnything()
        mock_json_dict = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(urllib2, "urlopen")
        self.mox.StubOutWithMock(json, "loads")
        self.mox.StubOutWithMock(base64, "b64decode")

        urllib2.urlopen(self.__remote_url).AndReturn(mock_response)
        mock_response.read().AndReturn(mock_html)

        json.loads(mock_html).AndReturn(mock_json_dict)

        base64.b64decode(mock_json_dict["content"].AndReturn(
            self.__mock_file_without_version)).AndReturn(
                self.__mock_file_without_version)

        self.mox.ReplayAll()

        stable_updater = StableUpdater(self.__repo, self.__remote_url)

        self.assertTrue(not stable_updater.check())
        self.assertEquals(None, stable_updater.remote_version)

    def test_mutiple_remote_versions(self):
        """ In case the remote version file contains multiple version
        definitions, make sure that no update is indicated. """

        version.version = "0.0"

        mock_response = self.mox.CreateMockAnything()
        mock_html = self.mox.CreateMockAnything()
        mock_json_dict = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(urllib2, "urlopen")
        self.mox.StubOutWithMock(json, "loads")
        self.mox.StubOutWithMock(base64, "b64decode")

        urllib2.urlopen(self.__remote_url).AndReturn(mock_response)
        mock_response.read().AndReturn(mock_html)

        json.loads(mock_html).AndReturn(mock_json_dict)

        base64.b64decode(mock_json_dict["content"].AndReturn(
            self.__mock_file_with_multiple_versions)).AndReturn(
                self.__mock_file_with_multiple_versions)

        self.mox.ReplayAll()

        stable_updater = StableUpdater(self.__repo, self.__remote_url)

        self.assertTrue(not stable_updater.check())
        self.assertEquals(None, stable_updater.remote_version)

    def test_empty_response_read(self):
        """ Empty HTML/JSON should be handled gracefully. """

        version.version = "0.0"

        mock_response = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(urllib2, "urlopen")
        self.mox.StubOutWithMock(json, "loads")
        self.mox.StubOutWithMock(base64, "b64decode")

        urllib2.urlopen(self.__remote_url).AndReturn(mock_response)
        mock_response.read().AndReturn("")

        self.mox.ReplayAll()

        stable_updater = StableUpdater(self.__repo, self.__remote_url)

        self.assertTrue(not stable_updater.check())
        self.assertEquals(None, stable_updater.remote_version)

    def test_malformed_base64_string(self):
        """ Make sure malformed base64 is handled gracefully. """

        version.version = "0.0"

        mock_response = self.mox.CreateMockAnything()
        mock_html = self.mox.CreateMockAnything()
        mock_json_dict = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(urllib2, "urlopen")
        self.mox.StubOutWithMock(json, "loads")
        self.mox.StubOutWithMock(base64, "b64decode")

        urllib2.urlopen(self.__remote_url).AndReturn(mock_response)
        mock_response.read().AndReturn(mock_html)

        json.loads(mock_html).AndReturn(mock_json_dict)

        base64.b64decode(mock_json_dict["content"].AndReturn(
            self.__mock_file_with_proper_version)).AndRaise(
                TypeError("Invalid Base64"))

        self.mox.ReplayAll()

        stable_updater = StableUpdater(self.__repo, self.__remote_url)

        self.assertTrue(not stable_updater.check())
        self.assertEquals(None, stable_updater.remote_version)

    def test_invalid_url(self):
        """ Invalid URL should be handled gracefully. """

        version.version = "0.0"

        self.mox.StubOutWithMock(urllib2, "urlopen")

        urllib2.urlopen(self.__remote_url).AndRaise(
            ValueError("Unknown url type"))

        self.mox.ReplayAll()

        stable_updater = StableUpdater(self.__repo, self.__remote_url)

        self.assertTrue(not stable_updater.check())
        self.assertEquals(None, stable_updater.remote_version)

    def test_malformed_version_variable_definition(self):
        """ Malformed remote version variables should be handled gracefully.
        """

        version.version = self.__mocked_remote_version

        mock_response = self.mox.CreateMockAnything()
        mock_html = self.mox.CreateMockAnything()
        mock_json_dict = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(urllib2, "urlopen")
        self.mox.StubOutWithMock(json, "loads")
        self.mox.StubOutWithMock(base64, "b64decode")

        urllib2.urlopen(self.__remote_url).AndReturn(mock_response)
        mock_response.read().AndReturn(mock_html)

        json.loads(mock_html).AndReturn(mock_json_dict)

        base64.b64decode(mock_json_dict["content"].AndReturn(
            self.__mock_file_with_malformed_version)).AndReturn(
                self.__mock_file_with_malformed_version)

        self.mox.ReplayAll()

        stable_updater = StableUpdater(self.__repo, self.__remote_url)

        self.assertTrue(not stable_updater.check())
        self.assertEquals(None, stable_updater.remote_version)

    def test_version_check_fails_second_time(self):
        """ If a second version check fails, make sure that the update
        availability statuses reflects that. """

        version.version = "0.0"

        mock_response = self.mox.CreateMockAnything()
        mock_html = self.mox.CreateMockAnything()
        mock_json_dict = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(urllib2, "urlopen")
        self.mox.StubOutWithMock(json, "loads")
        self.mox.StubOutWithMock(base64, "b64decode")

        urllib2.urlopen(self.__remote_url).AndReturn(mock_response)
        mock_response.read().AndReturn(mock_html)

        json.loads(mock_html).AndReturn(mock_json_dict)

        base64.b64decode(mock_json_dict["content"].AndReturn(
            self.__mock_file_with_proper_version)).AndReturn(
                self.__mock_file_with_proper_version)

        urllib2.urlopen(self.__remote_url).AndRaise(urllib2.URLError("Timeout"))

        self.mox.ReplayAll()

        stable_updater = StableUpdater(self.__repo, self.__remote_url)

        self.assertTrue(stable_updater.check())
        self.assertEquals(self.__mocked_remote_version,
                          stable_updater.remote_version)

        self.assertTrue(not stable_updater.check())
        self.assertEquals(None, stable_updater.remote_version)

    def test_github_has_old_version(self):
        """ Ensure proper behavior when we receive a remote version file that
        details a version older than the current one. """

        version.version = "1.3.3.8"

        mock_response = self.mox.CreateMockAnything()
        mock_html = self.mox.CreateMockAnything()
        mock_json_dict = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(urllib2, "urlopen")
        self.mox.StubOutWithMock(json, "loads")
        self.mox.StubOutWithMock(base64, "b64decode")

        urllib2.urlopen(self.__remote_url).AndReturn(mock_response)
        mock_response.read().AndReturn(mock_html)

        json.loads(mock_html).AndReturn(mock_json_dict)

        base64.b64decode(mock_json_dict["content"].AndReturn(
            self.__mock_file_with_proper_version)).AndReturn(
                self.__mock_file_with_proper_version)

        self.mox.ReplayAll()

        stable_updater = StableUpdater(self.__repo, self.__remote_url)

        self.assertTrue(not stable_updater.check())
        self.assertEquals(self.__mocked_remote_version,
                          stable_updater.remote_version)


if "__main__" == __name__:
    unittest.main()
