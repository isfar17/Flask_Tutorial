from project import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
#this is the user database, where we store our user data and password in cryptic form(werkzeug does it)
class User(db.Model,UserMixin):#usermixin is  included to tell flask to look for users here
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    password=db.Column(db.String(200),nullable=False)
    
    def __init__(self,name,password):
        self.name=name
        self.password=generate_password_hash(password)