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
admin.add_view(ModelView(Base,db.session))
admin.add_view(ModelView(Child,db.session))
```
Here we are going to encounter one thing. Let's go to ``flask shell`` and create our Database and Tables:
```
E:\Flask\Flask_Tutorial\4.Flask Admin\2.flask_Admin_Basic 2>flask shell
Python 3.11.4 (tags/v3.11.4:d2340ef, Jun  7 2023, 05:45:37) [MSC v.1934 64 bit (AMD64)] on win32
App: app
Instance: E:\Flask\Flask_Tutorial\4.Flask Admin\2.flask_Admin_Basic 2\instance
>>> from app import *
>>> db.create_all()
>>> db.session.commit()
>>>
```
Now run the app, go to ``/admin`` and we will see this:
![first_view](https://github.com/isfar17/Flask_Tutorial/blob/master/04.Flask%20Admin/3.flask_Admin_(one%20to%20many)/images/first.jpg)

Now we add Some Test Data in our app. But we wil encounter a problem. When we created our Tables, we defined a relationship between them. That is one to many
relationship. But here we are not able to see the relationship column to add ``Child`` object in our ``Base`` class:

![wthout_modify](https://github.com/isfar17/Flask_Tutorial/blob/master/04.Flask%20Admin/3.flask_Admin_(one%20to%20many)/images/without_modify.jpg)

And also in the ``Base`` tab, we can see the data but not their child. How we can modify this so that we can see who is the child of the ``Base`` class and
we also can add ``Child`` in our ``Base`` class?

Well the simpliest answer is to modify the code. Let's go back to our old code:
```python
admin.add_view(ModelView(Base,db.session))
admin.add_view(ModelView(Child,db.session))
```
We all can see that there are 2 views we added. The ModelView class determines how the Tables will be shown and what column will be shown during adding data.
We can modify this class by the following:
***
1. Make a new class and name it a similar name to the class we want to add(ex: we want to change the look of ``Base``, we say ``Modified_Base``.
2. Make the class a derivative  of ``ModelView`` class.
3. Choose what column and what form column to show (will see in a little bit).
---

So below the Tables, we make another class and write this code:
```python
#------Modify Model View--------------------------

class Modify_Base(ModelView):
    form_columns=["id","name","children"]
    column_list=["id","name","children"]
```
So what does this Class do? We have set the ``form_column`` to ``["id","name","children"]`` which means while adding data in our database, we wil be able to
see this columns. And what does ``column_list`` does? Well it does the similar too. But this shows the columns we want to see in our ``Base`` Tab after adding
the data. Now we do one last thing:
```python
admin.add_view(Modify_Base(Base,db.session))
admin.add_view(ModelView(Child,db.session))
```
instead of using the ``ModelView`` class we now are using ``Modify_Base``. Let's save and run our app. Go to ``/admin`` and go to Base Tab we can see:

![column_view](https://github.com/isfar17/Flask_Tutorial/blob/master/04.Flask%20Admin/3.flask_Admin_(one%20to%20many)/images/column_list.jpg)

Here the blue lines are the columns we defined earlier to show. Let's go and add a data:

![form_choice](https://github.com/isfar17/Flask_Tutorial/blob/master/04.Flask%20Admin/3.flask_Admin_(one%20to%20many)/images/form_choice.jpg)

Here we can see the columns we defined earlier. Now we are clear what ``form_choice`` and ``column_list`` does. That's it. we are good to go.
