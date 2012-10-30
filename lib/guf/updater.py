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

""" This module contains the Updater type.

Updater is the supertype for the StableUpdater and BleedingEdgeUpdater, and
provides common methods (e.g. extracting downloaded tarball, replacing
software). """

import urllib2
import os

class Updater(object):
    """ Updater contains common methods used by the StableUpdater and
    BleedingEdgeUpdater. """

    def __init__(self, repo, update_dir = "/tmp"):
        self.__repo = repo
        self.__update_dir = update_dir

    def download_update(self):
        self.download_tarball()

    def download_tarball(self):
        tarball_url = self.get_tarball_url(self.__repo)

        url_object = urllib2.urlopen(tarball_url)

        filename = url_object.info().get("Content-Disposition").split("filename=")[-1]

        local_filename = os.path.join(self.__update_dir, filename)

        with open(local_filename, "wb") as local_file:
            local_file.write(url_object.read())

        return local_filename

    def get_tarball_url(self, repo):
        raise Exception("Method not overridden")

