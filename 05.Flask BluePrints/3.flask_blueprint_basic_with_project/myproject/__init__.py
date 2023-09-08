from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=True
app.config["SECRET_KEY"]="secret#234)"

# database location and other stuffs must be done before initialiazing the db

db=SQLAlchemy(app)

# AT init file, blueprint must be set after defining db


from myproject.firstapp.views import firstapp
from myproject.secondapp.views import secondapp

app.register_blueprint(firstapp,url_prefix="/")
app.register_blueprint(secondapp,url_prefix="/second")

