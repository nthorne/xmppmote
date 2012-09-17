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

""" This module contains the StableUpdater type.

StableUpdater is responsible for performing stable version checks and updates of
the software, against github. """

import sys
import os

sys.path.append(os.path.abspath("../.."))

from updater import Updater

import urllib2
import json
import base64

import version
import re

import logging

class StableUpdater(Updater):
    """ StableUpdater queries github for lates tag, and if that differs from the
    version defined in version.version, a tarball for the newer tag is
    downloaded. """ 

    def __init__(self, remote_url):
        self.__remote_url = remote_url

        self.has_new_version = False
        self.remote_version = None

        self.__version_regex = re.compile(r"version\s*=.*")
        self.__version_get_regex = re.compile(r"^\s*version[^0-9]*([.0-9]+).*$")
        self.__invalid_version_token = re.compile(r"[^.0-9]")


    def check(self):
        """ Check __remote_url for an new software version. This is done via the
        github json API, where we download the version file, and inspect its
        contents. """

        self.has_new_version = False
        self.remote_version = None

        logger = logging.getLogger()

        try:
            response = urllib2.urlopen(self.__remote_url)
        except (ValueError, urllib2.URLError), exc:
            logger.info(u"Failed to connect to %s: %s" % (self.__remote_url,
                                                          exc))
            return

        html = response.read()

        if not html:
            return

        try:
            json_dict = json.loads(html)
        except ValueError:
            return

        try:
            remote_src = base64.b64decode(json_dict["content"])
        except TypeError:
            return

        self.remote_version = self.__parse_remote_version(remote_src)

        if self.remote_version and hasattr(version, "version"):
            self.has_new_version = version.version < self.remote_version

    def __parse_remote_version(self, remote_src):
        """ Parse the string contents of the version file, attempting to extract
        the version defined in it. """

        ver = re.findall(self.__version_regex, remote_src)

        result = None

        if ver and 1 == len(ver):
            result = re.sub(self.__version_get_regex, r"\1", ver[0])
            if re.findall(self.__invalid_version_token, result):
                result = None

        return result

