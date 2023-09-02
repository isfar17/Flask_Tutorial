# Creating Many to Many relationship using SQLAlchemy
Let's build our basic app structure :
```python

from flask import Flask,render_template

app=Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")


if __name__=="__main__":
    app.run(debug=True)
```

### The basics of Many to Many relationship
Let's take an example of a supershop. A supershop has many items and the itmes are not just one in quantity. There might be 10 chips packet, or 20 cokes.
And customers come and buy all those things. The noticeable thing is :
***
1. A customer can buy multiple items such as 2 coke and 3 chips.
2. An item can be bought by multiple customers. For example: a coke can be bought by 5 customers.
---
Let's take another example of a social media. A social media has many users and many user can comment on a post. The noticeable thing is :
***
1. A user can comment multiple times in a post.
2. A comment can be commented by multiple users. For example: When we graduate, a lot of users can comment us by saying Congratulations.
---

In both of the cases, we can see there needs to be 2 tables to store the data into the database, but they need to be connected to each other as well. This
is the case of many to many relationship where tabes need to be connected to each other in order to fetch and insert data and relate the data.

In Flask, we can easily create our database and connect them. In the past example we have seen how one to many or one to one relation works. The best way
to create multiple relation is to create a seperate table and link it with the other tables. The three steps are:
***
1. Create two tables and define their datatypes and everything (In our case its ``User`` and ``Comment`` under our blog application database ).
2. Create an ``association table`` or ``helper table``  Where we take the reference of the Tables we want to link to.
3. Inside the Tables add extra relationship column to create connection with the helper table.
---
Now before creating our tables, we have to initialize and setup our database. Lets create and initialize.
```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#Migrate used to migrate the database for further change without losing data
#without losing any data

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False

db=SQLAlchemy(app)
Migrate(app,db)#without setting this , migration commands will not run,commands
                #at commands.txt file.

```
Let's create our 2 tables:
```python
class User(db.Model):

    __tablename__="users"# custom tablenaeme,better with plural form. avoids error
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(150),nullable=False)

    def __repr__(self):#very important because it is the custom way to show things when an object is called.
        return f"{self.name}"

class Comment(db.Model):
    __tablename__="comments"

    id=db.Column(db.Integer,primary_key=True)
    comment=db.Column(db.String(150),nullable=True)
   
    def __repr__(self):
        return f"{self.comment}"

```
Lets go to command line and run commands to initialize and setup database
```
E:\Flask\new\flask_sql_3(many to many)>flask shell
Python 3.11.4 (tags/v3.11.4:d2340ef, Jun  7 2023, 05:45:37) [MSC v.11934 64 bit (AMD64)] on win32
App: app
Instance: E:\Flask\new\flask_sql_3(many to many)\instance
>>> from app import *
>>> db.create_all()
>>>
```
**Note:** We have to open flask shell at the current working directory, otherwise we will get no app found error or similar ones.
Now that we have created our database and no error is seen, we can work on adding data into the tables:
```
>>> user1=User(name="Anthony")
>>> user2=User(name="Jubayer")
>>> user3=User(name="Rahmat")
>>> user4=User(name="Kamal")
>>> db.session.add_all([user1,user2,user3])
>>> db.session.commit()
>>> db.session.add(user4)
>>> db.session.commit()
>>> com1=Comment(comment="first")
>>> com2=Comment(comment="second")
>>> com3=Comment(comment="third")
>>> com4=Comment(comment="fourth")
>>> db.session.add_all([com1,com2,com3,com4])
>>> db.session.commit()
```
Now we can open our database from database viewer or VS Code extension to open database and can see all of our data.
After creating everything, we now need to link the tables together. We have to create a helper/assosication table on top
of the Tables we created. It is because later on we will take the variable and use it inside the Tables, but if we dont define
our helper table before the Tables, we get not found error.
```python
helper_table=db.Table(   "user and comment",#the table name of the helper table
    db.Column("user_id",db.Integer,db.ForeignKey("users.id")),#plular form is the taken from the __tablename__ part
    db.Column("comment_id",db.Integer,db.ForeignKey("comments.id"))   )
```
this table is the connector or associcate table between two databases. there must be a Table created, where Table class takes 3 arguements or more.
``[variable=db.Table("tablename",(columns with parameters)) and more]`` so we define the class or Other Tables first, then we come up and 
imclude the columns. the columns takes a column name(which will be shown in the  associate table)
then the type of data to be stored, then the foreignkey which will link (with column of the table)provided in the relationship column on the other class.

The last part of creating relation is to add to one extra column in all the tables, the column will refer to the helper table.
In ``User`` table we write :
```python
comments=db.relationship("Comment",back_populates="users",secondary=helper_table) #many to many with comment
               #   relationship with Comment table,back populats is used in many to many relationship. secondary
               # is the indication that the secondary table where the relation will be created is helper table      
               # Note here list is being used to store the other instances.
```
Inside of ``Comment`` table we add:
```python
    users=db.relationship("User",back_populates="comments",secondary=helper_table)#many to many with comment
               #   relationship with User table,back populats is used in many to many relationship. secondary
               # is the indication that the secondary table where the relation will be created is helper table      
               # Note here list is being used to store the other instances.
```
Now the whole program looks just like this :
```python
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False

db=SQLAlchemy(app)
Migrate(app,db)

#-----------------------------------------------

helper_table=db.Table(   "user and comment",#the table name of the helper table
    db.Column("user_id",db.Integer,db.ForeignKey("users.id")),#plular form is the taken from the __tablename__ part
    db.Column("comment_id",db.Integer,db.ForeignKey("comments.id"))   )

#------------------------------------------------
#user table.
class User(db.Model):
    __tablename__="users"# custom tablenaeme,better with plural form. avoids error
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(150),nullable=False)
    comments=db.relationship("Comment",back_populates="users",secondary=helper_table) 
    blogs=db.relationship("Blog",backref="users")

    def __repr__(self):#very important because it is the custom way to show things when an object is called.
        return f"{self.name}"

#------------------------------------------------

class Blog(db.Model):
    __tablename__="blogs"
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(150),nullable=False)
    content=db.Column(db.String(500),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"))
    def __repr__(self):
        return f"{self.title}"

#------------------------------------------------
    
class Comment(db.Model):
    __tablename__="comments"

    id=db.Column(db.Integer,primary_key=True)
    comment=db.Column(db.String(150),nullable=True)
    users=db.relationship("User",back_populates="comments",secondary=helper_table)
    def __repr__(self):
        return f"{self.comment}"

#------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


if __name__=="__main__":
    app.run(debug=True)
```

Go to command line. We already have created instances and have added them into the database. So we just want to modify the tables and not lose data.
For that we use Migrate Command in command prompt:
```
>>>E:\Flask\new\flask_sql_3(many to many)>flask db init
Some words and lines
>>>
>>>E:\Flask\new\flask_sql_3(many to many)>flask db migrate -m "created relation between user and blog"
some lines
>>>
>>>E:\Flask\new\flask_sql_3(many to many)>flask db upgrade
some lines
>>>
```
Now we open up our database editor app and can add relation. Or We can do the following:
**Note:** that for the tutorial, I had only shown the upper parts before, but i wrote the entire program and then ran all the commands. So here
is the full commands ive typed:
```
E:\Flask\new\flask_sql_3(many to many)>flask shell
Python 3.11.4 (tags/v3.11.4:d2340ef, Jun  7 2023, 05:45:37) [MSC v.11934 64 bit (AMD64)] on win32
App: app
Instance: E:\Flask\new\flask_sql_3(many to many)\instance
>>> from app import *
>>> db.create_all()
>>> user1=    blogs=db.relationship("Blog",back_populates="users")  
>>> user1=User(name="Anthony")
>>> user2=User(name="Jubayer")
>>> user3=User(name="Rahmat")
>>> user4=User(name="Kamal")
>>> db.session.add_all([user1,user2,user3])
>>> db.session.commit()
>>> db.session.add(user4)
>>> db.session.commit()
>>> com1=Comment(comment="first")
>>> com2=Comment(comment="second")
>>> com3=Comment(comment="third")
>>> com4=Comment(comment="fourth")
>>> db.session.add_all([com1,com2,com3,com4])
>>> db.session.commit()
>>> user1.comments.append(com1)
>>> user1.comments.append(com2)
>>> db.session.commit()
>>> user1.comments
[first, second]
>>> com3.users.append(user3)
>>> com3.users.append(user2)
>>> db.session.commit()
>>> for comment in user1.comments:
...     print(comment.comment)
...
first
second
```

That is it. We have created our datbase and relations among the tables.
