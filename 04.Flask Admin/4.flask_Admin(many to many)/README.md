# How to work with Many to Many relationship in Flask Admin
We pretty much know about SQLAlchemy and Database operations. We also know that by using ADMIN, we can easily accomplish our CRUD operations easily. Now we are
dealing with Many to Many relationship in flask. Since we *have to show* all the Tables in our Admin panel, its important to understand how to show Columns 
and Form columns in case of many to many relationship.

**STEP 1:**

Let's create our basic app. We will define ``SQLALCHEMY_DATABASE_URI`` and setup ``SECRET_KEY`` and also ``Migrate``. Then we will initiate our ``Admin`` and
our basic function to check our app is working or not.
```python
from flask import Flask,render_template
#importing the modules
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False
app.config["SECRET_KEY"]="secrethehe"
admin=Admin()
db=SQLAlchemy(app)
Migrate(app,db)#without setting this , migration commands will not run,commands
                #at commands.txt file.
admin.init_app(app)#without it /admin wont be able to show the view

@app.route("/")
def index():
    return render_template("index.html")

#/admin will show the admin page
if __name__=="__main__":
    app.run(debug=True)
```
Before running the app, we must create our database, or else our app will crash. So let's jump into the current working directory terminal and run our flask shell
```
E:\Flask\new\flask_sql_3(many to many)>flask shell
Python 3.11.4 (tags/v3.11.4:d2340ef, Jun  7 2023, 05:45:37) [MSC v.11934 64 bit (AMD64)] on win32
App: app
Instance: E:\Flask\new\flask_sql_3(many to many)\instance
>>> from app import *
>>> db.create_all()
>>>
```
Now let's run our app. We will see our ``index.html`` file. Don't forget to setup ``templates`` directory.

**STEP2 :**

Now we create our Models and make relationships. For practicing more, we are using both one to many and many to many relationships. So our Model is:
***
1. Our database has 3 Models. ``User``, ``Comment`` and ``Blog``. So we have 3 models and they are linked to each other.
2. ``User`` and ``Comment`` are related as many to many relationship. Because a user can comment muliple comments. and a  comment can be done by many users.
3. ``Blog`` and ``User`` are linked as one to many relationship. A user can have many blogs of his own.
---
So now we will start our coding. Let's build our Models and relate them with each other:
```python

helper_table=db.Table(   "user and comment",#the table name of the helper table
    db.Column("user_id",db.Integer,db.ForeignKey("users.id")),#plular form is the taken from the __tablename__ part
    db.Column("comment_id",db.Integer,db.ForeignKey("comments.id"))   )

#-----------------User Table-------------------------------

class User(db.Model):
    __tablename__="users"# custom tablenaeme,better with plural form. avoids error
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(150),nullable=False)
    comments=db.relationship("Comment",back_populates="users",secondary=helper_table) #many to many with comment
               #   relationship with Comment table,back populats is used in many to many relationship. secondary
               # is the indication that the secondary table where the relation will be created is helper table      
               # Note here list is being used to store the other instances.
    blogs=db.relationship("Blog",backref="users") #one to many with blog
            #here backref is used because its the parent class in one to many/one.
            # backref will create back reference in the child class it is linked to


    def __repr__(self):#very important because it is the custom way to show things when an object is called.
        return f"{self.name}"

#--------------------Blog Table----------------------------

class Blog(db.Model):
    __tablename__="blogs"
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(150),nullable=False)
    content=db.Column(db.String(500),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id")) #one to many with user
    #in the one to one/many case, the child class uses foreignkey column to link with the 
    #parent class.here users.id is the column we will link blog to user.
    def __repr__(self):
        return f"{self.title}"

#--------------------Comment Table--------------------------
    
class Comment(db.Model):
    __tablename__="comments"

    id=db.Column(db.Integer,primary_key=True)
    comment=db.Column(db.String(150),nullable=True)
    users=db.relationship("User",back_populates="comments",secondary=helper_table)#many to many with comment
               #   relationship with User table,back populats is used in many to many relationship. secondary
               # is the indication that the secondary table where the relation will be created is helper table      
               # Note here list is being used to store the other instances.
    def __repr__(self):
        return f"{self.comment}"

```
Here some things needs to be reviewd. So we created ``helper_table`` to create a many to many relation between ``Blog`` and ``Comment``. So in the table, we
take the ``id`` column of ``User`` and ``users`` column from ``Comment``. We set relationship between them by typing:
```python
db.Column("user_id",db.Integer,db.ForeignKey("users.id")),#plular form is the taken from the __tablename__ part
db.Column("comment_id",db.Integer,db.ForeignKey("comments.id"))   )
```
Here we are creating Integer column, and take the ForeignKey of ``users.id`` means the ``id`` column's reference. We do this for both Tables. 

On the other hand, we use ``db.relationship`` column in both of the ``User`` and  ``Comment`` column, to set ``MANY TO MANY`` relationship. We know we
wil use this column when we want to create a ``MANY TO MANY`` relation between 2 Tables.

Then we have set one to many relationship with ``Blog`` and ``User``. We use ``db.relationship`` in the parent ``User`` table and ``ForeignKey`` in the child
``Blog`` column. That's it. We have created relationships. Now we run migrate command and finish up our database upgrade setup. 

Next we need to add the Models in our Admin panel. So we use 
```python
admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Blog,db.session))
admin.add_view(ModelView(Comment,db.session))
```
And run the app. Let's see our first look:

![first](https://github.com/isfar17/Flask_Tutorial/blob/master/04.Flask%20Admin/4.flask_Admin(many%20to%20many)/image/first.jpg)

But there is a catch. We can add data in our Model, But  we cannot actually create relationships among them. Because we are not able to see other columns in our
form:

![without_modify](https://github.com/isfar17/Flask_Tutorial/blob/master/04.Flask%20Admin/4.flask_Admin(many%20to%20many)/image/without_modify_user.jpg)

And after adding them, we can't see its relationship with ``Blog`` and  ``Comment``:

![no_Relation](https://github.com/isfar17/Flask_Tutorial/blob/master/04.Flask%20Admin/4.flask_Admin(many%20to%20many)/image/no_relation_data.jpg)

So now, we know what to do. As usual, we have to edit the look of ``ModelView`` through a class, and define which ``columns`` to show while filling data and
which ``columns`` to show in the view.

```python
#modifying the modelview by custom rules
class Modified_User(ModelView):
    form_columns=["name","comments","blogs"]
    column_list=["id","name","comments","blogs"]

class Modified_Blog(ModelView):
    form_columns=["title","content","user_id"]
    column_list=["id","title","content","user_id"]

class Modified_Comment(ModelView):
    form_columns=["comment","users"]
    column_list=["id","comment","users"]

```
So now we have defined what to show while filling data and what to show in the view. Lets go and see what has changed. For the ``User`` Table:

![user](https://github.com/isfar17/Flask_Tutorial/blob/master/04.Flask%20Admin/4.flask_Admin(many%20to%20many)/image/form_choice.jpg)

Here blue mark indicates the modified view. And after adding any data, we can see in our view this:

![view](https://github.com/isfar17/Flask_Tutorial/blob/master/04.Flask%20Admin/4.flask_Admin(many%20to%20many)/image/column_list.jpg)

Again, blue mark indicates the modification. Now if we want to create relation between ``Comment`` and  ``User``, we can add them:

![data_add](https://github.com/isfar17/Flask_Tutorial/blob/master/04.Flask%20Admin/4.flask_Admin(many%20to%20many)/image/many_to_many_users.jpg)

And in case of ``Comment`` we see:

![data_comment](https://github.com/isfar17/Flask_Tutorial/blob/master/04.Flask%20Admin/4.flask_Admin(many%20to%20many)/image/many_to_many_comments.jpg)

That is it. We are good to go.
