from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime

app=Flask(__name__)

#we have to define app configuration for the databse before
#we define the db varibale
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False
app.config["SECRET_KEY"]="hi" #its very important to set secret key while working with data passing between site and server
#or else error will throw
#initializing the object of database

db=SQLAlchemy(app)

#creating basic model

class Base(db.Model):
    nid=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(25),nullable=False,unique=True)
    text=db.Column(db.String(200),nullable=False)
    date=db.Column(db.Date,default=datetime.utcnow())

    def __init__(self,text,name):
        self.name=name
        self.text=text
    

    def __repr__(self):
        return f"{self.nid} -> {self.name} -> {self.text[:5]}.. -> {self.date}"
    
#repr method is used to show how the object will look when it wil be called
#in the above case [1 -> Jamal -> errfs... -> 12/8/23]

@app.route("/")
def index():
    return render_template('index.html') 
#using basic form to function data passing method
@app.route("/view",methods=["GET","POST"])
def view():
    if request.method=="POST": #when it runs for the first time it returns 0 as false, so the last line will execute
        
        name=request.form.get("name")#request takes the data from html form name variable to function
        text=request.form.get("text")
        print(name,text)
        try:
            entry=Base(name=name,text=text) 
            db.session.add(entry)
            db.session.commit()

        except:
            print(f"{name} is already in use!Try different Name! ")
            return render_template("index.html") #will go to this page if the name provided already exists in datbase
        dic={"name":name,"text":text}
        return render_template("view.html",dic=dic)
    else:
        return "403 ERROR"
'''
wwewew weewewwe
wwewew is already in use!Try different Name!
127.0.0.1 - - [20/Aug/2023 01:10:43] "POST /view HTTP/1.1" 200 -
'''

if __name__=="__main__":
    app.run(debug=True)