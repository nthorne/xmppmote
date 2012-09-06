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

""" This module tests the borg module. """

import sys
import os

sys.path.append(os.path.abspath(".."))

import borg
import mox
import unittest

class BorgTest(mox.MoxTestBase):
    """ This type provides test cases for testing the borg module. """
    def test_make_borg(self):
        """ This method tests the make_borg function of the borg module. """
        class FirstType(borg.make_borg()):
            pass

        class SecondType(borg.make_borg()):
            pass


        first_type_first_instance = FirstType()
        first_type_first_instance.value = 42
        first_type_second_instance = FirstType()

        second_type_first_instance = SecondType()
        second_type_first_instance.value = 21
        second_type_second_instance = SecondType()

        self.assertEqual(42, first_type_first_instance.value)
        self.assertEqual(first_type_first_instance.value,
                         first_type_second_instance.value)

        self.assertEqual(21, second_type_first_instance.value)
        self.assertEqual(second_type_first_instance.value,
                         second_type_second_instance.value)

    def test_borg_init(self):
        """ This method tests initialising variables in the __init__ method of a
        Borg subclass. """

        class FirstType(borg.make_borg()):
            def __init__(self):
                super(FirstType, self).__init__()
                self.foo = 'bar'

        class SecondType(borg.make_borg()):
            def __init__(self):
                super(SecondType, self).__init__()
                self.foo = 'foobar'

        first_type_first_instance = FirstType()
        first_type_first_instance.value = 13
        first_type_second_instance = FirstType()
        
        second_type_first_instance = SecondType()
        second_type_first_instance.value = 26
        second_type_second_instance = SecondType()

        self.assertEqual('bar', first_type_first_instance.foo)
        self.assertEqual('bar', first_type_second_instance.foo)
        self.assertEqual(13, first_type_first_instance.value)
        self.assertEqual(first_type_first_instance.value,
                         first_type_second_instance.value)

        self.assertEqual('foobar', second_type_first_instance.foo)
        self.assertEqual('foobar', second_type_second_instance.foo)
        self.assertEqual(26, second_type_first_instance.value)
        self.assertEqual(second_type_first_instance.value,
                         second_type_second_instance.value)
    

if "__main__" == __name__:
    unittest.main()
