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

Now we have to make our functions. First we make our registraion functions. Then we will copy/paste our previous ``login`` code from our last tutorial.
Let's do it.

```python
```
