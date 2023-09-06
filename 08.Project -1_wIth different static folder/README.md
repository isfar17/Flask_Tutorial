# Flask Blog app with Flask-Blueprint Tutorial.
**( The blog is a free online blog template made with boostrap which has been re-constructed and integreted into flask and flask-blueprint )**
### Blueprint tutorial reminder:
Blueprint in short is used to manage multiple apps in a project. The project is run by a python file. The project contains a ```__int__.py``` file, a ```model.py```
in case if database work is needed. The project contains multiple folder. Each folder is an app. The apps contain their own templates folder,static folder, a python file such as ``routes.py``/``views.py`` file (to write python code for different functionalities and routes for the apps) and other stuffs if needed.
## 1. Structuring The Project
First I created a folder named it Project-1 (which is the folder I will make my project and python file). Then I created my project folder, ```main.py``` file in the same directory (outside of project folder) like below:
```
-> Project -1
      -> project
-> main.py
```
Then I created my blog app inside myproject:
```
-> Project -1
      -> project
            -> blog
-> main.py
```

Then i copy-pasted all the files of bootstrap blog folder:

```
-> Project -1
      -> project
            -> blog
            ->assets
            ->css
            ->js
            ->index.html
            ->contact.html
            ->about.html
            ->post.html
-> main.py
```

Then I created templates/blog inside blog and pasted html files into it. We created templates/blog folder to avoid collision
between the apps. If we did not put the inside folder, flask would search in default  ```templates``` folder for the templates. since we are in different
app, so we define our templates folder like this. And put assts,css,js into static folder (after creating the folder).I created an ```__init__.py``` file
under project folder to configure everything. **```main.py``` file will only run the whole project**. Inside the blog app, i created another views.py file to route
all the urls to their paths.
```
-> Project -1
      -> project
       |   -> blog
              |-> static
       |             ->assets
              |      ->css
       |             ->js
              | -> templates                  project and main.py file should be in the same directory, not one inside another
       |             | -> blog                for better understaing, the bar signs are used to show the foldre/files under a folder
              |          ->index.html
       |             |    ->contact.html
              |          ->about.html
       |             |    ->post.html
              |->views.py
       ->__init__.py
-> main.py
```

## 2. Coding

Now inside of the ```__init__.py``` file, which is the   most important file as it contains the whole project configurations in it, i import all the
important needed and initialize the app.
```python
from flask import Flask


app=Flask(__name__)
```
In the ```main.py``` file we write :

```python
from project import app



if __name__=='__main__':
    app.run(debug=True)
```

Then inside the ```views.py``` file under project/blog we imoprt blueprint and write a simple route:
```python
from flask import Blueprint,

blog=Blueprint("blog",__name__)

@blog.route("/")
def index():
    return "hellow world"
```
Frist we write our bluprint varibale and Create a Blueprint instance. then blueprint variable behaves like an app. we now use ```@blog.route()``` instead
of normally used ```@app.route()``` .The next part is very neccessary to understand. The insider parts of the Blueprint will add in the next part.
This is a very important part, because while writing the blueprint varibale, i faced many issues with templates and static files. ill explain them below.
But for now we go to ```__init__.py``` file again and register the blueprint after importing the blueprint variable.

```python
from flask import Flask

app=Flask(__name__)

from project.blog.views import blog #dont forget to add project.appname. i ran into no module error because of this

app.register_blueprint(blog,url_prefix="/")

```
Note that we have to register our dirrerent apps after initializing ``app`` and ``database``  and other configurations. I heard this a good practice.
Here we first register the app, then we have defined our apps route with ```url_prefix``` variable. This is good to define the urls of each apps. This avoids
clashes between app's route. If we would add another app in project, since we have added default "/" to first app we could say such as
```python
app.register_blueprint(another_app,url_prefix="/secondapp") #since "/" is taken by the first app
```

Now we go to the main.py file. run the file in the terminal and see "hellow world".

## 3. Redirect and Jinja Templating

After successfully running our project we now connect all the index and all the static,js,img files. First we go to the ```views.py``` file. Then we write all the routing functions for the templates folder. We first re-define our Blueprint by telling the templates folders location:

```python
blog=Blueprint("blog",__name__,template_folder="templates/blog")
```

We previously created templates/blog folder. This is because to avoid collision between the apps. If we did not put the inside folder, flask would search in default  ```templates``` folder for the templates. since we are in different app, so we define our templates folder like this. We can confirm that by looking into the structure previously we had where we added the templates folder like this :
```
-> project
 |   -> blog
        |-> static
               ...
        | -> templates
 |             | -> blog
        |           ->index.html
 |             |    ->contact.html
        |          ->about.html
 |             |    ->post.html
        |->views.py
 ->__init__.py
```
Down below we redefine index and write other functions to redirect them to their own html files.

```python
from flask import Blueprint,render_template

blog=Blueprint("blog",__name__,template_folder="templates/blog")

@blog.route("/")
def index():
    #return "hellow world"
    return render_template("index.html")

@blog.route("/post")
def post():
    return render_template("post.html")

@blog.route("/about")
def about():
    return render_template("about.html")

@blog.route("/contact")
def contact():
    return render_template("contact.html")
```

Now if we run ```main.py``` file again, **we will be able to see a non css/js based basic html website**. Also we will see all the html files in their own urls, but without css,js and images or **in raw html mode:**

![raw_view](https://github.com/isfar17/Flask_Tutorial/blob/master/08.Project%20-1_wIth%20different%20static%20folder/image/first_look.jpg)


Afer that we have to go inside of the html files downloaded from internet. Let's look inside the ```index.html``` file:

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
        <meta name="description" content="" />
        <meta name="author" content="" />
        <title>Clean Blog - Start Bootstrap Theme</title>
        <link rel="icon" type="image/x-icon" href="assets/favicon.ico" />
        <!-- Font Awesome icons (free version)-->
        <script src="https://use.fontawesome.com/releases/v6.3.0/js/all.js" crossorigin="anonymous"></script>
        <!-- Google fonts-->
        <link href="https://fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic" rel="stylesheet" type="text/css" />
        <link href="https://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800" rel="stylesheet" type="text/css" />
        <!-- Core theme CSS (includes Bootstrap)-->
        <link href="css/styles.css" rel="stylesheet" />
    </head>
    <body>
        <!-- Navigation-->
        <nav class="navbar navbar-expand-lg navbar-light" id="mainNav">
            <div class="container px-4 px-lg-5">
                <a class="navbar-brand" href="index.html">Start Bootstrap</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                    Menu
                    <i class="fas fa-bars"></i>
                </button>
                <div class="collapse navbar-collapse" id="navbarResponsive">
                    <ul class="navbar-nav ms-auto py-4 py-lg-0">
                        <li class="nav-item"><a class="nav-link px-lg-3 py-3 py-lg-4" href="index.html">Home</a></li>
                        <li class="nav-item"><a class="nav-link px-lg-3 py-3 py-lg-4" href="about.html">About</a></li>
                        <li class="nav-item"><a class="nav-link px-lg-3 py-3 py-lg-4" href="post.html">Sample Post</a></li>
                        <li class="nav-item"><a class="nav-link px-lg-3 py-3 py-lg-4" href="contact.html">Contact</a></li>
                    </ul>
                </div>
            </div>
        </nav>
        <!-- Page Header-->
        <header class="masthead" style="background-image: url('assets/img/home-bg.jpg')">
            <div class="container position-relative px-4 px-lg-5">
                <div class="row gx-4 gx-lg-5 justify-content-center">
                    <div class="col-md-10 col-lg-8 col-xl-7">
                        <div class="site-heading">
                            <h1>Clean Blog</h1>
                            <span class="subheading">A Blog Theme by Start Bootstrap</span>
                        </div>
                    </div>
                </div>
            </div>
        </header>
        <!-- Main Content-->
        <div class="container px-4 px-lg-5">
            <div class="row gx-4 gx-lg-5 justify-content-center">
                <div class="col-md-10 col-lg-8 col-xl-7">
                    <!-- Post preview-->
                    <div class="post-preview">
                        <a href="post.html">
                            <h2 class="post-title">Man must explore, and this is exploration at its greatest</h2>
                            <h3 class="post-subtitle">Problems look mighty small from 150 miles up</h3>
                        </a>
                        <p class="post-meta">
                            Posted by
                            <a href="#!">Start Bootstrap</a>
                            on September 24, 2023
                        </p>
                    </div>
                    <!-- Divider-->
                    <hr class="my-4" />
                    <!-- Post preview-->
                    <div class="post-preview">
                        <a href="post.html"><h2 class="post-title">I believe every human has a finite number of heartbeats. I don't intend to waste any of mine.</h2></a>
                        <p class="post-meta">
                            Posted by
                            <a href="#!">Start Bootstrap</a>
                            on September 18, 2023
                        </p>
                    </div>
                    <!-- Divider-->
                    <hr class="my-4" />
                    <!-- Post preview-->
                    <div class="post-preview">
                        <a href="post.html">
                            <h2 class="post-title">Science has not yet mastered prophecy</h2>
                            <h3 class="post-subtitle">We predict too much for the next year and yet far too little for the next ten.</h3>
                        </a>
                        <p class="post-meta">
                            Posted by
                            <a href="#!">Start Bootstrap</a>
                            on August 24, 2023
                        </p>
                    </div>
                    <!-- Divider-->
                    <hr class="my-4" />
                    <!-- Post preview-->
                    <div class="post-preview">
                        <a href="post.html">
                            <h2 class="post-title">Failure is not an option</h2>
                            <h3 class="post-subtitle">Many say exploration is part of our destiny, but it’s actually our duty to future generations.</h3>
                        </a>
                        <p class="post-meta">
                            Posted by
                            <a href="#!">Start Bootstrap</a>
                            on July 8, 2023
                        </p>
                    </div>
                    <!-- Divider-->
                    <hr class="my-4" />
                    <!-- Pager-->
                    <div class="d-flex justify-content-end mb-4"><a class="btn btn-primary text-uppercase" href="#!">Older Posts →</a></div>
                </div>
            </div>
        </div>
        <!-- Footer-->
        <footer class="border-top">
            <div class="container px-4 px-lg-5">
                <div class="row gx-4 gx-lg-5 justify-content-center">
                    <div class="col-md-10 col-lg-8 col-xl-7">
                        <ul class="list-inline text-center">
                            <li class="list-inline-item">
                                <a href="#!">
                                    <span class="fa-stack fa-lg">
                                        <i class="fas fa-circle fa-stack-2x"></i>
                                        <i class="fab fa-twitter fa-stack-1x fa-inverse"></i>
                                    </span>
                                </a>
                            </li>
                            <li class="list-inline-item">
                                <a href="#!">
                                    <span class="fa-stack fa-lg">
                                        <i class="fas fa-circle fa-stack-2x"></i>
                                        <i class="fab fa-facebook-f fa-stack-1x fa-inverse"></i>
                                    </span>
                                </a>
                            </li>
                            <li class="list-inline-item">
                                <a href="#!">
                                    <span class="fa-stack fa-lg">
                                        <i class="fas fa-circle fa-stack-2x"></i>
                                        <i class="fab fa-github fa-stack-1x fa-inverse"></i>
                                    </span>
                                </a>
                            </li>
                        </ul>
                        <div class="small text-center text-muted fst-italic">Copyright &copy; Your Website 2023</div>
                    </div>
                </div>
            </div>
        </footer>
        <!-- Bootstrap core JS-->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
        <!-- Core theme JS-->
        <script src="js/scripts.js"></script>
    </body>
</html>

```
All the html files are pretty much same here. This looks really odd since it has many codes in it. But we will not worry about any of these. Our consern is only the urls. Lets look the urls in ```<nav>``` tag:
```html
<li class="nav-item"><a class="nav-link px-lg-3 py-3 py-lg-4" href="index.html">Home</a></li>
<li class="nav-item"><a class="nav-link px-lg-3 py-3 py-lg-4" href="about.html">About</a></li>
<li class="nav-item"><a class="nav-link px-lg-3 py-3 py-lg-4" href="post.html">Sample Post</a></li>
<li class="nav-item"><a class="nav-link px-lg-3 py-3 py-lg-4" href="contact.html">Contact</a></li>
```
### Using url_for() functions to fix the routes.
Now we use url_for() to re-write the ```href``` var. We do this for all the ```href``` in ``navbar``.

```html
<li class="nav-item"><a class="nav-link px-lg-3 py-3 py-lg-4" href="{{url_for('blog.index')}}">Home</a></li>
<li class="nav-item"><a class="nav-link px-lg-3 py-3 py-lg-4" href="{{url_for('blog.about')}}">About</a></li>
<li class="nav-item"><a class="nav-link px-lg-3 py-3 py-lg-4" href="{{url_for('blog.post')}}">Sample Post</a></li>
<li class="nav-item"><a class="nav-link px-lg-3 py-3 py-lg-4" href="{{url_for('blog.contact')}}">Contact</a></li>

```
**Its worth mentioning that** if we just worked without ```blueprint```, we would just write the function name in ```url_for()``` function. But now we are 
using apps, so we have to define them as follows : ```'blueprint_variable.function_name'```. Our blueprint variable is blog. So we used ```blog.index``` and so
on to redirect them.

Now that all the navbar of the ```index.html```,```contact.html```,```about.html```,```post.html``` are same. so we bring in jinja template to make ```index.html``` as our basic html file, and then extend the file in the other html files. Lets modify it :
***
1. First of all we take note that all the ```<nav>``` are same for all the html files.

2. All elements under ```<header>``` tag has differences among all the files.

3. The ```<body>``` of all the html files are different.
---
So we take note of this and create some jinja syntax inside ```index.html``` file :

```html+jinja
<!DOCTYPE html>
<html lang="en">
    <head>     ...    </head>
    <body>
        <!-- Navigation-->
        <nav class="navbar navbar-expand-lg navbar-light" id="mainNav"> (navbar content compressed) </nav>

        <!-- Page Header-->

{% block header %}
              <header class="masthead" style="background-image: url('assets/img/home-bg.jpg')">  (header content compressed) </header>
{% endblock header %}


{% block content %}
        <!-- Main Content-->  (Main block content compressed) </div>
{% endblock content %}



        <!-- Footer-->
        <footer class="border-top"> (Footer content compressed) </footer>

        <!-- Bootstrap core JS-->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
        <!-- Core theme JS-->
        <script src="js/scripts.js"></script>
    </body>
</html>
```
We made sure that the ```head```, ```navbar```, ```footer``` remains same for all the files. After that on the other files we cut all the 
```head```, ```navbar```, ```footer``` tags, since we are directly inheriting from index.html. we redefine their files at the top by saying:

 ```jinja
{% extends 'index.html' %}

other stuffs
```
Now if we go back and run our application, it will run fine:

![second](https://github.com/isfar17/Flask_Tutorial/blob/master/08.Project%20-1_wIth%20different%20static%20folder/image/basic_routing.jpg)

Now we can route from one page to another by clicking on the links. But its just the basic skeleton of the site. Js, css, assets needs to added too.

## 4. Static files adding and a Hectic Journey
Solution of all the problem related to flask static can be found here :
 <a href="https://stackoverflow.com/questions/22152840/flask-blueprint-static-directory-does-not-work">https://stackoverflow.com/questions/22152840/flask-blueprint-static-directory-does-not-work</a>

Now we are at our final part. The static portion is stressing as its neccessary to understand the internal problem and code. Now we go back to
our ```views.py``` file. We re-write ```blog``` again :

```python
blog=Blueprint("blog",__name__,template_folder="templates/blog",static_folder="static",static_url_path="blog/static")
```

Here ``static_folder`` is defined as ``static``, because we used ```static``` named folder in our blog app. Without defining ```static_folder``` to ``static``
and ```static_url_path``` to ```"blog/static"``` flask would search for ``static`` directory in ``project`` directory, or in other words, in the main directory.
This would return the following error in terminal:

```
127.0.0.1 - - [18/Aug/2023 21:17:19] "GET /css/styles.css HTTP/1.1" 404 -
127.0.0.1 - - [18/Aug/2023 21:17:19] "GET /assets/img/post-sample-image.jpg HTTP/1.1" 404 -
127.0.0.1 - - [18/Aug/2023 21:17:19] "GET /js/scripts.js HTTP/1.1" 404 -
127.0.0.1 - - [18/Aug/2023 21:17:19] "GET /assets/img/post-bg.jpg HTTP/1.1" 404 -
```

Although everything is showing good, but 404 means not found. Its looking at the wrong directory. so we need to manually set the directory direction.
After that we go to ```index.html``` file and look at the css linker tag. We relocate the ``href`` by the following :

From this:
```html
<link href="css/styles.css" rel="stylesheet" />
```

to this:
```html
<link href="{{url_for('blog.static',filename='css/styles.css')}}" rel="stylesheet" />
```

Do the following for all the js and other css,jss linker tag. Now what happened here?

Since we no are using seperate app's ```static``` folder, not the default flask ```static``` folder, we use ```blog.static``` to tell the url_for()
function that this is the static of the blog app. The syntax follows : ``'blueprint_variable.static_folder_name'``. In the ``views.py`` file, we 
already defined that the path to static folder url is ```"blog/static"```. And the reason for this is we structured our app previously where
we added static folder like this :
```
-> project
     -> blog
        -> static
```
So now flask will go to this folder to look for the stuffs. Now we dont have to worry about the ``filename`` directory location. Flask is pointing static folder as the ``blog.static`` folder. SO all the files,folder under ```static``` is now available. we just write ``css.styles.css`` simply to point the css file and in case of js:

This :```<script src="js/scripts.js"></script>```
 
Turned to this: ```<script src="{{url_for('blog.static',filename='js/scripts.js')}}"></script>```

Now if we reload the app, we will see a beautiful nearly completed app:

![modified](https://github.com/isfar17/Flask_Tutorial/blob/master/08.Project%20-1_wIth%20different%20static%20folder/image/after_css_js_connection.jpg)

And in terminal we will see results.
```
127.0.0.1 - - [18/Aug/2023 21:51:01] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [18/Aug/2023 21:51:01] "GET /blog/static/js/scripts.js HTTP/1.1" 304 -
127.0.0.1 - - [18/Aug/2023 21:51:01] "GET /blog/static/css/styles.css HTTP/1.1" 304 -
127.0.0.1 - - [18/Aug/2023 21:51:01] "GET /blog/static/assets/img/home-bg.jpg HTTP/1.1" 304 -
127.0.0.1 - - [18/Aug/2023 21:51:01] "GET /blog/static/assets/favicon.ico HTTP/1.1" 304 -
```

Here We are not getting 404 eror, means it is found. So we successfully connected all the static, templates now.
What's remaining is adding the images in the background.

## 5. Adding the images to finish 
Any errors or not connecting images , this type of errors i faces and found soltion here: <a href="https://stackoverflow.com/questions/39579666/how-to-set-background-image-on-flask-templates">https://stackoverflow.com/questions/39579666/how-to-set-background-image-on-flask-templates</a>

Now we have learnt ```url_for()``` is a very powerful function in flask application. We go to ```index.html``` file and inspect where is the background image been used. We can see that in the header tag there is a ``background-image`` variable in ``header`` tag. We see:

```html 
<header class="masthead" style="background-image: url('assets/img/home-bg.jpg')">
```

We have to change url type. We use as usual ``url_for()`` function inside ``url()`` function:

```html 
<header class="masthead" style="background-image : url({{url_for('blog.static',filename='assets/img/home-bg.jpg')}})" >
```

Here VS Code might some erros such as  ``at-rule or selector expected`` or ``) expected`` types errors. But in real case, there is no error. So are good to go. Let's analyze what is happening here. We removed single quotation mark, as it nowdays not neccessary according to the link above. It gives the soltution to not connecting the image problem too. Then as usual, we are telling that the static folder to choose ``blog.static`` and filname is just ``assets/img/all images`` since static is already accessed.

Save everything and the site will run perfectly:

![final](https://github.com/isfar17/Flask_Tutorial/blob/master/08.Project%20-1_wIth%20different%20static%20folder/image/last_look.jpg)

























