from datetime import datetime
from functools import wraps
from flask import Blueprint, current_app, flash, redirect, render_template, abort, request, url_for
from flask_login import current_user, login_required

from accounts.data.user_api import UserAPI
from profiles.data.profile_api import ProfileAPI

profiles = Blueprint('profiles', __name__,
                        template_folder='templates')

from typing import cast

def get_um() -> UserAPI:
    """A type-hinted getter for the ProfileManager."""
    return cast(UserAPI, current_app.um)

def get_pm() -> ProfileAPI:
    """A type-hinted getter for the ProfileManager."""
    return cast(ProfileAPI, current_app.pm)

@profiles.post('/profiles/delete/all')
def delete_all():
    ''' for testing '''
    
    n = get_pm().delete_all()
    return f"deleted {n} profiles"

@profiles.get('/profiles/')
def read_profiles():

    profs = get_pm().read_all() 

    # TODO: implement profiles.html
    return render_template('profile_list.html',profs=profs)

#======================= TODO: IMPLEMENT THESE ===========

@profiles.route('/profiles/create', methods=['GET','POST'])
def create_profile():
    '''
    on GET, serve profile create form
    on POST, get username and profile_name from form
    
    if username is not valid, flash a message and redirect here
    else create the profile and redirect to the new profile page
    '''
    
    if request.method == 'GET':
        return render_template('profile_create.html')
    else:  # POST
        # check if profile name is taken
        if request.form.get('profile_name'):
            existing_profile = get_pm().read_by_profile_name(request.form.get('profile_name'))
            if existing_profile:
                flash('Profile name already taken')
                return redirect(url_for('profiles.create_profile'))
        # check if username is valid
        if request.form.get('username'):
            existing_user = get_um().read({'username': request.form.get('username')})
            if not existing_user.get('users'):
                flash('Username not found')
                return redirect(url_for('profiles.create_profile'))
        
        username = request.form.get('username')
        profile_name = request.form.get('profile_name')
        pm = get_pm()

        print(request.form)

        try:
            result = pm.create(request.form)
        except Exception as e:
            print(e)
            flash(str(e))
            return redirect(url_for('profiles.profile_create'))
        else:
            un = request.form.get('username')
            flash(f"Created profile {un}")
            return redirect(url_for('profiles.profile', profile_name=profile_name))
        


@profiles.get('/profiles/<profile_name>')
@login_required
def profile(profile_name):
    '''get profile by profile name
    render profile_view with profile data
    profile view should:
        give profile name and username in a table
        show a list of skills
        have a form that allows you to add skills
        the form should have a hidden input with value equal to the profile id}
    '''  
    
    existing_profile = get_pm().read_by_profile_name(profile_name)
    
    if existing_profile:
        # Assuming existing_profile is a Profile object
        return render_template('profile_view.html', profile=existing_profile)
    else:
        return redirect(url_for('profiles.read_profiles'))  # Redirect if not found
    '''
    p = get_pm().read_by_profile_name(profile_name)

    # wrong user and not an admin
    if not (current_user.username == p.get('username') and current_user.admin):
        return "Forbidden", 403

    ps = current_app.pm.read({'profile_name':p.get('profile_name')})
    ps = ps.get('profiles')

    if not ps: #profile does not exist
        flash('profile not found')
        return redirect(url_for('profiles.profile_view', profile_name=profile_name))

    p = ps[0]

    if request.method == 'GET':
        return render_template('profile_view.html', p=p)
    
    pid = p.get('id')
    result = current_app.pm.update(pid,request.form)

    if result:
        flash(f"Updated profile")
        return redirect(url_for('profiles.profile_view', profile_name=p.get('profile_name')))
    else:
        flash('no updates applied')
        return redirect(url_for('profiles.profile_view', profile_name=p.get('profile_name')))
    '''
    
"""
@accounts.get('/users/{username}/profiles/)
def get_user_profiles(username):
   ''' get profiles by username 
   show a listing in a table
   THIS ENDPOINT GOES IN accounts.routes'''
"""

@profiles.post('/profiles/<profile_name>/add-skill')
def add_skill(profile_name):
    ''' add skill from form
    form should have profile_id and skill
    add skill to profile skills and redirect back to the profile'''
    p = get_pm().read_by_profile_name(profile_name)
    pid = p.get('id')
    skill = request.form.get('skill')
    n = get_pm().add_skills(pid,[skill])
    flash(f"added {n} skills")
    return redirect(url_for('profiles.profile', profile_name=profile_name))