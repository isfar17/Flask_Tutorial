# Introduction to flask login

While making a multi-purpose website, it is neccessary to have a Registration and login system. In this tutorial we will be working with that. Let's build
our basic application first.
```python
from flask import Flask,render_template

app=Flask(__name__)

@app.route('/',methods=['GET',"POST"])
def index():
    return "hello world! Go to '/login' to log into the website "


if __name__=="__main__":
    app.run(debug=True)
```
The app will run perfectly. Now we have to understand some basics of ``Login system`` in ``Flask``.
***
Flask login uses a Table to store it's user's data into it. Then When a user inputs data into html form and send that back to flask, ``flask_login`` checks
if the user is available in the Table. If yes, then it allows user to get into any restricted area such as ``profile``, fill-up ```feedback from``` etc by
using it's internal function ``login_user(the_user_name_provided)``. And if anyone wants to logout, there is a simple function ``logout()`` that easily 
does all the work.

---
But before all of that, we have to initiate ``flask-login``. Let's import everything and initiate our database and ``flask-login``:

```python
from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SECRET_KEY"]="secret"

db=SQLAlchemy(app)


login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view ='login'


```
Let's break down everything in detail. First we configured our database variables. Then we setup ``SECRET_KEY``. After that we make our db variable and 
initialize our ``SQLAlchemy``. Further we start working with ``login system``. We first make an object named ``login_manager`` where we take LoginManager()
class. This class has all the functionalities included to work with login system. Then we bind our ``app`` and ``LoginManager`` we imported earlier. At 
last, we set up the  ``login_view``. It means that where we will work with ``login`` function. We set it equal to ``login``(We will create the  function 
down below later on). Or in other word, in which function the process will take place.So in total ``login_view``  is the name of the view to redirect to 
when the user needs to log in. This can be an absolute URL as well such as ``/googleauth``, if your authentication machinery is external to your 
application.

Next we setup our Table. Now there are some extra works we gotta do. First of all, we import a special class ``UserMixin`` under flask_login. This class
handles checking the users information while loggin in. We write:

```python
from flask_login import UserMixin

class User(db.Model,UserMixin):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    password=db.Column(db.String(200),nullable=False)

```
Now this is a basic class. But we want to make our password cryptic. Means if somehow our database gets leaked, we want to make sure that password remains
secure. So now we import a very helpful module and its function named ``werkzeug``.

Let's use it to make our password cryptic:
```python
from werkzeug.security import check_password_hash,generate_password_hash

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
```
We have made an extra function ``check_password``. This is to get extra functionalities while working with ``werkzeug``. We first store password in cryptic
format. But we also want to check if the password matches because it is now in cryptic format. That's it. We have done our first step. Let's go to terminal
and make some users manually because we are not going to make any registration form right now. We will have users data included and we will simple use 
those info to login and check if works or not.

Let's go down and make some restricted page first where the user, without loggin in cannot access them. But if he logs in, he can. Then lastly we will 
setup our ``login`` function and ``logout`` function.

```python

@app.route('/restricted',methods=['GET',"POST"])
@login_required
def restricted():
    return "hello world! This is a restriced area. Go to /login to log into the website "

@app.route('/another',methods=['GET',"POST"])
@login_required
def another_func():
    return "hello User! This is a another restrict area. Go to /login to log into the website "

```

We are almost ready. Let's go and make our ``login`` html file.

``` html+jinja
{% extends 'base.html' %}

{% block title  %}Login{% endblock title  %}

{% block body %}
    This is the body<br>
    hi this is login_page.html file<br>
        <!-- This pattern recognises the function to be called and gets to it. it will return whatever inside it is -->

        <form method="POST">

            <input type="text" name="name" >
            <input type="password" name="password" >
            <button type="submit">Submit</button>

        </form>
{% endblock body %}
```
Here we have made an ``html form`` and where we set it's url to the ``login`` function. The user will insert data
and submit it and flask will transfer data in the ``login`` function. There we will check their inputs.

Next there is a very neccessary task we have to do. **Before** writing the ``login`` we write:
```python
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
```
This is a vary important function. this triggers when a Userenters through login. it checks and pull out the Userfrom the table. then if there is a user,
it gives the user accessto restriced pages

documentation - https://flask-login.readthedocs.io/en/latest/#how-it-works

You will need to provide a user_loader callback. This callback is used to reload the user object from the user ID stored in the session. It should take the
str ID of a user, and return the corresponding user object. For example:
It should return None (not raise an exception) if the ID is not valid. (In that case, the ID will manually be removed from the session and processing will continue.)

Now we have to make our last and most important functions. That is ``login``.

```python
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



```
Let's break down the code one by one. So look at the top line:
```python
if request.method=="POST":
    do other stuffs
    then
    return redirect("to the page user wanted to go")

return render_template("login_page.html")
```

First time when this function will run, the method will be ``GET``, as no form is being 
sent, so ``if condition`` will fail and will show the template down below. That is the ``login_form`` template which has the login form. Later it will work
fine as it will be sending a form with ``POST`` method. The first portion:
```python
name=request.form.get("name")
password=request.form.get("password")

user=User.query.filter_by(name=name).first()
```
Here we are using ``flask-request`` module to request ``html-form`` data. We fetch the username and password data.
Then we search if our ``User`` Table has the user already added or not. This will either return ``None`` or ``an object``.
Next part:
```python
if user is None:
    return redirect(url_for("login_page"))
 
if user.check_password(password) is False:
    return redirect(url_for("login_page"))

login_user(user)
print("user logged in")

```
Here we are making sure if the user does not exists, we redirect user to ``login_page`` again to input the right
credintial. If the user exists, we then check if the password matches or not. If it does not, then again we will
send user to ``login_page`` again to enter correct password. If two of the condition fails, means we have input
our right information. We authorize user by ``login_user(user)`` and he is good to go.

**Additional Part :**

We actually could finish our code by returning user to ``homepage`` at the next line of ``login_user(user)``. But there
might be cases where user will actually want to go to suppose ``profile`` and he is not logged in. Since it will be
a restricted page, he will not gain access, and will redirected into ``login_page``. But html also stores the user's
typed url he wanted to go. We can get the url data and send user to that  url instead of ``homepage``.
```python
next = request.args.get('next')
if next and next[0]=="/":
    return redirect(next)

else:
    return redirect(url_for("view"))
```
Here we are fetching the ``next`` attribute from html header file using ``request``. It either might be None or
a string url. So we will check if the first part of the url is ``/`` such as ``/restricted``, we will redirect the
user there. But if not, we will send the user to ``view`` or to the homepage.

Lastly we setup our ``logout`` function. It is very easy to do.
```python
#logs out user. all access to restricted pages gets disabled
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
```

Now let's go and start our app. We will see:

![first](https://github.com/isfar17/Flask_Tutorial/blob/master/07.Flsak%20_%20Login/1.Flask_login_1(no%20regsitration)/image/first.jpg)

Next we try to login. So we type ``/login`` in url:

![login](https://github.com/isfar17/Flask_Tutorial/blob/master/07.Flsak%20_%20Login/1.Flask_login_1(no%20regsitration)/image/login_page.jpg)

We type our credintials and login:

![after](https://github.com/isfar17/Flask_Tutorial/blob/master/07.Flsak%20_%20Login/1.Flask_login_1(no%20regsitration)/image/after_login.jpg)

We click on logout and again taken to base. Now let's try to log into a restricted page. So we type ``/restricted``:

![restricted](https://github.com/isfar17/Flask_Tutorial/blob/master/07.Flsak%20_%20Login/1.Flask_login_1(no%20regsitration)/image/restricted.jpg)

We will see that we are redirected to our normal user log in page. So we write our credintials and try to log in. And now we will be redirected to
the restricted page. As we said, the ``next`` parameter will store the url value and send it to flask. We accessed it and later redirected here:

![after](https://github.com/isfar17/Flask_Tutorial/blob/master/07.Flsak%20_%20Login/1.Flask_login_1(no%20regsitration)/image/after_restrcited.jpg)

Here is what we see in our command prompt:
```
127.0.0.1 - - [17/Sep/2023 13:35:39] "POST /login HTTP/1.1" 302 -
127.0.0.1 - - [17/Sep/2023 13:35:39] "GET /view HTTP/1.1" 200 -
127.0.0.1 - - [17/Sep/2023 13:35:40] "GET /logout HTTP/1.1" 302 -
127.0.0.1 - - [17/Sep/2023 13:35:40] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [17/Sep/2023 13:35:44] "GET /restricted HTTP/1.1" 302 -
127.0.0.1 - - [17/Sep/2023 13:35:44] "GET /login?next=/restricted HTTP/1.1" 200 -
user logged in
/restricted
127.0.0.1 - - [17/Sep/2023 13:35:47] "POST /login?next=/restricted HTTP/1.1" 302 -
127.0.0.1 - - [17/Sep/2023 13:35:47] "GET /restricted HTTP/1.1" 200 
```
### I got stuck in login function with "next" parameter and here is why:

So before this one, i made two seperate functions where I show the html form file only. And in my html form, i specify the redirect url to another ``login``
function where the login will process. This ended up creating a big problem. While I was trying to get into any restricted page,  I was taken to login
page but then straight to ``view`` page. This happened because the redirect url of ``html form`` was already set and thus it would not carry any ``next``
parameter to the ``login`` function. So the ``next`` parameter condition failed everytime I tried working. I then put all the code into one function and
from the html file, I removed the ``action=`` parameter, Thus I could access the form from my ``html`` file where I processed my code too. Because I did
not specify any url in ``form``, Thus it would take the ``next`` parameter to flask. This is a  bit confusing. The main thing is:

---
1. Don't use two different functions to show and process the login.
2. Make sure, that the redirection,method allowence are ok.
***
