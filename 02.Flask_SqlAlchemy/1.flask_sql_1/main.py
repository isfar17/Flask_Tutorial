from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"#configure location

db=SQLAlchemy(app)#calling

#basic database-------------
class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(150),nullable=False)

    def __repr__(self):
        return f"{self.id} -> {self.name}"
#repr method is used to show how the object will look when it wil be called
    
    
@app.route('/')
def index(): 
    return 'hello world'

'''from the new updates, its not easily accessible to use database outside of the main.py file or outiside of the 
part where db/class is used.simple solution is to use flask shell from correct path. another usage is to use
application context which is a new addition. the first one is showed down. and then next part is written
'''
# e:\Flask\Flask_Tutorial\2.Flask_SqlAlchemy\1.flask_sql_1>set FLASK_APP=main.py
# e:\Flask\Flask_Tutorial\2.Flask_SqlAlchemy\1.flask_sql_1>flask shell
# Python 3.11.4 (tags/v3.11.4:d2340ef, Jun  7 2023, 05:45:37) [MSC v.1934 64 bit (AMD64)] on win32
# App: main
# Instance: E:\Flask\Flask_Tutorial\2.Flask_SqlAlchemy\1.flask_sql_1\instance
# >>> from main import *
# >>> db.create_all()    
# >>> user1=User(name="Jubayer")
# >>> db.session.add(user1)
# >>> db.session.commit()
# >>> User.query.all()
# [1 -> Jubayer]

#Another or the modern way:

#since we have created_database, we dont have to use db.init(app) method to initiate method anymore

with app.app_context():
    user1=User(name="Bablu") 
    db.session.add(user1)
    db.session.commit()
    print("Successfully added")
    
#After running it, if we look inside database we would see our data is added