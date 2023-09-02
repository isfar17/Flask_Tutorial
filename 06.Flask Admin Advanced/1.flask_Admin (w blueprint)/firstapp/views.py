from flask import Blueprint,render_template

firstapp=Blueprint("firstapp",__name__,template_folder="templates/firstapp")#we defined templates folder location
                                                                            #now it will look into the provided location

@firstapp.route("/")
def index():
    return render_template("index.html")

@firstapp.route("/new")
def new():
    return render_template("new.html")


#now templates are no longer in default position. we set templates/firstapp as templates folder
#we now can access them by typing firstapp/index.html or can directly define templates folder like above