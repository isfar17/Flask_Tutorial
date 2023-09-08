# Structuring a real Blueprint project and a depth look of everything
Till now we only had apps and their views created separately. We connected them together by registering them in the ``main.py`` file. Then we run the app and
navigated through the apps and pages. But now we will create the real blueprint project and structure it. In web development, while creating project, we 
basically have a project. Inside the project we have our apps and other stuffs such as database and configuration folder is created. Outside the project or
in the same level of the project there is a python file, which runs the whole application. This is the best structure. In our case, we structure our project
like this:

![project_look](https://github.com/isfar17/Flask_Tutorial/blob/master/05.Flask%20BluePrints/3.flask_blueprint_basic_with_project/image/project_Structure.jpg)

Hereat first we can see our project name, which is ``myproject``. Then inside the project, we see our two apps, ``firstapp`` and ``secondapp``. They have
their own ``templates`` and ``views.py`` file. Outside the apps, there are two additional files. **These are new case and we must understand their use**. 
So the first file ``model.py`` file is nothing but the database file, where we create all of our ``Tables`` and ``Custom  Admin View``(will see later). 
Then comes the ``__init__.py`` file.
***
The ``__init__.py`` file is a special Python file that is used to indicate that the directory it is present in is a Python package. It can contain 
initialization code for the package, or it can be an empty file. In Python, the ``__init__.py`` file is used to mark a directory as a Python package. 
It is used to initialize the package when it is imported. And why do we do that? See we already have said that we want to run our application
outside the project. So now if we covert our project into a package, we can import the ``app`` variable and run it as ``app.run`` in ``main.py`` file. And
we all knoe that python flask app only runs or starts when ``app.run()`` is called. That is why we do this.

---
The last thing might come in head that what about the configurations? Well we will now do this inside of that ``__init__.py`` file. Another point is
the ``instance`` folder is created automatically when we call our database create command in ``flask-shell``. Let's look at the detailed view of our project structure:

![detailed_View](https://github.com/isfar17/Flask_Tutorial/blob/master/05.Flask%20BluePrints/3.flask_blueprint_basic_with_project/image/detail_description.jpg)

Now let's go to our apps and create neccessary blueprints and setup all the routings.

**firstapp:**

In our firstapp folder's ``views.py`` file, we write:
```python
from flask import Blueprint,redirect,render_template

firstapp=Blueprint("firstapp",__name__,template_folder="templates/firstapp")

@firstapp.route("/")
def index():
    return render_template("index.html")

@firstapp.route("/new")
def new():
    return render_template("new.html")
```
As usual, ``firstapp`` is the blueprint app variable, and by using that variable, we set our routes to ``index.html`` file and ``new.html`` file. This
is simple. Now in our ``index.html`` file we write:
```html+jinja
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Firstapp/index</title>
</head>
<body>
   hi this is index 
<!-- 
   if we move to blueprints we now have made apps separate. so now we cant just
   use url_for('new') because url_for does not know which apps function we are calling.
   so we have to use appname.function now -->
   <a href="{{url_for('firstapp.new')}}">Go to New</a>
</body>
</html>
```
And in our ``new.py`` file:
```html+jinja
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>firstapp/new</title>
</head>
<body>
    this is new
</body>
</html>
```
Save it and our work in ``firstapp`` folder (**Not variable**) is done.


**secondapp:**

In our secondapp folder's ``views.py`` file, we write:
```python
from flask import Blueprint,redirect,render_template,url_for,request

secondapp=Blueprint("secondapp",__name__,template_folder="templates/secondapp")

@secondapp.route("/",methods=["GET","POST"])
def index():
    return render_template("second_index.html")

```
Now save it and go to ``__init__.py`` file. We write:
```python
from flask import Flask

app=Flask(__name__)

from myproject.firstapp.views import firstapp
from myproject.secondapp.views import secondapp

app.register_blueprint(firstapp,url_prefix="/")
app.register_blueprint(secondapp,url_prefix="/second")
```
Save it. Here is the catch. Now that we have set our ``app`` which is the __MAIN FLASK APP VARIABLE__, we won't run it here. Let's go to our
``main.py`` file. We write:
```python
from myproject import app

if __name__=="__main__":
    app.run(debug=True)
```
Look carefully that we are saying ``from myproject import app``. This means that we are importing the ``app`` variable from the ``myproject`` Package.
And it is defined inside the ``__init__.py`` file of the project. That's it. Let's run and see:

![first](https://github.com/isfar17/Flask_Tutorial/blob/master/05.Flask%20BluePrints/3.flask_blueprint_basic_with_project/image/first_index.jpg)

We can click on new and it will take us there. Everything works fine.

## Send data from html-form to flask database by using Flask-Blueprint
Our goal:
***
1. To configure database location and the secret key to secure data transfer
2. To make a Database and create Table inside of it
3. Use html file to make a form and send data to our flask-blueprint app
4. Save the data to database
---
### 1

Go to ``__init__.py`` file and configure everything neccessary:
```python
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=True
app.config["SECRET_KEY"]="secret#234)"

# database location and other stuffs must be done before initialiazing the db

db=SQLAlchemy(app)

# AT init file, blueprint must be set after defining db
```
This is a very important note that inside the init file, we must set our database variable or db before registering blueprints. Blueprints must be
registered after all the configurations and imports.
### 2
Now that we have created our database and setup secret key, we have to make our Table. Let's go and make one in the ``model.py`` file:
```python
from myproject import db

class SecondClass(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)

    def __init__(self,name):
        self.name=name

    def __repr__(self):
        return f"{self.id} -> {self.name}"
```
Why i named the class wierdly like ``SecondClass``? Because we wil now only work with the ``secondapp`` and this Table will also be used in that app only.
That's why for the sake of understanding, we made it. Now there is nothing to tell anything new about how to make a Table. We usually use db.Model as
superclass and make our ``columns``. But here we don't have the ``db`` created. So we import it by saying ``from myproject import db``, Since now myproject
is a python package. 

Now sometimes there is an issue of circular import error at ``__init__.py`` file. What is that? Basically suppose we have imported
the db variable in our models.py. Again if we now import our Table in the ``__init.py`` file, Which is basically dependent on db, Again db is created
in ``__init.py`` file. This is circular import error issue.

### 3

Let's go to our ``secondapp`` folder's ``templates/secondapp`` folder and in the ``second_index.html`` file we write:
```html+jinja
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>seconapp/index</title>
</head>
<body>
    this is the index page
    <br>
    <br>

     <form action="{{url_for('secondapp.data_entry')}}" method="post">

        Name: <input type="text" name="name">
        <button type="submit">Submit</button>

     </form>

</body>    
</html>
```
Here we wrote a form, the form takes name as it's input, the name of the attribute is also ``"name"`` because we know that we can access the ``form-data``
by their ``name attribute``. When we submit the data it will go to a function of the ``secondapp`` named ``data_entry``. And we also said that the method would be ``"post"``. That's it.

### 4

Let's go to our ``views.py`` file under ``secondapp`` and create our ``data_entry`` function and elaborate everything:
```python
from flask import Blueprint,redirect,render_template,url_for,request
from myproject import db
from myproject.model import SecondClass
from sqlalchemy import exc


@secondapp.route("/data_entry",methods=["GET","POST"])
def data_entry():
    try:
        data=SecondClass(name=request.form.get("name"))
        db.session.add(data)
        db.session.commit()
        return "You have successfully inserted data !"
    
    except exc.SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
        return redirect(url_for("secondapp.index"))
```
Firstly, while working with sending and recieving data, we should specify which ``methods`` to use or to allow while passing data. So we specify them.
Secondly  we will try to recieve data and save it in the database.
```python
from myproject import db
from myproject.model import SecondClass
from sqlalchemy import exc
```
We have defined our db or database variable in our project `__init__.py` file. So we imoprt it. Next we wrote our ``SecondClass`` model in ``model.py``
file. We import it also. Next, we import ``exc`` from ``sqlalchemy``. Here ``exc`` is exception. We can access different SQLAlchemy errors with this.
We need this later on. Next we write:
```python
data=SecondClass(name=request.form.get("name"))
db.session.add(data)
db.session.commit()
return "You have successfully inserted data !"
```
We make an object of ``SecondClass`` and we get our form-data from ``request.form.get("name")``. We take it and save the data in ``name`` attribute.
Then we add it and commit our data. __BUT__ There is a catch. THat is, while defining our ``name`` column in ``SecondClass``, if we go back, and see
that we added ``nullable=False`` attribute. What does this mean? This means the data we are trying to save can't be nullable. But if we try to
save it, it will return ``IntegrityError``. So to deal with this we use ``try`` block. If data saving does not fail, we will show the user a message.
But if the user fails, then we must take some action. So we say:
```python
db.session.rollback()
return redirect(url_for("secondapp.index"))
```
Means we rollback every operation we tried to do or undo everything and send the user to ``index`` again or in the page where the form is. So we use
``except`` block. Now look at the ``exc.SQLAlchemyError as e`` part. What does this mean?

Here we want to see which type of error is occuring. Since we said that the ``exc`` contains the errors of ``SQLAlchemy``, we can print it. We could
just say ``except``, but for better understanding, we imported the ``exc`` and printed out what error occured. Save it. Save everything and run our app.

Now if we go to ``/second``, we see this:

![second_index](https://github.com/isfar17/Flask_Tutorial/blob/master/05.Flask%20BluePrints/3.flask_blueprint_basic_with_project/image/second%20index.jpg)

Now if we enter anything and press submit, we see this message:

![after](https://github.com/isfar17/Flask_Tutorial/blob/master/05.Flask%20BluePrints/3.flask_blueprint_basic_with_project/image/after_inserting.jpg)

And if we just press submit without entering data, we will see this message in our terminal:

```
<class 'sqlalchemy.exc.IntegrityError'>
127.0.0.1 - - [08/Sep/2023 11:50:58] "GET /second/data_entry HTTP/1.1" 302 -
```
It says that there is an Integrity Error, or we tried to break the rule of the column where we tried to put data. That is it.

Lastly, with VS Code database viewer extension, if we open our database, we see this:

![database](https://github.com/isfar17/Flask_Tutorial/blob/master/05.Flask%20BluePrints/3.flask_blueprint_basic_with_project/image/database_view.jpg)

We are good to go.


