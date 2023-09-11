# How to bind Admin with Flask-Blueprint

Let's structure a project with flask-blueprint first. We won't be making a complete blueprint structure. Rather we will make a sample app which will be linked
to our ``main.py`` file. Our target is not blueprint, its binding the Admin.

![struct](https://github.com/isfar17/Flask_Tutorial/blob/master/06.Flask%20Admin%20Advanced/1.flask_Admin%20(w%20blueprint)/images/base_Structure.jpg)
 
After creating an app with own templates folder we now go to ``views.py`` file and write:
```python
from flask import Blueprint,render_template

firstapp=Blueprint("firstapp",__name__,template_folder="templates/firstapp")#we defined templates folder location
                                                                            #now it will look into the provided location
@firstapp.route("/")
def index():
    return render_template("index.html")

@firstapp.route("/new")
def new():
    return render_template("new.html")
```
Now that we have made our ``blueprint app`` and set our route. Let's go to our ``main.py`` file and associate  ``Admin`` with it.

```python
from flask import Flask
from flask_admin import Admin

app=Flask(__name__)
admin=Admin()
admin.init_app(app)

#importing the blurprint variable from the app and then registering
from firstapp.views import firstapp

app.register_blueprint(firstapp)


if __name__=="__main__":
    app.run(debug=True)
```
So what happening here is that since we have not made any ``__init__.py`` file, so we will make our ``app`` variable in ``main.py`` file. Now we import
``Admin`` and initiate it. Then we import our ``blueprint app`` and register it. Lastly we run the file.

![look](https://github.com/isfar17/Flask_Tutorial/blob/master/06.Flask%20Admin%20Advanced/1.flask_Admin%20(w%20blueprint)/images/view.jpg)

If we go to ``/admin`` we will see this:

![admin](https://github.com/isfar17/Flask_Tutorial/blob/master/06.Flask%20Admin%20Advanced/1.flask_Admin%20(w%20blueprint)/images/admin.jpg)

