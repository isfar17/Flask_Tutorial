from flask import Flask
from flask_sqlalchemy import SQLAlchemy#importing sql module

#importing the admin module. needs to be installed.
from flask_admin import Admin
#modelview is neccessary to show and view database in admin panel
from flask_admin.contrib.sqla import ModelView

app=Flask(__name__)
admin=Admin()#define
admin.init_app(app=app)#initialization in the server
#-----App Configuration-----------

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SECRET_KEY"]="SEcreT" #REQUIRED while passing data to website to database


db=SQLAlchemy(app)#initializing

#-------------Database Define------------------------------
#
class Base(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)

    def __repr__(self):
        return f'{self.id} -> {self.name}'

#------------Admin Panel Addition----------------------------------

#admin.add_view(ModelView(Classname,session))
admin.add_view(ModelView(Base,db.session))


@app.route('/')
def index(): 
    return 'hello world'

# Before Running the app, Please make sure database is created.commands.txt has the commands 
#to start the databse engine and to connect them with the app
if __name__=='__main__':
    app.run(debug=True)