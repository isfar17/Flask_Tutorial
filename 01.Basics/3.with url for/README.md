# url_for() function and its usage
In the last tutorial we learned about html fine connecting and rendering them in the server. In today's work we will try to redirect from one html file to another
html file using a function called ``url_for()`` .From flask documentation ``url_for()`` is a function which takes url path/function name in string format and redirects
function to that particular url/function. like if we put ``url_for('/user')`` , it will take us to user site. But if we type ``url_for('user')`` it will take us to
that function in our program. That is it. So lets add it in our program.

In our ``app.py`` file we write code like down below :

```python
from flask import Flask,render_template,redirect,url_for

app=Flask(__name__)

@app.route('/')
def index(): 
    return render_template("index.html")

#go to index.html to see url_for usage

@app.route('/new')
def new():
    print("Came to New")
    return redirect(url_for("index"))

if __name__=='__main__':
    app.run(debug=True)
```
if we see we have used two functions in return. That is because redirect function takes url_for() functions redirection and redirects to that path/function. It can be
write in many ways. But for now we will create our ``index.html`` file and see if we can redirect it. We will see that the function is running.

### Jinja Templating

This is one of the most important part of learning flask. We really want to put our python codes result into our html file. But its not possible in normal way.
Jinja helps is in this case. We can use jinja block in html file and can easily access any code from python file and return it into our html file. Let's see our 
example.

By convention, we have to make a base html file which will contain the common blocks of html tag every html file has. Suppose every html file will have
the same navbar or same footer in the website. Every page in webpage will have the same type of text and their heading can be same. So we create a ``base.html`` file
which will contain the common things and can derive them into our other html files just like programming! For example in our html file we write bootstrap template.
Then we create some jinja blocks. A jinja block has start and end tag:
```html+jinja
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

    <title>{% block title %}Base{% endblock title %}</title>
  </head>


  <body>
    {% block body %}
        
    {% endblock body %}

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
  </body>
</html>
```

Then in the ``index.html`` file we extend the components by typing :
```jinja
{% extends 'base.html' %}
```
Thats it! Now lets assume we want to write something in our body tag. If we write things such as   ``This is body`` in ``index.html`` file like down below, nothing
would show up.
```html
{% extends 'base.html' %}

This is body
```
Why? That is because we have created some blocks in our base jinja tag. So in order to show something in ``index.html`` file we must write things within
``block body`` tag. Lets modify the site file like this:

```html+jinja
{% extends 'base.html' %}

{% block title  %}HomePage{% endblock title  %}

{% block body %}
    This is the body
    <h1><a href="{{url_for('new')}}" target="_blank" rel="noopener noreferrer">Go to New to redirect here</a></h1>
        <!-- This pattern recognises the function to be called and gets to it. it will return whatever inside it is -->
{% endblock body %}
```
Here this line is most important to understand:
```html
<h1><a href="{{url_for('new')}}" target="_blank" rel="noopener noreferrer">Go to New to redirect here</a></h1>
```
To connect with other links/functions of program , we use url_for(). Since its html file, we use {{ }} inside where, we add url_for() function. The function 
indicates that it will take us to ``new`` named function. But we know that the function does not exits. so it will return 404 error if we click it. But the
basic now is cleared. 

Now if we run the app, we will see the picture like down below:
![image](https://github.com/isfar17/Flask_Tutorial/blob/master/01.Basics/3.with%20url%20for/images/url.jpg)
