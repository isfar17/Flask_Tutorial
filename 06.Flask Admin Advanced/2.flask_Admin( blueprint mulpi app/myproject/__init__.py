from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_migrate import Migrate
#this admin module is imported into __init__.py file because here everything is
#configured and initialized. so its the best use to configure and setup or modify everything here

app=Flask(__name__)
admin=Admin()
admin.init_app(app)
'''if we know about blueprints, we know that we create separate apps and then we use them with blueprint variable
declared within their folders python file. then we register them into the project __init__ file or main.py file() in
case of single app). Then we import Admin and admin.view and models from model.py file to view them into
/admin  route. we now can modify admin views unlike previous admin tutorial'''

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=True
app.config["SECRET_KEY"]="secrettttt"

# database location and other stuffs must be done before initialiazing the db


db=SQLAlchemy(app)
Migrate(app,db)


# AT init file, blueprint must be set after defining db

from flask_admin.contrib.sqla import ModelView
import myproject.model as model #more on notes.txt file about circular import error


admin.add_view(ModelView(model.SecondClass,db.session))#can do other stuffs such as modify in model.py and
                                                        #import them here without circular import
admin.add_view(model.Modified_Fun(model.Fun,db.session)) #Modified in model.py file



from myproject.firstapp.views import firstapp
from myproject.secondapp.views import secondapp

app.register_blueprint(firstapp)
app.register_blueprint(secondapp)

