# Show Tables in Admin Page
Since we know how to work with admin and to visit the page, we have a little work left to do. That is adding Tables of the Database into the admin panel.
So first we create our basic app:
```python
from flask import Flask

app=Flask(__name__)

@app.route('/')
def index(): 
    return 'hello world'

if __name__=='__main__':
    app.run(debug=True)
```
After that, We have to create our database. So we import ``SQLA lchemy`` and declare our Database. Then we initialize our database. Next, weconfigure its location and ``SECRET_KEY`` and other stuffs. Then we also we create our basic table and name it ``Base``. Furthermore, we create columns for the table such as id which takes Integer and name which takes String. We also set a ``__repr__`` method to define its look when its printed.
```python
from flask_sqlalchemy import SQLAlchemy#importing sql module

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
```
Make sure we create ``db`` variable after initializing our flask ``app``. With that creating, let's go to our shell and run commands.
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
Now we are almost set to go. This is the part we all know. Now we create our Admin panel and initialize it.
```python
#importing the admin module. needs to be installed.
from flask_admin import Admin
#modelview is neccessary to show and view database in admin panel
from flask_admin.contrib.sqla import ModelView

app=Flask(__name__)
admin=Admin()#define
admin.init_app(app=app)#initialization in the server
```
Now, the last part. Let's go down after the Table we created. Here two things to remember:
***
1. In order to show the database, we must do our adding procedure after creating the Tables, or down the code of the Tables.
2. By default admin panel shows default columns. We can change it which we will see later on.
---
Let's add this line :
```python
class Base(db.Model):
    ... ....

#------------Admin Panel Addition----------------------------------

#admin.add_view(ModelView(Classname,session))
admin.add_view(ModelView(Base,db.session))

```
Here, We use our ``ModelView`` class which we imported from ``flask-admin``. Now what ModelView does is that it shows the model or the Table we want to
add in our admin. Also it takes an additional arguement which is a `` database session``. This session is used by Admin to add/delete/update data in our Tables.

So when we run our app and go to ``/admin`` page, we see this:

![admin_view](https://github.com/isfar17/Flask_Tutorial/blob/master/04.Flask%20Admin/2.flask_Admin_Basic%202/images/admin_view.jpg)

Now after that we click on the ``Base`` Tab and see a ``Create`` Menu. We click it and see:

![table_View](https://github.com/isfar17/Flask_Tutorial/blob/master/04.Flask%20Admin/2.flask_Admin_Basic%202/images/second_view.jpg)

Now here we see the ``Name`` Variable we set earlier in our Model/Table. This is the exact same thing. One thing to notice is that there are red starts on them.
Why? That is because we earlier said that it is ``nullable=False`` and so it is indicating that we can't send it empty. After creating a data, means writing a name
if we click Save, we see this picture:

![last_View](https://github.com/isfar17/Flask_Tutorial/blob/master/04.Flask%20Admin/2.flask_Admin_Basic%202/images/third_view.jpg)

This is it. We are ready to go.
