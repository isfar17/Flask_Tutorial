from flask import Flask
from flask_sqlalchemy import SQLAlchemy#importing sql module
from flask_migrate import Migrate
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
Migrate(app,db)
#-------------------------------------
#we dont want to lose any data while modifying database
#so we used migration and migrate class to upgrade database
#without losing data, migration tutorial on sqlalchemy
#-------------Database Define------------------------------
#
class Base(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    children=db.relationship("Child",backref="base")#creating relation with child

    def __repr__(self):
        return f'{self.id} - {self.name}'
#---------------------Child--------------------------------

class Child(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    child_name=db.Column(db.String(200),nullable=False)
    base_name=db.Column(db.String(200),db.ForeignKey("base.name"))#child uses foreignkey of base

    def __repr__(self):
        return f'{self.id} - {self.child_name}'
#------Modify Model View--------------------------

class Modify_Base(ModelView):
    form_columns=["id","name","children"]
    column_list=["id","name","children"]



#------------Admin Panel Addition--------------------------

#admin.add_view(ModelView(Classname,session))
admin.add_view(Modify_Base(Base,db.session))
admin.add_view(ModelView(Child,db.session))
#------------------Tutorial-------------------------
''' So what happend was we used classes to view ther relationship based class like
one to many relationship in admin panel. we created relationship betwen base and child class
then we added them to admin. But admin does not shows the relaionship column in the admin panel
we have to modify them to view them. so we modified model view with a new name. means we made a 
child class which derived from modelview. then we included which columns we want to see while inserting
data into database. by including children in base class modified view, now we can add child class in the admin
panel. and also can see the list of child class. and then we declared which columns will be shown in the admin
view panel.so form_columns,column_list does different jobs, for simplycity we made them same.then we added them
to the admin view by the name of the derived class. '''

@app.route('/')
def index(): 
    return 'hello world'

# Before Running the app, Please make sure database is created.commands.txt has the commands 
#to start the databse engine and to connect them with the app
if __name__=='__main__':
    app.run(debug=True)


