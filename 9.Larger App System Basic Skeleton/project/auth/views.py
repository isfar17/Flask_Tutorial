from flask import Blueprint,render_template,redirect,url_for ,request# type: ignore
from project import login_manager
from project.model import User
from flask_login import login_user

auth=Blueprint("auth",__name__,template_folder="templates/auth")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))







@auth.route("/")
def index():
    return "Hello! This is the /auth app. all routes are available here"

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/registration")
def registration():
    return render_template("registration.html")

@auth.route("/registraion_process",methods=["GET","POST"])
def registration_process():
    return "Everything about registration will process here"

@auth.route("/login_process",methods=["GET","POST"])
def login_process():
    name=request.form.get("name")
    user=User.query.filter_by(name=name).first()
    if user is None:
        redirect(url_for("auth.login"))
    login_user(user)
    return redirect((url_for('profile.users_profile_lookup',id=user.id))) # type: ignore

@auth.route("/route")
def redirect_user():
    return redirect(url_for('profile.index')) # type: ignore