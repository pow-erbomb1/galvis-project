from flask import Blueprint, flash, redirect, render_template, request, url_for, current_app

#from accounts.data.user_manager import UserManager
#from accounts.data.user_api import UserAPI
from accounts.user_login import UserLogin
from flask_login import current_user, login_required, login_user, logout_user

# # conn_str = "<YOUR ATLAS CLUSTER URI>"
#conn_str = config._DATABASE_URL
#umngr = UserManager(conn_str)
#um = UserAPI()

accounts = Blueprint('accounts', __name__,
                        template_folder='templates')

@accounts.get('/users/')
@login_required
def users():
    if not current_user.admin:
        return "Forbidden", 403
    
    us = current_app.um.read_all()
    us = us.get('users')
    return render_template('users.html', users=us)

@accounts.get('/users/<username>/profiles/')
def get_user_profiles(username):
    '''pm = current_app.pm
    profiles = pm.read_by_username(username)
    return render_template('user_profiles.html', profiles=profiles, username=username)'''
    profiles_result = current_app.pm.read_by_username(username)
    
    if hasattr(profiles_result, 'profiles'):
        profiles = profiles_result.profiles
    else:
        profiles = list(profiles_result) if profiles_result else []
    
    return render_template('user_profiles.html', profiles=profiles)


#ADDED FROM LAB 4 STARTER CODE----------------------------------------------------
@accounts.route('/login', methods=['GET','POST'])
def login():
    '''on GET, serve login page.  on POST, authenticate and login
    use current_app.um to access UserAPI / UserManager
    '''

    if request.method=='GET':
        return render_template('login.html')

    users = current_app.um.read(request.form)

    ''' TODO
    # get username and password from form
    # read users from db by query
    '''    
    print(users)

    if users:
        u = users["users"][0]

        uid = u.get('id')
        un = u.get('username')
        admin = u.get('admin')

        # TODO: get values from u to pass to UserLogin
        #Create userlogin
        u = UserLogin(uid,un,admin)

        login_user(u)
        flash('logged in')
        return redirect(url_for('hello'))
    else:
        flash('login unsuccessful')
        return redirect(url_for('accounts.login'))

@accounts.route("/logout")
@login_required
def logout():
    logout_user()
    flash('logged out')
    return redirect(url_for('hello'))

#-----------------------------------------------------------

@accounts.route('/users/create', methods=['POST', 'GET'])
def create():
    ''' on GET, serve user create form
    on POST, get form data and update'''
    u = {
        'username': request.form.get('username'),
        'password': request.form.get('password'),
        'admin': request.form.get('admin'),
    }

    if request.method == 'GET':
        return render_template('create.html')
    else:

        try:
            result = current_app.um.create(request.form)
        except Exception as e:
            print(e)
            flash(str(e))
            return redirect(url_for('accounts.create'))
        else:
            un = request.form.get('username')
            flash(f"Created user {un}")
            return redirect(url_for('accounts.users'))
    
    #return "create user"

#@accounts.get('/users/')
#def users():
#    return um.read_all()

@accounts.route('/users/<username>', methods=['POST', 'GET'])
@login_required
def view(username):

    if not (current_user.username == username) :
        if not (current_user.admin):
           return "Forbidden", 403
        
    
    ''' on GET, serve populated user update form
    on POST, get form data and update user'''
    us = current_app.um.read({'username':username})
    us = us.get('users')

    if not us:
        flash('user not found')
        return redirect(url_for('accounts.users'))
    
    u = us[0]

    if request.method == 'GET':
        return render_template('view.html', u=u)
    
    uid = u.get('id')
    result = current_app.um.update(uid,request.form)

    if result:
        flash(f"Updated user")
        return redirect(url_for('accounts.view', username=u.get('username')))
    else:
        flash('no updates applied')
        return redirect(url_for('accounts.view', username=u.get('username')))

    #return "view / update users"

@accounts.post('/users/delete/all')
@login_required
def delete_all():
    if not current_user.admin:
        return "Forbidden", 403

    n = current_app.um.delete_all()
    return f"deleted {n} users"

@accounts.post('/users/delete/<username>')
@login_required
def delete(username):

    if not current_user.admin:
        return "Forbidden", 403
    

    data = current_app.um.read({'username':username})
    user = data.get('users', [])
    result = current_app.um.delete_by_id(user[0]['id'])

    if result:
        flash(f"Deleted user")
    else:
        flash(f"User not found")
        
    return redirect(url_for('accounts.users'))