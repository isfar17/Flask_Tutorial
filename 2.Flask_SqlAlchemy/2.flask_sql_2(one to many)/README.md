# Creating a relationship
Since we know how to create a database and table. So if we can now easily create a relation! Let's go and create models
and relationship. First we create Two models in our python ``app.py`` file:
```python
from flask import Flask,render_template
#importing the library
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

#we have to define app configuration for the databse before
#we define the db varibale
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False

#initializing the object of database
db=SQLAlchemy(app)

#creating basic model
class Owner(db.Model):
    user_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(70),nullable=False)

class Pet(db.Model):
    pet_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(70),nullable=False)


@app.route("/")
def index():
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)
```
This is a very basic thing. We know that a pet animal has an owner. But an owner can have multiple pets such as
two dogs/a dog and a cat. So if we can relate them through datbase, its done. Now we need to learn 2 points:
***
1. The Parent class which will relate to the Child class will use ``db.relationship`` column in It's Table.
2. The Child class which will relate to the Parent class will use ``db.Foreignkey()`` class under `db.Column()` column in It's Table.
---
Now inside the owner table, we create a ``pet`` variable and write the code written down below:
```python
pets=db.relationship("Pet",backref="pet_owner")
```
Here,while using one to many or one to one relationship, the parent class we will use ``name= db.relaionship("Classname",backref="anyname")``
.The backref will create a fake column for sqlite itself to indicate the relation with the sub class, means Child Model 
if we use the pets variable then it wil return us a list of the names of the pet owner linked to. Then in the child class we add:
```python
owner=db.Column(db.Integer,db.ForeignKey("owner.user_id"),nullable=True)
```
The child class is simple but will use a foreignkey which will link the pet with the owner. Here we are using owners user id as the foreignkey for pet.
Owners can use their pets variable to access the child class. ``db.Column()`` takes the first arguement as the type of the data it wil save. Then in the
next part it will take the the ``ForeignKey`` class which will take the ``'parentclass.columnname'`` as its arguement. There might be SQL KEY MAP error
which causes because of the similarities in the names of columns in two tables. Make sure the columns are different.

