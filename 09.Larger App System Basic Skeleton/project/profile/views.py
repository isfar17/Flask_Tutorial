from flask import Blueprint,redirect,url_for
from flask_login import login_required,current_user
from project.model import User
profile=Blueprint("profile",__name__,template_folder="templates/profile")

@profile.route("/") #accessed at /profile(since we used url_prefix="/profile" in blueprint registration.)
def index():
    return "Hello! This is the /profile app. all routes are available here"


@profile.route("/<int:id>") # type: ignore
@login_required
def users_profile_lookup(id):
    check=User.query.filter_by  (id=id).first()
    if current_user:
        return f"u are a current user! {check.name}"