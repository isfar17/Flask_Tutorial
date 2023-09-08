# Working with multiple apps in Flask Blueprint
This is the second stage of blueprint. We will learn:
***
1. How to create two apps with blueprint
2. link the apps by registering them
3. routing between the apps by using ``url_for()`` function
---
Now, we already know how to create Blueprint apps, in the past tutorial, we have seen that we need a blueprint app variable, setting the route through the
app, and lastly register the app in the ``main.py`` file. Let's go and make our two apps first.

**Project Layout:**
As we know, by using blueprint, we get the access to re-arrange our project. Since we are in a  basic version of blueprint, we will create our structure like
this:
```
->firstapp
  |->templates
     |->firstapp
  |  |   ->index.html
     |   ->new.html
  ->views.py

->secondapp
  |->templates
     |->secondapp
  |  |   ->index2.html
     |   ->connect.html
  ->views.py

->main.py
```
Here two apps ``firstapp`` and ``secondapp`` has their own ``templates`` and ``views.py`` file. Then they both have their routing and stuffs. All of their
configuration is done in ``main.py`` file.

**First App:**

In our ``views.py`` file, we create our blueprint variable and route the ``html`` files.
```python
from flask import Blueprint,render_template,redirect,url_for

firstapp=Blueprint("firstapp",__name__,template_folder="templates/firstapp")

@firstapp.route("/")
def index():
    return render_template("index.html")

@firstapp.route("/new")
def new():
    return render_template("new.html")

```
As usual, ``firstapp`` is the blueprint app variable just like ``flask app`` variable we used to set earlier when we had only one file. Then we defined
the ``templates`` directory location. And lastly, we set our route. 

Next we go to our ``templates`` directory to write the html files. In the ``index.html`` file, we write:
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
   -->

   <a href="{{url_for('firstapp.new')}}">Go to New</a> <br>

   <!-- Now in the second tutorial we are trying to add two apps into blueprint so that
   we can learn the structures. and as usual with two apps, we must define url_for
   with the name of the app and the function we are trying to route. here we are
   routing to the second app from first app -->
  <h4> <a href="{{url_for('secondapp.index')}}">Go to SeconApp</a> </h4>
</body>
</html>
```
We have moved to blueprints. We now have made apps separate. So now we can't just use ``url_for('new')`` because url_for does not know which ``new``
function is called. Or flask doesn't know which app's ``new`` function we are calling. So we have to use ``appname.function`` now.

**Second App:**

In our ``views.py`` file, we create our blueprint variable and route the ``html`` files.
```python
from flask import Blueprint,render_template

secondapp=Blueprint("secondapp",__name__,template_folder="templates/secondapp")

@secondapp.route("/",methods=["GET","POST"])
def index():
    # one thing im facing here is that i cant use two same html file name
    #in two different app. but functions can be same like this one. here
    # im using index which ive used in first app too
    return render_template("index2.html")

@secondapp.route("/connect",methods=["GET","POST"])
def connect():
    return render_template("connect.html")
```
As usual, ``secondapp`` is the blueprint app variable just like ``flask app`` variable we used to set earlier when we had only one file. Then we defined
the ``templates`` directory location. And lastly, we set our route. One thing I'm facing here is that I can't use two same html file name in two different
app. But functions can be same like this one here I am using ``index`` which ive used in first app too.

Next we go to our ``index2.html`` file. We write:
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
     <a href="{{url_for('secondapp.connect')}}" target="_blank" rel="noopener noreferrer">Go to Connect</a>

</body>
</html>
```
Here we are saying that by clicking the link, we will go to our ``connect.html`` file. 

**Route through one app to another:**

Now let's go to our ``connect.html`` file and write:
```html+jinja
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>secondapp/connect</title>
</head>
<body>
   <h1> <a href="{{url_for('firstapp.index')}}" target="_blank" rel="noopener noreferrer"</a>Go to First index</h1> 
</body>
</html>
```
So here we said that this link will take us to ``firstapp.index`` means to the ``index`` function of ``firstapp``.

Now the second part is to go to ``main.py`` file and register blueprint apps.
```python
from flask import Flask

app=Flask(__name__)

from firstapp.views import firstapp
from secondapp.views import secondapp

# now in the main app we have to imoprt the blueprint variables we set earlier
# to register them into blurprint
app.register_blueprint(firstapp,url_prefix="/")
app.register_blueprint(secondapp,url_prefix="/second")

if __name__=="__main__":
    app.run(debug=True) #we dont have to define any views here. because it will automatically redirect to "/" where
                        #we earlier in the first app, set index as "/" here. so app will go to firstapp first
```
``app.run()`` automatically takes us to to "/" endpoint. So we do not need anything to do. Another thing to notice is that in our two ``views.py`` file,
we have wrote the two functions like this:
```python
#First app's index
@firstapp.route("/")
def index():
    return render_template("index.html")
```
```python
#Second app's index
@secondapp.route("/",methods=["GET","POST"])
def index():
    return render_template("index2.html")
```
So how we sort out the problem of not colliding two functions at the same url endpoint? Let's go to our ``main.py`` file again and see what is there:
```python
app.register_blueprint(firstapp,url_prefix="/")
app.register_blueprint(secondapp,url_prefix="/second")
```
We said, we can access the ``secondpp`` and it's route by going to ``/second/other_url_we_want_to_access``.

Now save all and run this ``main.py`` file.

![LOOK](https://github.com/isfar17/Flask_Tutorial/blob/master/05.Flask%20BluePrints/2.flask_blueprint_basic_2%20apps/image/look.jpg)

Click the ``Go to SeconApp``, and we will be taken to here:

![second](https://github.com/isfar17/Flask_Tutorial/blob/master/05.Flask%20BluePrints/2.flask_blueprint_basic_2%20apps/image/second.jpg)



