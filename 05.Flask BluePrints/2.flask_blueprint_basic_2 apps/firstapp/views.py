from flask import Blueprint,render_template,redirect,url_for

firstapp=Blueprint("firstapp",__name__,template_folder="templates/firstapp")

@firstapp.route("/")
def index():
    return render_template("index.html")

@firstapp.route("/new")
def new():
    return render_template("new.html")

#using url_for to route to another app
@firstapp.route("/takeme_to_second")
def take_me():
    return redirect(url_for("secondapp.index"))