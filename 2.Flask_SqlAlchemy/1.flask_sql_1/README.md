# SQLALCHEMY BASICS

Let's dive into the code directly. Here we must remember some of the points down below :

***
1. Flask app can be attached to most of the databases out there using configuration.
2. By default flask has a package named ``flask_sqlalchemy`` which takes care of all the sql related work and we just write python code and execute them automatically
3. All the Table we create are created in class form.
4. Database has to be initialized or to be created before running the app, or the app will crash.
---
So now in our python file, we write code like down below :
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
    
@app.route('/')
def index(): 
    return 'hello world'
```
If we run the app, we will see ``'hello world'`` in the browser. Now that we have imported SQLAlchemy class, we automatically have imported all the functionalities
of database work. Now we have to create our SQLalchemy class's object, with which will access all the functionalities of SQLalchemy.
**Note** That we must and must create object after creating the app. Lets work :
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"#configure location

db=SQLAlchemy(app)#calling
    
@app.route('/')
def index(): 
    return 'hello world'
```
**Note** Since we are creating a datbase instance/object we must specify where would be the location. So we use 
```python
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"
```
to configure location. Its very important to notice that since we are using ``sqlite`` we use 3 '/' sign to define the path. But if we would use
just mysql or others we would use ``mysql://username:password/databasename_and_location`` in this format.

After everything is ok, we go to command prompt. We have to go the same location where the ``app.py`` is. Since it will run the app, we will work here.
In the command prompt we set our flask app and start our flask shell:
```
e:\Flask\Flask_Tutorial\2.Flask_SqlAlchemy\1.flask_sql_1>set FLASK_APP=main.py
e:\Flask\Flask_Tutorial\2.Flask_SqlAlchemy\1.flask_sql_1>flask shell
Python 3.11.4 (tags/v3.11.4:d2340ef, Jun  7 2023, 05:45:37) [MSC v.1934 64 bit (AMD64)] on win32
App: main
Instance: E:\Flask\Flask_Tutorial\2.Flask_SqlAlchemy\1.flask_sql_1\instance
>>>
```
A flask folder will be created automatically and there will be a databse file named ``database.db``. After that we import our db and create database.
```
>>> from main import *
>>> db.create_all()
>>>  
```
If we see nothing, we can make sure everything is working fine. If there is an error, we can lookup online or in the other folders in this tutorial folder to
see what might be the mistake. Now since we have created a database, there should be a table too. The format is :
```python
class Table_name(db.Model):#we inherit db.Model as the base class to use its functionalities.
    __tablename__="thename" #this line can be avoided, its the custom way to set the table name in database
    variable=db.Column(other stuffs)
```
Lets create a proper Table :
```python
class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(150),nullable=False)

    def __repr__(self):
        return f"{self.id} -> {self.name}"
```
The repr method determines how the class will look when it wil be printed. More about this function in python basics.
Now ``primary_key`` variable is the automatic increasing variable. It will set the first data as 0. Then the next data as 1 and so on. The String class takes string
as its input, the Integer takes integer, ``nullable`` makes sure the data input there must be valid not a ``None`` or empty string.

Now if we go to command prompt and write the commands again, it will create a table inside the database.Next we try to create a user in the flask shell.
After that we will add it into the table,and commit in the database.
**Note**
***
1. A data must be added into database using db.add() or db.add_all([data in list form])
2. A data must be commited to add into the database, or else the data insertion will fail
---
So keeping that in mind, lets go and work:
```
>>> from main import *
>>> db.create_all()    
>>> user1=User(name="Jubayer")
>>> db.session.add(user1)
>>> db.session.commit()
>>> User.query.all()
[1 -> Jubayer]
```
Here query method is the way to see data in the table. We have queried all the data by ``query.all()`` method. More on CRUD functionalities of flask database in
online.

Since flask has been updated, its not easier anymore to add data into flask database by just typing python command into the python file like past. There is a
new way to do so. In our ``app.py`` file we add a little bit modification. At first we initialized the app from the shell. Now we will add a line under
db variable:
```python
db.init(app)#passing app as the target
```
And then down below we will add the data with a with block(i know its confusing):
```python
with app.app_context():
    user1=User(name="Bablu") 
    db.session.add(user1)
    db.session.commit()
    print("Successfully added")
```
``app.app_context()`` allows us to use database and CRUD functionalities outside of app and in the python file directly. 
**Note** We dont have to initialize the datbase more than once. so the ``db.init(app)`` line should be deleted after running the file once.
