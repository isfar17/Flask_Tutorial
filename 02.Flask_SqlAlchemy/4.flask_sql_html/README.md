# Taking Data from HTML form and storing it into the databse.
We know how to create a database using SQLAlchemy. We also know how to insert data into table and commit it. So the only thing we need to learn is how to get 
data from html input and take it to database. Here we are going to work with that. First we create our app and neccessary views to work with.
```python
from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime

app=Flask(__name__)

#we have to define app configuration for the databse before
#we define the db varibale
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False
app.config["SECRET_KEY"]="hi" #its very important to set secret key while working with data passing between site and server
#or else error will throw
#initializing the object of database

db=SQLAlchemy(app)

class Base(db.Model):
    nid=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(25),nullable=False,unique=True)
    text=db.Column(db.String(200),nullable=False)
    date=db.Column(db.Date,default=datetime.utcnow())

    def __init__(self,text,name):
        self.name=name
        self.text=text
    

    def __repr__(self):
        return f"{self.nid} -> {self.name} -> {self.text[:5]}.. -> {self.date}"

@app.route("/")
def index():
    return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
```
Here we have created our database and then defined its location.The ``app.config["SECRET_KEY"]`` is used to set a secret key between the server and the client side.
When anyone sends data, it make sures that data is coming from the actual site and validates, its is more likely a token. We just set it to a random string. We can
use crypto module to make it harder to crack. Next we created our ``Base`` table where we have defined some of it's columns and datatype. Next with ``__repr__`` 
method is used to modify the look of the class when it is printed out. After creating a database, we defined some views. In the ``templates`` folder, we have 
``base.html``, ``index.html``, and ``view.html``. The ``base.html`` file has the basic structure of the html file like down below:
```html+jinja
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}Base Home{% endblock title %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9" crossorigin="anonymous">
  </head>
  <body>
    <h1>Hello, world!</h1>

    <br><br><br>
    
    {% block body %}
        This is Base Body
    {% endblock body %}

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-HwwvtgBNo3bZJJLYd8oVXjrBZt8cqVSpeBNS5n7C8IVInixGAoxmnlMuBnhbgrkm" crossorigin="anonymous"></script>
  </body>
</html>
```
Here we have defined the basic structure with jinija templating. We will change our title and body content of the other files after importing the content.
However, lets go to ``index.html`` and write a Bootstrap Form. (We can also copy paaste them from Bootstrap website):

```html+jinja
{% extends 'base.html' %} 

{% block title %} HOMEPAGE {% endblock title %}


 {%block body %}
<div class="container">
  <form action="{{url_for('view')}}" method="post">
      <!--this url_for() will take data into view function-->

        <div class="form-floating mb-3">
          <!--taken from bootstrap5 page as a sample-->
          <input class="form-control" type="name" name="name" aria-label=" input example" />

          <label for="floatingInput">Name</label>
        </div>
        <!--the name variable of (input tag and text area tag ) will be accessed in python file
            to fetch data from form. !-->
        <div class="form-floating">
          <div class="form-floating">
            <textarea class="form-control" placeholder="Leave a comment here" id="floatingTextarea" name="text"></textarea>
            <label for="floatingTextarea">Text</label>
          </div>
        </div>
      <br /><br /><br />
      <button class="btn btn-primary" type="submit">Button</button>
  </form>
</div>
{% endblock body %}
```
Here we are extending the ``base.html`` and writing our form-class inside of body tag. We defined the forms data sending location to ``view`` function with
``action="{{url_for('view')}}"``. Then in this we want to look at this two lines:
```html+jinja
<input class="form-control" type="name" name="name" aria-label=" input example" />
... ...
<textarea class="form-control" placeholder="Leave a comment here" id="floatingTextarea" name="text"></textarea>

```
We must remember that python can only access data from this tags with ``name=`` attribute. We take this attribute's string name and using it, we fetch data.
After that in our python file we write our ``view`` function:
```python
@app.route("/view",methods=["GET","POST"])
def view():
    if request.method=="POST": #when it runs for the first time it returns 0 as false, so the last line will execute
        
        name=request.form.get("name")#request takes the data from html form name variable to function
        text=request.form.get("text")
        print(name,text)
```
This is the basic function. Now if we run the app we see this image :
!(view)[https://github.com/isfar17/Flask_Tutorial/blob/master/02.Flask_SqlAlchemy/4.flask_sql_html/image/form_image.jpg]

If we input data and click submit, we will see these lines in our terminal :
```
wwewew weewewwe
127.0.0.1 - - [20/Aug/2023 01:10:43] "POST /view HTTP/1.1" 200 -
```













