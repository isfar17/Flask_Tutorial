from flask import Blueprint,render_template
from project.model import User#we bring users database here to use them
common=Blueprint("common",__name__,template_folder="templates/common")

@common.route("/")
def index():
    query=User.query.all()#get all the user name and their data
    return render_template("index.html",query=query) #send it to the html file