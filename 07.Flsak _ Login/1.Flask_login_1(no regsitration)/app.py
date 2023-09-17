from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
#This Module is required to use them to work with login
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required
#this module encrypts  password which we will store in our class later.
from werkzeug.security import check_password_hash,generate_password_hash
app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SECRET_KEY"]="secret" #required while working with forms,admin,login most of the cases

db=SQLAlchemy(app)

#we create an object of login manager class. then we initiate the login manager.

login_manager=LoginManager()

login_manager.init_app(app)

#: The name of the view to redirect to when the user needs to log in.
#: (This can be an absolute URL as well, if your authentication
#: machinery is external to your application.)
login_manager.login_view ='login_page' # type: ignore


#-----------------------------------------------------
#we created the table and added some users manually so that we dont 
#have to write registration code here.that will be in the next tutorial

class User(db.Model,UserMixin):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    password=db.Column(db.String(200),nullable=False)

#usually we dont use it.But init will store the cryptic password
#so we use init to manually input values
    def __init__(self,name,password):
        self.name=name
        self.password=generate_password_hash(password)
#the werkzeug will check if both password matches or not
    def check_password(self,password):
        return check_password_hash(self.password,password)
#---------------------------------------------------
# This is a vary important function. this triggers when a User
# enters through login. it checks and pull out the User
# from the table. then if there is a user, it gives the user access
# to restriced pages
#documentation - https://flask-login.readthedocs.io/en/latest/#how-it-works

# You will need to provide a user_loader callback. This callback is used to reload the user object from the user ID stored in the session. It should take the str ID of a user, and return the corresponding user object. For example:

# It should return None (not raise an exception) if the ID is not valid. (In that case, the ID will manually be removed from the session and processing will continue.)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
#-----------------------------------------------
#this is the login route.login_view is set to login_page too.so the app will route the user here while login.
@app.route("/login",methods=["GET","POST"])
def login_page():
    if request.method == 'POST':
        name=request.form.get("name")
        password=request.form.get("password")
        
        user=User.query.filter_by(name=name).first()

        if user is None:
            return redirect(url_for("login_page"))
        
        
        if user.check_password(password) is False:
            return redirect(url_for("login_page"))
        
        login_user(user)
        print("user logged in")

        next = request.args.get('next')
        print(next)
        if next and next[0]=="/":
            return redirect(next)
    
        else:
            '''
            return flask.redirect(next or url_for('index'))
            '''   
            print("no next found")
            return redirect(url_for("view"))
    #first time the method will be get, as no form is being sent, so it will show the template down below. later it will
    #work fine    
    return render_template("login_page.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

#-----------------------restricted pages---------------------------
#routing normally to pages

@app.route('/restricted',methods=['GET','POST'])
@login_required
def restricted():
    return "hello world! This is a restriced area. Go to /login to log into the website "

@app.route('/another',methods=['GET','POST'])
@login_required
def another_func():
    return "hello User! This is a another restrict area. Go to /login to log into the website "

@app.route('/',methods=['GET',"POST"])
def index():
    return "hello world! Go to '/login' to log into the website "



#a restricted page cant be seen without login
@app.route("/view",methods=['GET',"POST"])
@login_required
def view():
    return render_template("view.html")

#------------------------------------------------
if __name__=='__main__':
    app.run(debug=True)
    
'''
127.0.0.1 - - [17/Sep/2023 13:35:40] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [17/Sep/2023 13:35:44] "GET /restricted HTTP/1.1" 302 -
127.0.0.1 - - [17/Sep/2023 13:35:44] "GET /login?next=/restricted HTTP/1.1" 200 -
user logged in
/restricted
127.0.0.1 - - [17/Sep/2023 13:35:47] "POST /login?next=/restricted HTTP/1.1" 302 -
127.0.0.1 - - [17/Sep/2023 13:35:47] "GET /restricted HTTP/1.1" 200 -
'''