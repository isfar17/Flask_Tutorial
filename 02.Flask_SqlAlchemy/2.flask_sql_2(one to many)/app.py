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

#while using one to many or one to one relationship, the parent class
#we will use 
#   name= db.relaionship("Classname",backref="anyname")

#here backref will create a fake column for sqlite itself to
#indicate the relation with the sub class, means Child Model
#if we use the pets variable then it wil return us a list
#of the names of the pet owner linked to
    pets=db.relationship("Pet",backref="pet_owner")


#the child class is simple but will use a foreignkey 
#which will link the pet with the owner. here we are using
#owners user id as the foreignkey for pet.
#owners can use their pets variable to access the child class

class Pet(db.Model):
    pet_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(70),nullable=False)
    owner=db.Column(db.Integer,db.ForeignKey("owner.user_id"),nullable=True)



@app.route("/")
def index():
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)