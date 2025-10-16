from pathlib import Path
import sys
import unittest
from unittest.mock import Mock
from pydantic import ValidationError

try:
    from gradescope_utils.autograder_utils.decorators import weight, number
except Exception as e:
    # print(e)
    from test_dummy import weight,number

from profiles.data.profile_api import ProfileAPI
from profiles.data.profile_models import *

# this is a mock pm
mock_pm = Mock()
p1 = Profile(username='jane',profile_name='North Country Guides')
mock_pm.read_all.return_value = ProfileCollection(profiles=[p1])
mock_pm.read_by_profile_name.return_value = p1

class TestProfiles(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # dbm = DBManager(cs, db, col)
        # cls.pm = ProfileManager(dbm)
        cls.api = ProfileAPI(mock_pm)

    # @unittest.skip
    @weight(2.5)
    @number("5")
    def test_create(self):

        # create with dict
        p2 = {'username':'jane','profile_name':'Seacoast Guides'}
        self.api.create(p2)

        p3 = {'username':'jane'}
        with self.assertRaises(ValidationError):
            self.api.create(p3)

    @weight(2.5)
    @number("6")    
    def test_read_all(self):
        ps = self.api.read_all()
        # print(ps)

        self.assertIsInstance(ps[0],dict)

    @weight(2.5)
    @number("7")
    def test_read_by_profile_name(self):

        p1 = self.api.read_by_profile_name("North Country Guides")
        self.assertIsInstance(p1,dict)

    @weight(2.5)
    @number("8")
    def test_add_skills(self):

        pid = '765sa8f765sa'

        self.api.add_skills(pid, ['running','jumping','throwing'])

        with self.assertRaises(ValidationError):
            self.api.add_skills(pid, 'running')


if __name__=="__main__":
    unittest.main()