from .user_manager import UserManager
from .user_models import *

#conn_str = "mongodb+srv://student123:student123@cluster0.n5ntvo6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
#um = UserManager(conn_str)

class UserAPI:

    def __init__(self, user_manager: UserManager):
        self.um = user_manager

    def delete_all(self) -> int:
        return self.um.delete_all()

    def create(self, user: dict ) -> str:
        '''takes an unvalidated dict, validates, and passes dict to UserManager for insertion'''

        u = User(**user).model_dump()
        return self.um.create(u)

    def read_by_id(self, uid: str ) -> dict:
        '''reads, validates, and returns dict'''

        u = self.um.read_by_id(uid)

        if u:   
            return User(**u).model_dump()
    
    def read_all(self) -> dict:

        us = self.um.read_all()
        return UserCollection(users=us).model_dump()
    
    def read(self, query: dict ) -> dict:

        q = UserQuery(**query)
        us = self.um.read(q.model_dump())
        return UserCollection(users=us).model_dump()
    
    def update(self,id:str,update:dict) -> int:

        u = UserUpdate(**update)
        n = self.um.update(id,u.model_dump())
        return n
    
    def delete_by_id(self,id:str) -> int:

        return self.um.delete_by_id(id)

