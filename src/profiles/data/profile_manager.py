from .db_manager import DBManager
from profiles.data.profile_models import *   
 

class ProfileManager:
    '''
    The profile manager takes and returns model objects
    The DBManager works with plain python objects'''

    #================ THESE ARE IMPLEMENTED ================

    def __init__(self, dbm: DBManager):
        '''connect to db server and set self.col'''
    
        self.dbm = dbm
        self.dbm.create_index("profile_name")

    def delete_all(self):
        '''delete all profiles'''

        return self.dbm.delete_all()

    def create(self, p: Profile):
        '''create profile'''

        return self.dbm.create(p.model_dump())
    
    def read_all(self) -> ProfileCollection:
        '''read all profiles'''

        r = self.dbm.read_all()
        return ProfileCollection(profiles=r)
    
    #=================IMPLEMENT THESE================

    #-------------------- READS ----------------------

    def read(self,query: ProfileQuery)->ProfileCollection:
        '''read profile by query'''

        # need to exclude None so that you can query by any of the optional fields
        q = query.model_dump(exclude_none=True)

        ''' now do the query'''
        r = self.dbm.read(q)
        return ProfileCollection(profiles=r)

    def read_by_id(self,id: str) -> Profile:
        '''read profile by id
        p = self.dbm.read_by_id(id)
        return Profile(**p) if p else None'''
        result = self.dbm.read_by_id(id)
        return Profile(**result) if result else None

    def read_by_profile_name(self,name:str) -> Profile:
        '''read profile by profile_name
        results = self.dbm.read({'profile_name': name})
        # Convert cursor to list and get first item if exists
        profiles = list(results)
        p = profiles[0] if profiles else None
        return Profile(**p) if p else None'''
        results = self.dbm.read({'profile_name': name})
        profiles = list(results)
        return Profile(**profiles[0]) if profiles else None

    def read_by_username(self,uname:str) -> ProfileCollection:
        '''read all profiles by username
        p = self.dbm.read({'username': uname})
        return ProfileCollection(profiles=p)'''
        results = self.dbm.read({'username': uname})
        return ProfileCollection(profiles=list(results))

    #---------------- UPDATES ----------------------
        
    def add_skills(self, pid, skills: ProfileSkills):
        '''add skills to profile'''
        self.dbm.add_to_set(pid,'skills', skills.skills)
        updated_profile = self.read_by_id(pid)
        return updated_profile



