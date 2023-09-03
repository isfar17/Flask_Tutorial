# How to Add multiple Tables and Modify the look of any Table in Admin Panel
Let's create our app first. We first as usual import our flask application and make our minimal app. Afer that, we also import SQL module. Furthermore, We create
a one to many relationship Table. Lastly we add a normal ``index``  view function.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy#importing sql module
from flask_migrate import Migrate

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SECRET_KEY"]="SEcreT" #REQUIRED while passing data to website to database


db=SQLAlchemy(app)#initializing
Migrate(app,db)
#-------------Parent Database Define------------------------------
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

@app.route('/')
def index(): 
    return 'hello world'

# Before Running the app, Please make sure database is created.commands.txt has the commands 
#to start the databse engine and to connect them with the app
if __name__=='__main__':
    app.run(debug=True)
```
Let's understand our code better. Here we are creating 2 classes. One is Parent class, Another is child class. So as we know what one to many relationship means,
we know that a parnet can have many children. But a child can have one mother. That is the case we are simulating here. in the ``Base`` class, the ``children``
column takes a list of all the objects or the data of the childs that are belonged to or connected to the parent class. Suppose a parent class object has
3 child object related to it. So ``children`` column will store all those child object's reference. After that as usual ``Child`` class has its own columns.
We add an extra column ``base_name`` which basically takes the Foreignkey or in other words the reference of the parent class. We also define which column
and its datatype to be take as the key. It is important.

Many time we do mistake by this:
```python
parent1=-Parent(name="A Parent)
child=Child(name="A child)
#child.base_name=parent #THIS IS WRONG
child.base_name=parent.id #THIS IS Correct, because here we are defining the column and datatype
```
Now we go and add our admin panel:
```python
#importing the admin module. needs to be installed.
from flask_admin import Admin
#modelview is neccessary to show and view database in admin panel
from flask_admin.contrib.sqla import ModelView

...
...

admin=Admin()#define
admin.init_app(app=app)#initialization in the server

... ...

#------------Admin Panel Addition--------------------------

#admin.add_view(ModelView(Classname,session))
admin.add_view(Modify_Base(Base,db.session))
admin.add_view(ModelView(Child,db.session))
```
Here we are going to encounter one thing. Let's
