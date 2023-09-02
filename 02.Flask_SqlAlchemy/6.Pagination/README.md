# Pagination with SQLAlchemy 
When building a search engine or a blog app, we dont want to show all the query results in one page. Because that would be a very long big page if there were 10k posts
or search results. So we need a solution to break the results into parts and show them only when clicked. This breaking queries into parts is known as Pagination.

Flask supports pagination. And it is really easy to make. Lets build our app first:
```python
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///databse.db"
db=SQLAlchemy(app)

class Blog(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200))
    content=db.Column(db.String(200))    

@app.route("/")
def hello():
    return "Hello! use /numbers to go through the query data show"

if __name__=='__main__':
    app.run(debug=True)
```
We go to command line and create database, and if we run the app, everything works just fine like down below:
![first](https://github.com/isfar17/Flask_Tutorial/blob/master/02.Flask_SqlAlchemy/6.Pagination/image/first_pic.jpg)

After that, we go to our views, and write  code for pagination. In our file, we write a very simple code:
```python
@app.route('/<int:page_val>')
def index(page_val):
    # query=Blog.query.all()
    query=Blog.query.paginate(per_page=3,page=page_val)
    return render_template("index.html",query=query)
```
Here we take an integer or page_val as the arguement for the function. Then here ``query=Blog.query.paginate(per_page=3,page=page_val)`` is the query type
for pagination. We create a pagination object of the ``Blog`` Table.The pagination object splits the results or the data of the table into multiple segments and
returns a list We then pass ``per_page`` paramater where we set how many object/results we want to show per page. The next parameter ``page`` takes the page 
number and gives the result of that particular page(if exists). So if anyone passes the page number 6, the ``query`` object returns the result of the 6th page' 
result. After that we return the query result in the ``index.html`` file.

```html+jinja
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVST
    QN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

    <title>{% block title %}Base{% endblock title %}</title>
  </head>

  <body>
    {% block body %}
<div class="container">
    <br>

{% for q in query %}
    

    <div class="card" style="width: 18rem;">
        <div class="card-body">
          <h5 class="card-title">{{q.id}}</h5>
          <h6 class="card-subtitle mb-2 text-muted">{{q.title}}</h6>
          <p class="card-text">{{q.content}}</p>
        </div>
      </div>
      {% endfor %}
        {% endblock body %}
    </nav>
</div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/
      bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
</body>
</html>

```
Here we are looping through the list we sent and print the pagination object on the page.

```html+jinja
{% for q in query %}
    <div class="card" style="width: 18rem;">
        <div class="card-body">
          <h5 class="card-title">{{q.id}}</h5>
          <h6 class="card-subtitle mb-2 text-muted">{{q.title}}</h6>
          <p class="card-text">{{q.content}}</p>
        </div>
      </div>
      {% endfor %}
```
Here, we took the class sample from Bootstrap Sample page, and copy pasted here. Then we loop through and in every loop a ``card`` will be added with data 
inside it. So now if we run the app, we will be taken to our base page we saw earlier. Now if we type ``127.0.0.0/1`` we will see results like this:
![second](https://github.com/isfar17/Flask_Tutorial/blob/master/02.Flask_SqlAlchemy/6.Pagination/image/second.jpg)
Thus for every page we will see results like this until we get to end. But there is a thing. If no result is fetched, suppose there are 10 data only and
per page , we set to see 5 posts. So we can only paginate 2 times. But if we write ``127.0.0.0/5``, we get no url/ no page found. Why? Because there will be
no results to show, And thus we get a None result. And the url won't be valid anymre.

Now instead of going to the pages one by one, we can use links to go there. We see in all the websites some kind of trails of numbers such as : 1,2,3...last like 
this. So we can use this feature here too. Lets copy a Bootstrap Pagination Trail code. Then copy-paste into the html file:
```html+jinja
<nav aria-label="Page navigation example">
  <ul class="pagination">
    <li class="page-item"><a class="page-link" href="#">Previous</a></li>
    <li class="page-item"><a class="page-link" href="#">1</a></li>
    <li class="page-item"><a class="page-link" href="#">2</a></li>
    <li class="page-item"><a class="page-link" href="#">3</a></li>
    <li class="page-item"><a class="page-link" href="#">Next</a></li>
  </ul>
</nav>
```
And we can see in the end of the  result in every page, we get some numbers. Now lets modify it so that we can use it with flask.
```html+jinja
<nav aria-label="Page navigation example">
  <ul class="pagination">

      {% for page in query.iter_pages(left_edge=3,right_edge=3)  %}
          {% if page %}        
          <li class="page-item"><a class="page-link" href="{{ url_for('index',page_val=page) }}">{{page}}</a></li>
          {%else%}
          ...
      {% endif %}
      {% endfor %}
  </ul>
</nav>
```
The pagination reference is taken from boostrap 5. Now since we are using query.paginate() function, we have access to iteration through page numbers. 
So we are using that query.iter_page() function to use it in pagination.```{% for page in query.iter_pages(left_edge=3,right_edge=3)  %}```. One thing
ensuring noting that **WE MUST USE IF ELSE STATEMENT WHILE WRITING PAGINATION SYSTEM**. This is because PAGINATION would not show every single iteration. 
It will show couple of the numbers, Then some of the middle and some of the last. This is how paginatin works.So we must not forget that and use if statment 
to make sure if there page exists or its just None. 
```html+jinja
          {% if page %}        
          <li class="page-item"><a class="page-link" href="{{ url_for('index',page_val=page) }}">{{page}}</a></li>
          {%else%}
```
Here we check if there is a page number being generated, since pagintation at a point gives None and at the end again returns last numbers. Then we set its
url to the ``view`` function we wanted to set previously. We are also passing the ``page``value here as an arguement. Without
using (if else ) statment, we will get ``build_error``. Because since pagination object returns None after some numbers, at one point, None will be passed in 
url_for() function which would fail to build a route ``/none`` and it does not exists. Also we cant use ``int`` with ``None``. We used left_edge and right_edge
to tell how many numbers to show each side before its a none page. Then if there is None after 3 numbers, we will show ... dots which have been showed using else
statement.

Now we run the app and go to ``/1`` and see the results:
![third](https://github.com/isfar17/Flask_Tutorial/blob/master/02.Flask_SqlAlchemy/6.Pagination/image/third.jpg)

If we click we wil be taken to those results.






