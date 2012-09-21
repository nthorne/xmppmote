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
import version
import urllib2
import json

class BleedingEdgeUpdater(Updater):
    """ BleedingEdgeUpdater queries github for current commit id, and if that
    differs from the commit id of the installed software (if available), it
    attempts to update the installed version by pulling from github, if
    possible; otherwise a tarball of HEAD of origin/master is downloaded. """

    def __init__(self, remote_url):
        super(BleedingEdgeUpdater, self).__init__()

        self.__remote_url = remote_url
        self.__project_root = os.path.dirname(
            os.path.abspath(version.__file__))

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

        try:
            response = urllib2.urlopen(self.__remote_url)

            html = response.read()

            json_dict = json.loads(html)

            result = json_dict["sha"]
        # raised from urlopen
        except urllib2.URLError:
            pass
        # raised if urlopen returns None
        except AttributeError:
            pass
        # raised upon None or invalid json data
        except (TypeError, ValueError):
            pass
        # raised if the sha key does not exists in the json dict
        except KeyError:
            pass

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

