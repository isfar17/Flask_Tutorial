from flask import Flask,render_template
#importing the modules
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#Migrate used to migrate the database for further change
#without losing any data

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False

db=SQLAlchemy(app)
Migrate(app,db)#without setting this , migration commands will not run,commands
                #at commands.txt file.


#-----------------------------------------------
'''
this table is the connector or associcate table between two databases.
there must be a Table created, where Table class takes 3 arguements or more.
[variable=db.Table("tablename",(columns with parameters)) and more]
so we define the class or Other Tables first, then we come up and 
imclude the columns. the columns takes a column name(which will be shown in the  associate table)
then the type of data to be stored, then the foreignkey which will link (with column of the target table)
provided in the relationship column on the other class.the foreignkey column elements are:
in the first part we used users.id means users table's id.
'''

helper_table=db.Table(   "user and comment",#the table name of the helper table
    db.Column("user_id",db.Integer,db.ForeignKey("users.id")),#plular form is the taken from the __tablename__ part
    db.Column("comment_id",db.Integer,db.ForeignKey("comments.id"))   )

#------------------------------------------------
#user table.
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

#------------------------------------------------

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

#------------------------------------------------
    
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


#------------------------------------------------


@app.route("/")
def index():
    return render_template("index.html")


if __name__=="__main__":
    app.run(debug=True)