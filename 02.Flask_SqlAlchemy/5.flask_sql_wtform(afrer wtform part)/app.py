from flask import Flask, redirect, render_template, url_for, session,flash
#imoprting the form modules
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Email,InputRequired
#importing database moduels and errors
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.config["SECRET_KEY"] = "key"

db = SQLAlchemy(app)
Migrate(app, db)
'''
What is Migration? Basically Migration is a tool or class that keeps track of change in database
and save the changes without losing any data provided before. if we were to write any extra column
in database and we had to change anything, we might end up recreating the database again. so this 
is a very good tool to use to save changes without any problem

The commands to migrate any changes to database are:

>>set FLASK_APP=(appname).py
>>flask db init
>>flask db migrate -m "any message" or just flask db migrate
>>flask db upgrade

we run this everytime there is a change in database
 Note that without initiating Migration(app,db) flask wont find anything and will return error
'''

#creating forms
class TestForm(FlaskForm): #form tutorial in the next part,skip for now to understand how form to database thing works
    name = StringField(label="Enter Name",
                       validators=[InputRequired("Must Put Name")])
    email = StringField(label="Enter Email", validators=[
                        InputRequired("Must Put Email"), Email()])
    choice = SelectField(label="Choices", choices=[("Python", "Python"),("Java", "Java"), ("C++", "C++")], 
                            validators=[InputRequired("Must Put choices")])
    submit = SubmitField()
#creating database------------------------------------
class TestDB(db.Model):

    user_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(150),nullable=False)
    email=db.Column(db.String(200),nullable=False,unique=True)
    choice=db.Column(db.String(150))
    
    def __init__(self,name,email,choice):
        self.name=name
        self.email=email
        self.choice=choice
    
    def __repr__(self):
        return f"{self.name} -> {self.email}"
    
#----------------------------------------------------------
@app.route("/",methods=["POST","GET"])
def index():
#without flask form, we had to route another function to process the data
#and we would get data by typing request.form.get("name") instead of form.name.data
    form=TestForm()
    if form.validate_on_submit():#tutorial down below
        session["name"]=form.name.data
        session["email"]=form.email.data
        session["choice"]=form.choice.data
        try:
            save_data=TestDB(name=form.name.data,email=form.email.data,choice=form.choice.data)
            db.session.add(save_data)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            print(type(e))
            db.session.rollback()
            flash("Email Must be Unique!")
            return redirect(url_for("index"))
        return redirect(url_for("show_val"))
    
    return render_template("index.html",form=form)
'''
Now we define form/any variable with the created Form class. then we will
check if the form is validate by internally using validators. if it is
then we will store the values into session.or else it will create a form
instance and give user an html form to fillup data. after getting the
values  we can directly put them into database but we want to show what
we have put. so we will use session.

session:
it is a special thing which will store the values of provided data until
user is online. in other words, users session time is limited time it will
store the value, if user leaves site, or logouts, sesions gets deleted, and all
the variables get deletd.

so now by using session we can access the session variable from the entire app
starting from functions to even html files. thats why we are using to store it
'''
@app.route("/show")
def show_val():
    query=TestDB.query.filter_by(email=session["email"]).first()#will return none if no form is filled
    print(query)
    print(session["email"])
    return render_template("query.html",query=query)



if __name__=="__main__":
    app.run(debug=True)

