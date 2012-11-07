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

import logging
import os
import urllib2

class Updater(object):
    """ Updater contains common methods used by the StableUpdater and
    BleedingEdgeUpdater. """

    def __init__(self, repo, update_dir = "/tmp"):
        self.__repo = repo
        self.__update_dir = update_dir

    def download_update(self):
        """ Download an update using the prefered method (default is tarball
        download). """

        self.download_tarball()

    def download_tarball(self):
        """ Download a source tree tarball from github. """

        tarball_url = self.get_tarball_url(self.__repo)

        local_filename = None

        logger = logging.getLogger()

        if not os.path.isdir(self.__update_dir):
            os.mkdir(self.__update_dir)

        try:
            url_object = urllib2.urlopen(tarball_url)

            if url_object:
                try:
                    filename = url_object.info().get(
                        "Content-Disposition").split("filename=")[-1]
                except:
                    filename = os.path.basename(tarball_url) + ".tar.gz"

                local_filename = os.path.join(self.__update_dir, filename)

                logger.info(u"Downloading %s to %s" %
                            (tarball_url, local_filename))

                with open(local_filename, "wb") as local_file:
                    local_file.write(url_object.read())
        except urllib2.HTTPError, error:
            logger.info(u"%d encountered when attempting to download %s" % 
                        (error.getcode(), tarball_url))
        except urllib2.URLError:
            logger.info(u"Failed to download %s" % tarball_url)
        except AttributeError:
            logger.info(u"Missing urlopen handler for %s" % tarball_url)

        return local_filename

    def get_tarball_url(self, repo):
        """ This method is to be overriden by subtypes, in order to fetch the
        appropriate tarball. """

        raise Exception("Method not overridden")

