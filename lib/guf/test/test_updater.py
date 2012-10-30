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

""" This module tests the updater module. """

import __builtin__

import sys
import os

sys.path.append(os.path.abspath(".."))

import mox
import unittest

from updater import Updater

import urllib2

class UpdaterTest(mox.MoxTestBase):
    """ This type provides test cases for Updater. """ 

    __repo = "foo/bar"
    __tarball_filename = "random filename"
    __tarball_url = "url/%s" % __tarball_filename
    __update_dir = "a local folder"
    __content_string = "attachment; filename=%s" % __tarball_filename
    __target_filename = "%s/%s" % (__update_dir, __tarball_filename)

    def test_download_update(self):
        """ download_update should default to calling download_tarball. This
        allows for nifty override, e.g. pullin with Git by subtype. """

        self.mox.StubOutWithMock(Updater, "download_tarball")

        Updater.download_tarball()
        
        self.mox.ReplayAll()

        updater = Updater(self.__repo)
        updater.download_update()

    def test_download_tarball(self):
        """ download_tarball should download the tarball found at
        get_tarball_url, to get_target_directory """

        mock_resource = self.mox.CreateMockAnything()
        mock_file = self.mox.CreateMockAnything()
        mock_http_message = self.mox.CreateMockAnything()
        mock_contents = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(Updater, "get_tarball_url")
        self.mox.StubOutWithMock(urllib2, "urlopen")
        self.mox.StubOutWithMock(__builtin__, "open")
        self.mox.StubOutWithMock(os.path, "isdir")

        os.path.isdir(self.__update_dir).AndReturn(True)

        Updater.get_tarball_url(self.__repo).AndReturn(self.__tarball_url)
        urllib2.urlopen(self.__tarball_url).AndReturn(mock_resource)

        mock_resource.info().AndReturn(mock_http_message)
        mock_http_message.get("Content-Disposition").AndReturn(self.__content_string)

        __builtin__.open(self.__target_filename, "wb").AndReturn(mock_file)
        mock_file.__enter__().AndReturn(mock_file)
        mock_file.write(mock_resource.read().AndReturn(mock_contents))
        mock_file.__exit__(mox.IgnoreArg(), mox.IgnoreArg(), mox.IgnoreArg())

        self.mox.ReplayAll()

        updater = Updater(repo = self.__repo, update_dir = self.__update_dir)
        self.assertEquals(self.__target_filename, updater.download_tarball())

    def test_download_tarball_invalid_url(self):
        """ if urlopen raises URLError, None shall be returned from
        download_tarball. """

        self.mox.StubOutWithMock(Updater, "get_tarball_url")
        self.mox.StubOutWithMock(urllib2, "urlopen")
        self.mox.StubOutWithMock(os.path, "isdir")

        os.path.isdir(self.__update_dir).AndReturn(True)

        Updater.get_tarball_url(self.__repo).AndReturn(self.__tarball_url)
        urllib2.urlopen(self.__tarball_url).AndRaise(urllib2.URLError("Nah-ah"))

        self.mox.ReplayAll()

        updater = Updater(repo = self.__repo, update_dir = self.__update_dir)
        self.assertEquals(None, updater.download_tarball())

    def test_download_tarball_no_handler(self):
        """ if urlopen returns None (i.e. no handler), None shall be returned
        from download_tarball. """

        self.mox.StubOutWithMock(Updater, "get_tarball_url")
        self.mox.StubOutWithMock(urllib2, "urlopen")
        self.mox.StubOutWithMock(os.path, "isdir")

        os.path.isdir(self.__update_dir).AndReturn(True)

        Updater.get_tarball_url(self.__repo).AndReturn(self.__tarball_url)
        urllib2.urlopen(self.__tarball_url).AndReturn(None)

        self.mox.ReplayAll()

        updater = Updater(repo = self.__repo, update_dir = self.__update_dir)
        self.assertEquals(None, updater.download_tarball())

    def test_download_tarball_http_error(self):
        """ if urlopen raises HTTPError, None shall be returned from
        download_tarball. """

        self.mox.StubOutWithMock(Updater, "get_tarball_url")
        self.mox.StubOutWithMock(urllib2, "urlopen")
        self.mox.StubOutWithMock(os.path, "isdir")

        os.path.isdir(self.__update_dir).AndReturn(True)

        Updater.get_tarball_url(self.__repo).AndReturn(self.__tarball_url)
        urllib2.urlopen(self.__tarball_url).AndRaise(
            urllib2.HTTPError(self.__tarball_url, 404, "There is no url", None,
                              None))

        self.mox.ReplayAll()

        updater = Updater(repo = self.__repo, update_dir = self.__update_dir)
        self.assertEquals(None, updater.download_tarball())

    def test_download_tarball_download_directory_does_not_exist(self):
        """ if the folder in which the tarball is to be stored does not exist,
        it should be created. """

        mock_resource = self.mox.CreateMockAnything()
        mock_file = self.mox.CreateMockAnything()
        mock_http_message = self.mox.CreateMockAnything()
        mock_contents = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(Updater, "get_tarball_url")
        self.mox.StubOutWithMock(urllib2, "urlopen")
        self.mox.StubOutWithMock(__builtin__, "open")
        self.mox.StubOutWithMock(os.path, "isdir")
        self.mox.StubOutWithMock(os, "mkdir")

        os.path.isdir(self.__update_dir).AndReturn(False)
        os.mkdir(self.__update_dir)

        Updater.get_tarball_url(self.__repo).AndReturn(self.__tarball_url)
        urllib2.urlopen(self.__tarball_url).AndReturn(mock_resource)

        mock_resource.info().AndReturn(mock_http_message)
        mock_http_message.get("Content-Disposition").AndReturn(self.__content_string)

        __builtin__.open(self.__target_filename, "wb").AndReturn(mock_file)
        mock_file.__enter__().AndReturn(mock_file)
        mock_file.write(mock_resource.read().AndReturn(mock_contents))
        mock_file.__exit__(mox.IgnoreArg(), mox.IgnoreArg(), mox.IgnoreArg())

        self.mox.ReplayAll()

        updater = Updater(repo = self.__repo, update_dir = self.__update_dir)
        self.assertEquals(self.__target_filename, updater.download_tarball())

    def test_download_filename_construction_raises(self):
        """ download_tarball should download the tarball found at
        get_tarball_url, to get_target_directory """

        mock_resource = self.mox.CreateMockAnything()
        mock_file = self.mox.CreateMockAnything()
        mock_http_message = self.mox.CreateMockAnything()
        mock_contents = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(Updater, "get_tarball_url")
        self.mox.StubOutWithMock(urllib2, "urlopen")
        self.mox.StubOutWithMock(__builtin__, "open")
        self.mox.StubOutWithMock(os.path, "isdir")

        os.path.isdir(self.__update_dir).AndReturn(True)

        Updater.get_tarball_url(self.__repo).AndReturn(self.__tarball_url)
        urllib2.urlopen(self.__tarball_url).AndReturn(mock_resource)

        mock_resource.info().AndReturn(mock_http_message)
        mock_http_message.get("Content-Disposition").AndRaise(
            AttributeError("foobar"))

        __builtin__.open("%s/%s.tar.gz" %
                          (self.__update_dir, self.__tarball_filename),
                          "wb").AndReturn(mock_file)
        mock_file.__enter__().AndReturn(mock_file)
        mock_file.write(mock_resource.read().AndReturn(mock_contents))
        mock_file.__exit__(mox.IgnoreArg(), mox.IgnoreArg(), mox.IgnoreArg())

        self.mox.ReplayAll()

        updater = Updater(repo = self.__repo, update_dir = self.__update_dir)
        self.assertEquals("%s/%s.tar.gz" %
            (self.__update_dir, self.__tarball_filename),
                          updater.download_tarball())


if "__main__" == __name__:
    unittest.main()
