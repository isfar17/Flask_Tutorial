# Flask Admin Basics and why it is more important than Blueprint and other basic things?(According to me)
Let's talk about the importance. When we talk about Django, another python based web-framework, which is bigger than flask of course, we get many extra
advantage of it. Django is way bigger and more popular for large webapp development. It's one of the best feature is we don't need any extra admin panel
in the beginning. We get our pre-built admin panel where there are Tables shown. We can check and review the data, can update, can add and even delete. All
the manegment of Admin is pre-built. But flask does not have an admin panel pre-built. So we build one by typing everything and adding those functionalities
one by one. But flask has already a module named Flask-Admin which does the most of the work. If we install it and just add some codes or lines, we can
access all the function of Admin panel like we used to get in Django.

## Flask-Admin
Let's create our basic app.
```python
from flask import Flask
 

app=Flask(__name__)

@app.route('/')
def index(): 
    return 'hello world'

if __name__=='__main__':
    app.run(debug=True)

```
Now we run the app and everything works fine. Lets add the admin panel. First we install the module and then we import them

```python
#importing the admin module. needs to be installed.
from flask_admin import Admin
#modelview is neccessary to show and view database in admin panel
from flask_admin.contrib.sqla import ModelView 
```
Although we dont have any database or Table, ``ModelView`` will not be in any of use for now. So since we imported, Now the second part is to
initialize the site. Lets go and do that

```python
app=Flask(__name__)

admin=Admin()#define
admin.init_app(app=app)#initialization in the server

@app.route('/')
def index(): 
    return 'hello world'
```
Here we first create an instance of Admin class. Then we initalize the app. Now if we just run our server and type ``/admin`` we see this image:
![view](https://github.com/isfar17/Flask_Tutorial/blob/master/04.Flask%20Admin/1.flask_Admin_basic/images/admin_view.jpg)

Thats it.










