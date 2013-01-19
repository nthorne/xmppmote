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

""" This module contains the BleedingEdgeUpdater type.

BleedingEdgeUpdater is responsible for performing bleeding edge version checks
and updates of the software, against github. """

import sys
import os

sys.path.append(os.path.abspath("../../.."))


from updater import Updater

import git
import git.exceptions
import version
import urllib2
import json
import logging


class BleedingEdgeUpdater(Updater):
    """ BleedingEdgeUpdater queries github for current commit id, and if that
    differs from the commit id of the installed software (if available), it
    attempts to update the installed version by pulling from github, if
    possible; otherwise a tarball of HEAD of origin/master is downloaded. """

    def __init__(self, repo):
        super(BleedingEdgeUpdater, self).__init__(repo)

        self.__remote_url = os.path.join(
            os.path.join(
                os.path.join('https://api.github.com/repos', repo),
                'commits'),
            'HEAD')
        self.__project_root = os.path.dirname(
            os.path.abspath(version.__file__))

        # TODO: Do we really want to cache this? If we do, we need
        #  to make sure that we remember to update the cache whenever
        # it changes.
        self.local_head_commit_hash = None
        self.origin_head_sha = None

        if self.is_repo():
            self.repo = git.LocalRepository(self.__project_root)

            if self.has_git():
                self.local_head_commit_hash = self.repo.getHead().hash

    def is_repo(self):
        """ Test if the project root is a git repo (i.e. has a .git subfolder).
        """

        return os.path.isdir(os.path.join(self.__project_root, ".git"))

    def has_git(self):
        """ Test if git v1 is available. """

        try:
            result = "1." == self.repo.getGitVersion()[:2]
        except (git.exceptions.GitException, AttributeError):
            result = False

        return result

    def get_origin_head_sha(self):
        """ Return the SHA of origin/HEAD. """

        result = None

        logger = logging.getLogger()

        try:
            response = urllib2.urlopen(self.__remote_url)

            html = response.read()

            json_dict = json.loads(html)

            result = json_dict["sha"]
        # raised from urlopen
        except urllib2.URLError, exc:
            logger.info(u"Failed to connect to %s: %s" % (self.__remote_url,
                                                          exc))
        # raised if urlopen returns None
        except AttributeError:
            pass
        # raised upon None or invalid json data
        except (TypeError, ValueError):
            logger.info(u"Invalid JSON returned from %s" % self.__remote_url)
        # raised if the sha key does not exists in the json dict
        except KeyError:
            logger.info(u"No sha key in JSON data.")

        return result

    def check(self):
        """ Check __remote_url for a new software version. This is done via the
        github json API, where we query origin for the HEAD SHA, and compare it
        to the local HEAD SHA. """

        new_version = False

        self.origin_head_sha = self.get_origin_head_sha()
        if self.origin_head_sha:
            new_version = self.local_head_commit_hash != self.origin_head_sha

        return new_version

    def get_update_version(self):
        """ Get the version that the last update check yielded. """

        return self.origin_head_sha

    def download_update(self):
        """ Download source code update. """

        if self.is_repo() and self.has_git():
            if self.fetch_from_origin():
                self.merge_with_origin()
        else:
            self.download_tarball()

    def fetch_from_origin(self):
        """ Fetch software update from origin. """

        try:
            self.repo.fetch()
        except (AssertionError, git.exceptions.GitException):
            return False

        return True

    def get_tarball_url(self, repo):

        return os.path.join(
            os.path.join("https://github.com", repo),
            "tarball/master")

    def merge_with_origin(self):
        """ Merge changes fetched from origin. Local changes will be stashed
        before attempting to merge. """

        try:
            self.repo.saveStash()
        except git.exceptions.GitException:
            return False

        try:
            self.repo.merge("origin/master")
            self.repo.popStash()
        except git.exceptions.GitException:
            self.repo.resetHard(self.local_head_commit_hash)
            return False

        return True

        pass
