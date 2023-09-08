from flask import Blueprint,render_template



secondapp=Blueprint("secondapp",__name__,template_folder="templates/secondapp")


@secondapp.route("/",methods=["GET","POST"])
def index():
    # one thing im facing here is that i cant use two same html file name
    #in two different app. but functions can be same like this one. here
    # im using index which ive used in first app too
    return render_template("index2.html")


@secondapp.route("/connect",methods=["GET","POST"])
def connect():
    return render_template("connect.html")