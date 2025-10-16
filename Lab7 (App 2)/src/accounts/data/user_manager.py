try:
    from .db_manager import DBManager
except:
    from accounts.data.db_manager import DBManager

from pymongo.errors import DuplicateKeyError

class UserManager(DBManager):

    def __init__(self, conn_str:str, db, col):
        '''connect to db server and set self.col'''

        super().__init__(conn_str, db, col)
        self.col.create_index("username", unique=True)

    def create(self, u):

        try:
            uid = super().create(u)
        except DuplicateKeyError as e:
            print(u)
            raise Exception("username must be unique")
        else:
            return uid