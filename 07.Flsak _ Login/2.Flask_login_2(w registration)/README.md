# Registration and User login with Flask
We previously had seen how ``flask_login`` works. In order to work with ``flask_login``, we had to create new user beofre running the app, or in the database
so that we can have pre registered user in our database. From there, we could use user and password value and log in. But in a real life project, There are 
no pre-built username and password. A new user has to register in the site, and then can log in easily in the webpage. Now we will create a simple registration
form with flask and embed it with flask login. 

First we create our app as usual, with ``templates`` directory. Next we make our basic app code:
```python
from flask import Flask
app = Flask(__name__)

@app.route('/',methods=['GET',"POST"])
def index():
    return 'hello world home page go to /registration for registration and in /login for login'

if __name__=='__main__':
    app.run(debug=True)
```
Then we step by step import all the modules:
```python
from flask import Flask,render_template,redirect,url_for,request

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required
from werkzeug.security import check_password_hash,generate_password_hash
```
Here ``SQLAlchemy`` will work with database and so on. ``SQLAlchemyError`` will show any error that will occur while registering or loggin in. ``LoginManager`` and ``UserMixin`` will be used for login. Then lastly ``werkzeug`` will be used for sequrity and encrypt/decrypt password.

Next we setup our configuration:
```python
app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SECRET_KEY"]="secret" #required while passing secure data

db=SQLAlchemy(app)

login_manager=LoginManager()

login_manager.init_app(app)
login_manager.login_view ='login' 
```
``SQLALCHEMY_DATABASE_URI`` will set where the database file would be in. Then we create our database instance ``db``. Then ``login_manager``. Also we set
our ``login_view``. Thus we finish setting up our configuration for flask app. 

**Database Creation :**

This is the ``User`` Table. We will use this Table as our ``user database``. So we have taken ``UserMixin`` class as super class to point
flask to come here while loggin in and registering a new user. We also hash password and make check password to work with ``werkzeug`` for security
purpose.

```python
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
```

Now we have to make our registraion and login functions. First we make our registraion functions (because there are two). Then we will copy/paste our 
previous ``login`` code from our last tutorial.
Let's do it.

```python
#route to registration form
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
```
And let's go to our basic ``registration.html`` file:

```html+jinja
{% extends 'base.html' %}

{% block title  %}Registration{% endblock title  %}

{% block body %}
    <div class="container">
        This is the body <br>
        Please fill up your registraion form <br>
        <br>
    <!-- the url_for()  recognises the function to be called and gets to it. it will return whatever inside it is -->
        <form action="{{url_for('registration_process')}}" method="POST"> 
            <!--the url for this file is set to registration_process where data will be processed to make a user-->
            Name : <input type="text" name="name" > <br> <br>
            Password : <input type="password" name="password" > <br> <br>
            Submit : <button type="submit">Submit</button>

        </form>
    </div>
{% endblock body %}
```
Now let us break things into pieces to understand everything in detail. First of all, ``registration`` function will redirect user to the ``registration`` 
page. There user can put their data into the ``registration.html`` file. Then this file will take data and any function will be able to acccess the form 
data.

```python
name=request.form.get("name")
password=request.form.get("password")
user=User.query.filter_by(name=name).first()

if user:
    return redirect(url_for("registration"))
```
Here we first fetch ``name`` and ``password`` value. Then we have to check if these are new. How? We check that if there are any user exists with that
name. If exists, means there cannot be any new user created. So we have to redirect user to registration form again. So we redirect the user to 
``registration`` form again.

Second part:

```python
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
```
If the user does not exist, we have to create a new user. So we make an object of ``User`` Model. Then we add the user by ``db`` command. Here two things
might happen:

1. The user will be added successfully
2. The user will make a mistake, such as
     1. Putting a name that exceeds limit
     2. Provided name/password might be null (for malicious perpose)
     3. maybe provided a unique name etc.

So we have to be prepared for all the situations out there. So we use ``try`` block. First it will try to add, if it fails, the database operation will
fail. So ``flask`` will show errors. In order to avoid that error, we use ``except`` block. We say if there is an error occurs, which will be found by
``SQLAlchemy``, we can print to check what type of error we got. We also have used a command ``db.session.rollback()``. This command says that it
will revert everything it was trying to do. Means the addition or registraion process will terminate. Lastly, if it fails then next line will execute
means to redirect user to registraion page again. Or else ``except`` block won't run and in ``try`` block, it will execute and add user to database.

Next is our login. So after completing registraion, site will redirect user to login again. So we have to make a ``login`` function and ``login.html`` file.
Let's go and work.

```python
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
```
Here we try to login user as usual. This is from previous tutorial, Here we have said if user exists, we login user and send him where he wanted to go with
`next`. Or if not, take him to base. In any of the error cases, take user to ``login`` page again.

Lastly, we make our ``logout`` function which is very easy to make.
```python
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
```
Simple code. Now let's learn a key thing. Go to ``view.html`` and write:
```html+jinja
{% extends 'base.html' %}

{% block body %}
<div class="container">
    Hello User! <br>
    {% if current_user.is_authenticated %}
    <b>YOU CAN see this line because it seems you are logged in!!</b><br>
    <a href="{{url_for('logout')}}" >Logout</a>
        
    {% endif %}
</div>
{% endblock body %}
```
There is a part ``{% if current_user.is_authenticated %}``. This means this jinja block will check if the current user is authenticated or not. If not,
then there is a ``text`` and ``Logout`` button available. That won't be shown to any user. So any user without loggin in, can go to``/view`` and will only
see ``"Hello User!"``. But any person who is authenticated will see the next parts too. This is a very critical part of learning flask.

Let's make some restricted page for the site so that anyone trying to access those page will be caught and taken to ``login.htmnl`` file.

```python
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
```
These urls are locked with ``login_required`` decorator. So any user not authenticated cannot access these functions, or urls.

We go to our command line editor with ``flask shell`` command.
```python
E:\Flask\Flask_Tutorial\07.Flsak _ Login\2.Flask_login_2(w registration)>flask shell
>>> from main import *
>>> db.create_all()    
>>>
```
That's it. Let's go and start our app:

![first](https://github.com/isfar17/Flask_Tutorial/blob/master/07.Flsak%20_%20Login/2.Flask_login_2(w%20registration)/image/first%20look.jpg)

Then we register user:

![register](https://github.com/isfar17/Flask_Tutorial/blob/master/07.Flsak%20_%20Login/2.Flask_login_2(w%20registration)/image/registraion.jpg)

After a successfull registration, we are redirected to login page.

![login](https://github.com/isfar17/Flask_Tutorial/blob/master/07.Flsak%20_%20Login/2.Flask_login_2(w%20registration)/image/redirected_login.jpg)

Then we can see our ``view`` page:

![view](https://github.com/isfar17/Flask_Tutorial/blob/master/07.Flsak%20_%20Login/2.Flask_login_2(w%20registration)/image/after_login.jpg)

Now let's log out and try to go to any restricted page:

![trying](https://github.com/isfar17/Flask_Tutorial/blob/master/07.Flsak%20_%20Login/2.Flask_login_2(w%20registration)/image/trying_rest_page.jpg)

But it will redirect us to ``login`` page. So we login using our username and password:

![after_login](https://github.com/isfar17/Flask_Tutorial/blob/master/07.Flsak%20_%20Login/2.Flask_login_2(w%20registration)/image/final_w_next.jpg)

We have been redirected to the page we wanted to go. Now let's go and logout. Then we try to visit our `/view` page again to see if we can see logout
text:

![without_login](https://github.com/isfar17/Flask_Tutorial/blob/master/07.Flsak%20_%20Login/2.Flask_login_2(w%20registration)/image/view_wo_login.jpg)

There it is. We can see that there are nothing much. We are good to go.
















