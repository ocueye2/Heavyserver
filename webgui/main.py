from login.login import add_user, check_user, getpath
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os


add_user("a", "a")
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace with a secure random key

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    # In production, check if the user exists in your database
    return User(user_id) if user_id else None

@app.route('/')
@login_required
def home():
    vms = os.listdir(f"{getpath()}/../vm's/vm/{current_user.id}")
    return render_template('dash.html',vms=vms)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_id = check_user(username, password)
        if user_id != -1:
            user = User(user_id)
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/setup')
def setup():
    """Setup route to render login.html inline for simplicity."""
    return login_template

if __name__ == '__main__':
    app.run(debug=True)
