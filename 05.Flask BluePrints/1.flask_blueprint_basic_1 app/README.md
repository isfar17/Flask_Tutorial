# Basics of Blueprint and Basic Application
When we talk about web frameworks such as Django, React, They are big frameworks. So They can deal many apps together in one place. For example, Let's talk about
Facebook. So consider ``Facebook`` as a project. It has many parts. ``Messeging``, ``Groups``, ``Marketplace`` where you can sell and buy stuffs. All this are a single
apps. These apps has many functionalities and features of their own. And they are all linked to the main project. That is ``Facebook``. Let's see a diagram:

![fb](https://github.com/isfar17/Flask_Tutorial/blob/master/05.Flask%20BluePrints/1.flask_blueprint_basic_1%20app/images/what%20is%20project%20and%20apps.jpg)

Now all the big frameworks, such as Django, React, VueJS and so on has this features built in. They have automatic directory and paths, and all the tools to make
big project. Here is a look of Django and React project directory:

![directory](https://github.com/isfar17/Flask_Tutorial/blob/master/05.Flask%20BluePrints/1.flask_blueprint_basic_1%20app/images/collage.png)

The left one is Django and the right one is React. Now flask can be also modified to make big projects like with multiple apps. This is done through a very 
poplular module named  ``Flask-Blueprint``. By using it, we can easily make a complete project and link apps together. That is the basic of Blueprint.

# Basics of Blueprint
Let's start from very basic. We will not make any project, nor any complex things. We just will learn the basic applications of ``Blueprint``. Till now
we have been making a single file and inside of that, we put our code and run the whole server. But now we will create a seperate folder. Inside of that folder,
we will make our app files, and write our urls and other stuffs. Then we will create another file outside the folder and run our application through that file.
So 2 things to note:
***
1. The folder in flask is known or called as ``app``.
2. The outside file is the file with which we will run our application.
---
Now we go and create our first app. Inside of the app, we make our own ``templates`` folder, in which we create our ``index.html`` and ``new.html`` files.
Now we create a ``view.py`` file where we will setup the routes for the html files. Outside the app, we make another ``main.py`` file, with which we will
run our app.

![look](https://github.com/isfar17/Flask_Tutorial/blob/master/05.Flask%20BluePrints/1.flask_blueprint_basic_1%20app/images/file_look.jpg)

After that we go inside the ``main.py`` file. We initiate and make our app. This is not the app we created, this is ``FLASK APP`` we are setting up.
```python
from flask import Flask

app=Flask(__name__)


if __name__=="__main__":
    app.run(debug=True)
```
We save it. Now after creating the routes in our app, we **ALWAYS AND ALWAYS** come to this file and run this file. This file starts everything.

Now let's go to our ``views.py`` file. We import our ``Bluprint`` and setup our blueprint variable:
```python
from flask import Blueprint

firstapp=Blueprint("firstapp",__name__,template_folder="templates/firstapp")#we defined templates folder location
                                                                            #now it will look into the provided location
```
Now this is a bit or very confusing. What this might be? So the real answer is -
***

Flask blueprint connects app together. Now in order to connect apps with Blueprint, we need to initialize it. So we use ``Blueprint`` class of flask
to initialize the app. Basically we set the variable name same as the app. Because later on we need to register the apps in our main file. By registering
the apps, we connect them. When we register the apps, we have to register them through the ``variable`` we take to initialize ``Blueprint``.

---
Here the basic syntax of the Blueprint class setup is 
```python
variable(same_as_app)=Blueprint("the_variable_name_itself",__name__, other parameters)
```
Ok so Blueprint's first option is the blueprint app name. We have to set it to the name of the blueprint variable itself. The next parameter
is import name. So we set it to ``__name__`` which returns the name of the app or file. There are other parameters such as ``templates_folder`` . We set it
to ``templates/firstapp``. And why is that? Because without setting it, Flask automatically will find the  ``templates`` folder outside the project, or in
other words where the ``main.py`` file is. But with blueprint, we have made a different app. So we must define the new path. In order to avoid confusion,
we set it to ``templates/appname`` because later on we will see many apps are there with ``templates`` and flask will confuse them. That is why we need to
seperate the folder name by using another folder inside of ``templates`` folder.
Here are some definations according to documentaion:
```
:param name: The name of the blueprint. Will be prepended to each
  endpoint name.
:param import_name: The name of the blueprint package, usually
  ``__name__``. This helps locate the ``root_path`` for the
  blueprint.
:param static_folder: A folder with static files that should be
  served by the blueprint's static route. The path is relative to
  the blueprint's root path. Blueprint static files are disabled
  by default.
:param static_url_path: The url to serve static files from.
  Defaults to ``static_folder``. If the blueprint does not have
  a ``url_prefix``, the app's static route will take precedence,
  and the blueprint's static files won't be accessible.
:param template_folder: A folder with templates that should be added
  to the app's template search path. The path is relative to the
  blueprint's root path. Blueprint templates are disabled by
  default. Blueprint templates have a lower precedence than those
  in the app's templates folder.
:param url_prefix: A path to prepend to all of the blueprint's URLs,
  to make them distinct from the rest of the app's routes.
```
Now down below we create our route:
```python

@firstapp.route("/")
def index():
    return render_template("index.html")

@firstapp.route("/new")
def new():
    return render_template("new.html")

```

