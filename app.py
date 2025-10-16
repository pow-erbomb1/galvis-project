
import json

from flask import Flask
from flask_login import FlaskLoginClient, LoginManager

from accounts.data import user_api, user_manager

from accounts.routes import accounts
from accounts.user_login import UserLogin
from flask import Flask, render_template

from profiles.data.profile_api import ProfileAPI
from profiles.data.profile_manager import ProfileManager
from profiles.data.db_manager import DBManager
from profiles.routes import profiles

import config

db_url = config.TEST_CONFIG.DB_URL
db_db = config.USER_CONFIG.USER_DB
db_col = config.USER_CONFIG.USER_COL
g_db = config.GUIDE_CONFIG.GUIDE_DB
p_col = config.GUIDE_CONFIG.PROFILE_COL

app = Flask(__name__)
app.secret_key = 'secret_key'
app.register_blueprint(accounts)
app.register_blueprint(profiles)

umngr = user_manager.UserManager(db_url, db_db, db_col)
app.um = user_api.UserAPI(umngr)

dbm = DBManager(db_url, g_db, p_col)
pmngr = ProfileManager(dbm)
app.pm = ProfileAPI(pmngr)

#Added from Lab 4 starter code------------

app.test_client_class = FlaskLoginClient 
# UserLogin.setup_db(app.um)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    print('loading user')
    return UserLogin.get(user_id)

#-----------------------------------------


@app.route('/')
def hello():
    ''' serve index.html '''

    return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)