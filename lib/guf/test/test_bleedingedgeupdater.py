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

""" This module tests the bleedingedgeupdater module. """

import sys
import os

sys.path.append(os.path.abspath(".."))

import mox
import unittest

from bleedingedgeupdater import BleedingEdgeUpdater
import version
import git
import urllib2
import json
import git.exceptions


class BleedingEdgeUpdaterTest(mox.MoxTestBase):
    """ Provides test cases for BleedingEdgeUpdater. """

    __project_root = os.path.dirname(
        os.path.abspath(version.__file__))
    __repo = "foo/bar"
    __remote_url = "https://api.github.com/repos/foo/bar/commits/HEAD"
    __tarball_url = "https://github.com/foo/bar/tarball/master"
    __mock_local_head_hash = "local"
    __mock_origin_head_sha = "origin"
    __tarball_filename = "/tmp/guf.tar.gz"

    def test_is_repo_when_is_repo(self):
        """ If project root contains a .git directory, make sure that is_repo
        indicates that. """

        self.mox.StubOutWithMock(os.path, "isdir")

        # This first call is __init__ checking is_repo in order to create a
        # LocalRepository attribute.
        os.path.isdir(os.path.join(self.__project_root, ".git")).AndReturn(True)
        os.path.isdir(os.path.join(self.__project_root, ".git")).AndReturn(True)

        self.mox.ReplayAll()

        updater = BleedingEdgeUpdater(self.__repo)
        self.assertTrue(updater.is_repo())

    def test_is_repo_when_isnt_repo(self):
        """ If project root does not contain a .git directory, make sure that
        is_repo indicates that. """

        self.mox.StubOutWithMock(os.path, "isdir")

        # This first call is __init__ checking is_repo in order to create a
        # LocalRepository attribute.
        os.path.isdir(os.path.join(
            self.__project_root, ".git")).AndReturn(False)
        os.path.isdir(os.path.join(
            self.__project_root, ".git")).AndReturn(False)

        self.mox.ReplayAll()

        updater = BleedingEdgeUpdater(self.__repo)
        self.assertTrue(not updater.is_repo())

    def test_has_git_when_has_git(self):
        """ has_git should return True if the git library indicates git v1 as
        being available. """

        self.mox.StubOutWithMock(git.LocalRepository, "getGitVersion")

        git.LocalRepository.getGitVersion().AndReturn("1.7.5.4")

        self.mox.ReplayAll()

        updater = BleedingEdgeUpdater(self.__repo)
        self.assertTrue(updater.has_git())

    def test_has_git_when_does_not_have_git(self):
        """ has_git should return False if the git library is unable to locate
        git v1. """

        self.mox.StubOutWithMock(git.LocalRepository, "getGitVersion")

        # This first call is __init__ retrieving HEAD commit hash
        git.LocalRepository.getGitVersion().AndRaise(
            git.exceptions.GitException("dang nabit"))

        self.mox.ReplayAll()

        updater = BleedingEdgeUpdater(self.__repo)
        self.assertTrue(not updater.has_git())

    def test_has_git_when_is_not_repo(self):
        """ If project root is not a repo, has_git should return False, rather
        than raising an exception, as it requires a local repository in order to
        query git for version(?!). """

        self.mox.StubOutWithMock(BleedingEdgeUpdater, "is_repo")
        self.mox.StubOutWithMock(git.LocalRepository, "getGitVersion")

        BleedingEdgeUpdater.is_repo().AndReturn(False)

        self.mox.ReplayAll()

        updater = BleedingEdgeUpdater(self.__repo)
        self.assertTrue(not updater.has_git())

    def test_getting_local_commit_hash(self):
        """ If project root is a git repo, and git is avaialable, tha
        local_head_commit_hash attribute should contain the SHA of HEAD after
        having initialized BleedingEdgeUpdater. """

        mock_commit = self.mox.CreateMockAnything()
        mock_commit.hash = self.__mock_local_head_hash

        self.mox.StubOutWithMock(git.LocalRepository, "getHead")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "is_repo")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "has_git")

        BleedingEdgeUpdater.is_repo().AndReturn(True)
        BleedingEdgeUpdater.has_git().AndReturn(True)
        git.LocalRepository.getHead().AndReturn(mock_commit)

        self.mox.ReplayAll()

        updater = BleedingEdgeUpdater(self.__repo)
        self.assertEquals(self.__mock_local_head_hash,
                          updater.get_local_head_commit_hash())

    def test_getting_local_commit_hash_no_repo(self):
        """ If project root is not a repo, local_head_commit_hash attribute
        should equal None. """
        mock_commit = self.mox.CreateMockAnything()
        mock_commit.hash = self.__mock_local_head_hash

        self.mox.StubOutWithMock(git.LocalRepository, "getHead")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "is_repo")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "has_git")

        BleedingEdgeUpdater.is_repo().AndReturn(False)

        self.mox.ReplayAll()

        updater = BleedingEdgeUpdater(self.__repo)
        self.assertEqual(None, updater.get_local_head_commit_hash())

    def test_getting_local_commit_hash_no_git(self):
        """ If git is not available, local_head_commit_hash attribute should
        equal None. """

        mock_commit = self.mox.CreateMockAnything()
        mock_commit.hash = self.__mock_local_head_hash

        self.mox.StubOutWithMock(git.LocalRepository, "getHead")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "is_repo")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "has_git")

        BleedingEdgeUpdater.is_repo().AndReturn(True)
        BleedingEdgeUpdater.has_git().AndReturn(False)

        self.mox.ReplayAll()

        updater = BleedingEdgeUpdater(self.__repo)
        self.assertEqual(None, updater.get_local_head_commit_hash())

    def test_getting_origin_head_hash(self):
        """ Sunshine case when querying github for origin/master HEAD SHA. """

        mock_response = self.mox.CreateMockAnything()
        mock_html = self.mox.CreateMockAnything()
        mock_json_dict = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(urllib2, "urlopen")
        self.mox.StubOutWithMock(json, "loads")

        urllib2.urlopen(self.__remote_url).AndReturn(mock_response)
        mock_response.read().AndReturn(mock_html)

        json.loads(mock_html).AndReturn(mock_json_dict)

        mock_json_dict["sha"].AndReturn(self.__mock_origin_head_sha)

        self.mox.ReplayAll()

        bleeding_updater = BleedingEdgeUpdater(self.__repo)

        self.assertEquals(self.__mock_origin_head_sha,
                          bleeding_updater.get_origin_head_sha())

    def test_getting_origin_head_hash_urlopen_exception(self):
        """ If urlopen raises an exception (timeout, invalid url, etc.), None
        should be returned. """

        self.mox.StubOutWithMock(urllib2, "urlopen")
        self.mox.StubOutWithMock(json, "loads")

        urllib2.urlopen(self.__remote_url).AndRaise(urllib2.URLError("na-ah"))

        self.mox.ReplayAll()

        bleeding_updater = BleedingEdgeUpdater(self.__repo)

        self.assertEquals(None, bleeding_updater.get_origin_head_sha())

    def test_getting_origin_head_hash_no_response(self):
        """ If urlopen returns None, None should be returned. """

        self.mox.StubOutWithMock(urllib2, "urlopen")
        self.mox.StubOutWithMock(json, "loads")

        urllib2.urlopen(self.__remote_url).AndReturn(None)

        self.mox.ReplayAll()

        bleeding_updater = BleedingEdgeUpdater(self.__repo)

        self.assertEquals(None, bleeding_updater.get_origin_head_sha())

    def test_getting_origin_head_hash_no_html(self):
        """ If we fail to read the urlopen query, None shall be returned. """

        mock_response = self.mox.CreateMockAnything()

        self.mox.StubOutWithMock(urllib2, "urlopen")

        urllib2.urlopen(self.__remote_url).AndReturn(mock_response)

        mock_response.read().AndReturn(None)

        self.mox.ReplayAll()

        bleeding_updater = BleedingEdgeUpdater(self.__repo)

        self.assertEquals(None, bleeding_updater.get_origin_head_sha())

    def test_getting_origin_head_hash_no_json(self):
        """ In the case of the read HTML not containing proper json, None shall
        be returned. """

        mock_response = self.mox.CreateMockAnything()
        mock_html = "no json for you"

        self.mox.StubOutWithMock(urllib2, "urlopen")

        urllib2.urlopen(self.__remote_url).AndReturn(mock_response)

        mock_response.read().AndReturn(mock_html)

        self.mox.ReplayAll()

        bleeding_updater = BleedingEdgeUpdater(self.__repo)

        self.assertEquals(None, bleeding_updater.get_origin_head_sha())

    def test_getting_origin_head_hash_no_sha_in_json(self):
        """ If the json response from github does not contain a SHA key, None
        shall be returned. """

        mock_response = self.mox.CreateMockAnything()
        mock_html = self.mox.CreateMockAnything()

        mock_json_dict = {'foo': 'bar'}

        self.mox.StubOutWithMock(urllib2, "urlopen")
        self.mox.StubOutWithMock(json, "loads")

        urllib2.urlopen(self.__remote_url).AndReturn(mock_response)
        mock_response.read().AndReturn(mock_html)

        json.loads(mock_html).AndReturn(mock_json_dict)

        self.mox.ReplayAll()

        bleeding_updater = BleedingEdgeUpdater(self.__repo)

        self.assertEquals(None, bleeding_updater.get_origin_head_sha())

    def test_github_has_new_version(self):
        """ If the github query returns a SHA key that differs from the local
        master HEAD key, check shall indicate that a new version is available.
        """

        mock_commit = self.mox.CreateMockAnything()
        mock_commit.hash = self.__mock_local_head_hash

        self.mox.StubOutWithMock(git.LocalRepository, "getHead")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "is_repo")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "has_git")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "get_origin_head_sha")

        BleedingEdgeUpdater.is_repo().AndReturn(True)
        BleedingEdgeUpdater.has_git().AndReturn(True)
        git.LocalRepository.getHead().AndReturn(mock_commit)

        BleedingEdgeUpdater.get_origin_head_sha().AndReturn(
            self.__mock_origin_head_sha)

        self.mox.ReplayAll()

        updater = BleedingEdgeUpdater(self.__repo)

        self.assertTrue(updater.check())

    def test_github_does_not_have_new_version(self):
        """ If the github query returns a SHA key that is equal to the local
        master HEAD key, check shall indicate that there is no new version
        available. """

        mock_commit = self.mox.CreateMockAnything()
        mock_commit.hash = self.__mock_local_head_hash

        self.mox.StubOutWithMock(git.LocalRepository, "getHead")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "is_repo")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "has_git")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "get_origin_head_sha")

        BleedingEdgeUpdater.is_repo().AndReturn(True)
        BleedingEdgeUpdater.has_git().AndReturn(True)
        git.LocalRepository.getHead().AndReturn(mock_commit)

        BleedingEdgeUpdater.get_origin_head_sha().AndReturn(
            self.__mock_local_head_hash)

        self.mox.ReplayAll()

        updater = BleedingEdgeUpdater(self.__repo)

        self.assertTrue(not updater.check())

    def test_download_update_when_has_git_and_is_repo_fetch_succeeds(self):
        """ If the project root is a git repo, and git is available, changes
        shall be fetched from github. """

        self.mox.StubOutWithMock(BleedingEdgeUpdater, "is_repo")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "has_git")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "fetch_from_origin")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "merge_with_origin")
        self.mox.StubOutWithMock(git.LocalRepository, "fetch")

        BleedingEdgeUpdater.is_repo().AndReturn(True)

        BleedingEdgeUpdater.is_repo().AndReturn(True)
        BleedingEdgeUpdater.has_git().AndReturn(True)

        BleedingEdgeUpdater.fetch_from_origin().AndReturn(True)
        BleedingEdgeUpdater.merge_with_origin()

        self.mox.ReplayAll()

        updater = BleedingEdgeUpdater(self.__repo)
        updater.download_update()

    def test_download_update_when_has_git_and_is_repo_fetch_fails(self):
        """ If the project root is a git repo, and git is available, changes
        shall be fetched from github. """

        self.mox.StubOutWithMock(BleedingEdgeUpdater, "is_repo")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "has_git")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "fetch_from_origin")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "merge_with_origin")
        self.mox.StubOutWithMock(git.LocalRepository, "fetch")

        BleedingEdgeUpdater.is_repo().AndReturn(True)

        BleedingEdgeUpdater.is_repo().AndReturn(True)
        BleedingEdgeUpdater.has_git().AndReturn(True)

        BleedingEdgeUpdater.fetch_from_origin().AndReturn(False)

        self.mox.ReplayAll()

        updater = BleedingEdgeUpdater(self.__repo)
        updater.download_update()

    def test_download_update_when_no_git(self):
        """ If git is not available, there should be no attempt to fetch from
        origin, but rather a source tarball should be downloaded. """

        self.mox.StubOutWithMock(BleedingEdgeUpdater, "is_repo")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "has_git")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "fetch_from_origin")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "merge_with_origin")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "download_tarball")
        self.mox.StubOutWithMock(git.LocalRepository, "fetch")

        BleedingEdgeUpdater.is_repo().AndReturn(True)

        BleedingEdgeUpdater.is_repo().AndReturn(True)
        BleedingEdgeUpdater.has_git().AndReturn(False)

        BleedingEdgeUpdater.download_tarball()

        self.mox.ReplayAll()

        updater = BleedingEdgeUpdater(self.__repo)
        updater.download_update()

    def test_download_update_when_no_repo(self):
        """ If project root is not a repo, there should be no attempt to fetch
        from origin, but rather a source tarball should be downloaded. """

        self.mox.StubOutWithMock(BleedingEdgeUpdater, "is_repo")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "fetch_from_origin")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "merge_with_origin")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "download_tarball")
        self.mox.StubOutWithMock(git.LocalRepository, "fetch")

        BleedingEdgeUpdater.is_repo().AndReturn(True)

        BleedingEdgeUpdater.is_repo().AndReturn(False)

        BleedingEdgeUpdater.download_tarball()

        self.mox.ReplayAll()

        updater = BleedingEdgeUpdater(self.__repo)
        updater.download_update()

    def test_getting_tarball_url(self):
        """ Make sure that the get_tarball url method is overloaded and returns
        a sane URL. """

        self.mox.ReplayAll()

        updater = BleedingEdgeUpdater(self.__repo)

        self.assertEquals(self.__tarball_url,
                          updater.get_tarball_url(self.__repo))

    def test_fetching_from_github_succeeds(self):
        """ If fetching from github succeeds, fetch_from_origin should return
        True. fetch_from_origin can safely assume that git is installed and that
        the tree is a repo. """

        self.mox.StubOutWithMock(BleedingEdgeUpdater, "is_repo")
        self.mox.StubOutWithMock(git.LocalRepository, "fetch")

        BleedingEdgeUpdater.is_repo().AndReturn(True)

        git.LocalRepository.fetch()

        self.mox.ReplayAll()

        self.assertTrue(BleedingEdgeUpdater(self.__repo).fetch_from_origin())

    def test_fetching_from_github_fails(self):
        """ If fetching from github fails (an assertion is raised),
        fetch_from_origin should return false. """

        self.mox.StubOutWithMock(BleedingEdgeUpdater, "is_repo")
        self.mox.StubOutWithMock(git.LocalRepository, "fetch")

        BleedingEdgeUpdater.is_repo().AndReturn(True)

        git.LocalRepository.fetch().AndRaise(AssertionError)

        git.LocalRepository.fetch().AndRaise(git.exceptions.GitException("foo"))

        self.mox.ReplayAll()

        updater = BleedingEdgeUpdater(self.__repo)

        self.assertFalse(updater.fetch_from_origin())
        self.assertFalse(updater.fetch_from_origin())

    def test_mergeing_with_fetched_source_succeeds(self):
        """ If both merge and stash pop succeeds, true should be returned
        from merge_with_origin. """

        self.mox.StubOutWithMock(BleedingEdgeUpdater, "is_repo")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "has_git")
        self.mox.StubOutWithMock(git.LocalRepository, "saveStash")
        self.mox.StubOutWithMock(git.LocalRepository, "merge")
        self.mox.StubOutWithMock(git.LocalRepository, "popStash")

        BleedingEdgeUpdater.is_repo().AndReturn(True)
        BleedingEdgeUpdater.has_git().AndReturn(True)

        git.LocalRepository.saveStash()
        git.LocalRepository.merge("origin/master")
        git.LocalRepository.popStash()

        self.mox.ReplayAll()

        updater = BleedingEdgeUpdater(self.__repo)

        self.assertTrue(updater.merge_with_origin())

    def test_mergeing_with_fetched_source_merge_fails(self):
        """ If the merge fails, false shoule be returned from merge_with_origin,
        and the repo should be reset to the state it was in before the merge
        attempt. """

        mock_commit = self.mox.CreateMockAnything()
        mock_commit.hash = self.__mock_local_head_hash

        self.mox.StubOutWithMock(BleedingEdgeUpdater, "is_repo")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "has_git")
        self.mox.StubOutWithMock(git.LocalRepository, "getHead")
        self.mox.StubOutWithMock(git.LocalRepository, "saveStash")
        self.mox.StubOutWithMock(git.LocalRepository, "merge")
        self.mox.StubOutWithMock(git.LocalRepository, "resetHard")

        BleedingEdgeUpdater.is_repo().AndReturn(True)
        BleedingEdgeUpdater.has_git().AndReturn(True)
        git.LocalRepository.getHead().AndReturn(mock_commit)

        git.LocalRepository.saveStash()
        git.LocalRepository.merge("origin/master").AndRaise(
            git.exceptions.GitException("dang nabit"))
        git.LocalRepository.resetHard(self.__mock_local_head_hash)

        self.mox.ReplayAll()

        updater = BleedingEdgeUpdater(self.__repo)

        self.assertFalse(updater.merge_with_origin())

    def test_mergeing_with_fetched_source_stash_pop_fails(self):
        """ If the stash pop fails, false should be returned from
        merge_with_origin, and the repo should be reset to the state it was in
        before the merge attempt. """

        mock_commit = self.mox.CreateMockAnything()
        mock_commit.hash = self.__mock_local_head_hash

        self.mox.StubOutWithMock(BleedingEdgeUpdater, "is_repo")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "has_git")
        self.mox.StubOutWithMock(git.LocalRepository, "getHead")
        self.mox.StubOutWithMock(git.LocalRepository, "saveStash")
        self.mox.StubOutWithMock(git.LocalRepository, "merge")
        self.mox.StubOutWithMock(git.LocalRepository, "popStash")
        self.mox.StubOutWithMock(git.LocalRepository, "resetHard")

        BleedingEdgeUpdater.is_repo().AndReturn(True)
        BleedingEdgeUpdater.has_git().AndReturn(True)
        git.LocalRepository.getHead().AndReturn(mock_commit)

        git.LocalRepository.saveStash()
        git.LocalRepository.merge("origin/master")
        git.LocalRepository.popStash().AndRaise(
            git.exceptions.GitException("dang nabit"))
        git.LocalRepository.resetHard(self.__mock_local_head_hash)

        self.mox.ReplayAll()

        updater = BleedingEdgeUpdater(self.__repo)

        self.assertFalse(updater.merge_with_origin())

    def test_download_tarball_succeeds(self):
        """ If download_tarball returns a valid, existing, filename,
        the download is considered succeeded, and an attempt to install the
        update will be performed. """

        self.mox.StubOutWithMock(BleedingEdgeUpdater, "is_repo")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "fetch_from_origin")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "merge_with_origin")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "download_tarball")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "update_from_tarball")
        self.mox.StubOutWithMock(os.path, "isfile")

        BleedingEdgeUpdater.is_repo().AndReturn(True)

        BleedingEdgeUpdater.is_repo().AndReturn(False)

        BleedingEdgeUpdater.download_tarball().AndReturn(self.__tarball_filename)
        os.path.isfile(self.__tarball_filename).AndReturn(True)
        BleedingEdgeUpdater.update_from_tarball(self.__tarball_filename)

        self.mox.ReplayAll()

        updater = BleedingEdgeUpdater(self.__repo)
        updater.download_update()

    def test_download_tarball_fails(self):
        """ If download_tarball returns None, the download attempt will be
        considered failed, and the update attempt should be aborted. """

        self.mox.StubOutWithMock(BleedingEdgeUpdater, "is_repo")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "fetch_from_origin")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "merge_with_origin")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "download_tarball")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "update_from_tarball")

        BleedingEdgeUpdater.is_repo().AndReturn(True)

        BleedingEdgeUpdater.is_repo().AndReturn(False)

        BleedingEdgeUpdater.download_tarball()

        self.mox.ReplayAll()

        updater = BleedingEdgeUpdater(self.__repo)
        updater.download_update()

    def test_download_tarball_succeeds_but_no_tarball(self):
        """ If download_tarball returns a non-zero string, but the file
        pointed to by that string does not exists, the update should be
        aborted. """

        self.mox.StubOutWithMock(BleedingEdgeUpdater, "is_repo")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "fetch_from_origin")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "merge_with_origin")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "download_tarball")
        self.mox.StubOutWithMock(BleedingEdgeUpdater, "update_from_tarball")
        self.mox.StubOutWithMock(os.path, "isfile")

        BleedingEdgeUpdater.is_repo().AndReturn(True)

        BleedingEdgeUpdater.is_repo().AndReturn(False)

        BleedingEdgeUpdater.download_tarball().AndReturn(self.__tarball_filename)

        os.path.isfile(self.__tarball_filename).AndReturn(False)

        self.mox.ReplayAll()

        updater = BleedingEdgeUpdater(self.__repo)
        updater.download_update()


if "__main__" == __name__:
    unittest.main()
