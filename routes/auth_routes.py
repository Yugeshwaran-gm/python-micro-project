from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required
from utils.auth_utils import AuthUtils

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        print(f"Login attempt with email: {email}")
        
        # Create AuthUtils instance
        auth_utils = AuthUtils()
        
        # Get user and check credentials
        user = auth_utils.get_user_by_email(email)
        
        if user and auth_utils.verify_password(user, password):
            login_user(user)
            print(f"Login successful for user: {email}")
            return redirect(url_for('timetable.dashboard'))
        else:
            if user is None:
                print(f"User not found with email: {email}")
            else:
                print("Password verification failed")
            flash('Invalid email or password')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
