from flask import Blueprint,render_template

firstapp=Blueprint("firstapp",__name__,template_folder="templates/firstapp")

@firstapp.route("/")
def index():
    return render_template("index.html")

@firstapp.route("/new")
def new():
    return render_template("new.html")