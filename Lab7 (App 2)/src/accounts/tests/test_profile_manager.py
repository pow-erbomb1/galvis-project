from pathlib import Path
import sys
import unittest

try:
    from gradescope_utils.autograder_utils.decorators import weight, number
except Exception as e:
    # print(e)
    from test_dummy import weight,number

from utils.db_manager import DBManager
from profiles.data.profile_manager import ProfileManager
from profiles.data.profile_models import *
from config import GUIDE_CONFIG

cs = GUIDE_CONFIG.DB_URL
db = GUIDE_CONFIG.GUIDE_DB
col = GUIDE_CONFIG.PROFILE_COL

class TestProfiles(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        dbm = DBManager(cs, db, col)
        cls.pm = ProfileManager(dbm)

    def setUp(self):
        print(self.id())
        self.pm.delete_all()

    @classmethod
    def tearDownClass(cls):
        cls.pm.delete_all()

    def create_profile(self):
        p = Profile(username="admin", profile_name="joes_adventures")
        return self.pm.create(p)        

    # @unittest.skip
    @weight(2.5)
    @number("1")
    def test_create_read(self):
        ''' create, read_by_id'''

        pid = self.create_profile()

        p = self.pm.read_by_id(pid)
        self.assertEqual(p.profile_name,"joes_adventures")

    @weight(2.5)
    @number("2")
    def test_read_by_profile_name(self):

        pid = self.create_profile()

        p = self.pm.read_by_profile_name('joes_adventures')
        # print(p)
        self.assertEqual(p.profile_name, "joes_adventures")

    @weight(2.5)
    @number("3")
    def test_read_by_user_id(self):

        self.create_profile()

        # and another
        p = Profile(username="admin", profile_name="joes_arctic_adventures")
        self.pm.create(p)
        
        profs = self.pm.read_by_username('admin')
        # print(profs)
        self.assertEqual(len(profs.profiles),2)

    @weight(2.5)
    @number("4")
    def test_add_skills(self):
        ''' add skills'''

        pid = self.create_profile()

        skills = ProfileSkills(skills=["trad climbing", "lead climbing", "multi-pitch climbing"])

        r = self.pm.add_skills(pid,skills)
        # print(r)

        p = self.pm.read_by_id(pid)
        # p = Profile(**p)
        # print(p)

        self.assertEqual(len(p.skills),3)

if __name__ == '__main__':
    unittest.main()
    pass