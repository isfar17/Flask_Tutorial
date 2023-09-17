from flask import Flask,render_template,redirect,url_for,request

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required
from werkzeug.security import check_password_hash,generate_password_hash

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SECRET_KEY"]="secret" #required while passing secure data

db=SQLAlchemy(app)

login_manager=LoginManager()

login_manager.init_app(app)
login_manager.login_view ='login'    # type: ignore
#-------------------------------------------------

class User(db.Model,UserMixin):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    password=db.Column(db.String(200),nullable=False)
#same as flask login -1 .
    def __init__(self,name,password):
        self.name=name
        self.password=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)
    
#--------------------------------------------------  
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


#Shows the registraion template
@app.route("/registration",methods=["GET","POST"])
def registration():
    return render_template("registration.html")

#work with registration
@app.route("/registration_process",methods=["GET","POST"])
def registration_process():
    name=request.form.get("name")
    password=request.form.get("password")
    user=User.query.filter_by(name=name).first()
    
    if user:
        return redirect(url_for("registration"))
    else:
        try:
            add=User(name=name,password=password)
            db.session.add(add)
            db.session.commit()
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return redirect(url_for('registration'))
    return redirect(url_for("login"))


@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=="POST":
        name=request.form.get("name")
        password=request.form.get("password")
        
        user=User.query.filter_by(name=name).first()
        
        if user is None:
            return redirect(url_for("login"))
        
        if user.check_password(password) is False:
            return redirect(url_for("login"))
        
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

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

#------------------Basic Page and restricted page----------
#tutorial for login 
@app.route('/',methods=['GET',"POST"])
def index():
    return 'hello world home page go to /registration for registration and in /login for login'

@app.route("/view")
def view():
    return render_template("view.html")

@app.route("/adminpage")
@login_required
def secret():
    return "This is a restriced page ! if you are an user you can see it. go to /view to logout or /logout to logout"



if __name__=='__main__':
    app.run(debug=True)