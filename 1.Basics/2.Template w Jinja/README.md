# Using Templates to work with html files from Flask app
We know that the basic code for Flask minimal app is :
```python
from flask import Flask


app=Flask(__name__)



@app.route('/')
def index(): 
    return 'hello world'



if __name__=='__main__':
    app.run(debug=True)
    
```

This shows us a basic text in the localhost server. But its impossible to work with other stuffs of html files in flask app with just writing html lines in flaskapp.
So instead of that, we can simply make an html file. then we can connect the file into our flask app. For example in our directory, we make a folder in the same 
directory where the ``app.py`` file is. The folder's name must be ``templates``. This is because by default, flask searches for html files/templates in `templates` folder. So its important that the name must be the same. Inside of 
the folder we create an html file named ``index.html``. The file contains below code:

```html
 
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  
</body>
</html>
```
Then we go to our ``app.py`` file. We modify our code like down below :
```python
from flask import Flask,render_template


app=Flask(__name__)



@app.route('/')
def index(): 
    return render_template("index.html")


if __name__=='__main__':
    app.run(debug=True)
```
Here we first import a function named ``render_template``. This function locates the html file inside of it. Then shows it in the corresponding url. Let's see by running our
app. But We will see nothing but a white screen. Now we need to learn something. Thast is Bootstrap.

### What on earth is Bootstrap?
See as a backend developer, we dont have much time to work with css,js and others stuffs in html files. We just want to work in the background. Bootstrap is a tool
which allows us to do the  css/js automatically. There is a site we can visit (Bootstrap)[https://getbootstrap.com/docs/5.3/getting-started/introduction/]. We just
simply add their css/js links in our html files and our html file look beautiful and clean.
Here is the code:

```html
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

    <title>Index</title>
  </head>


  <body>
     This is the body.
     

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
  </body>
</html>

```
And we will be able to see our page something like down below:
 
![image](https://github.com/isfar17/Flask_Tutorial/blob/master/1.Basics/2.Template%20w%20Jinja/images/image.jpg)

Don't worry about the blue line and other stuffs. We will learn them in the next tutorial.
