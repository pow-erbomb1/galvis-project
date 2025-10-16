from profiles.data.profile_manager import ProfileManager
from profiles.data.profile_models import *

class ProfileAPI:
    ''' these functions will take and return plain python data
    the ProfileManager works with model objects'''

    #-------------- THESE ARE IMPLEMENTED --------------

    def __init__(self, pm: ProfileManager):
        self.pm = pm

    def delete_all(self):
        return self.pm.delete_all()

    def create(self, data) -> str:
        p = Profile(**data)
        return self.pm.create(p)
    
    def read_all(self) -> list[dict]:
        r = self.pm.read_all()
        return [p.model_dump() for p in r.profiles]

    #============= TODO: IMPLEMENT THESE==============

    #----------- READS -----------

    def read(self,query:dict={}) -> list[dict]:
        '''read profile by query'''
        pq = ProfileQuery(**query)
        pcs = self.pm.read(pq)
        return [p.model_dump() for p in pcs.profiles]

    def read(self,query:dict={}) -> list[dict]:
        '''read profile by query'''
        pq = ProfileQuery(**query)
        pcs = self.pm.read(pq)
        return [p.model_dump() for p in pcs.profiles]

    def read_by_id(self, id: str) -> dict:
        '''read profile by id'''
        p = self.pm.read_by_id(id)
        return p.model_dump() if p else None
    
    def read_by_username(self,username: str) -> list[dict]:
        '''read all profiles by username'''
        pcs = self.pm.read_by_username(username)
        return [p.model_dump() for p in pcs.profiles]
    
    def read_by_profile_name(self,profile_name):
        '''read profile by profile_name'''
        p = self.pm.read_by_profile_name(profile_name)
        return p.model_dump() if p else None
                
    #-------------- UPDATES --------------

    def add_skills(self,pid: str,skills: list[str]) -> int:
        '''add skills to profile'''
        ps = ProfileSkills(skills=skills)
        return self.pm.add_skills(pid, ps)