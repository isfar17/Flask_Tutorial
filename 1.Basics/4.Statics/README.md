# Static file/link connection with url_for() function.

Now since we know how things works with url_for(), we can use it/ must use it to link to any css/js/image to modify element/(add/show image) in html file.
Lets see the example.

In  the Program folder, we must create a ``static`` folder. Flask automatically searches for statics files in static folder. So its better for beginners to
use the same name. Now in the static folder we put an image. we need to link it to our html file. First we write in our ``app.py`` file :
```python
from flask import Flask,render_template

app=Flask(__name__)

@app.route('/')
def index(): 
    return render_template("index.html")

@app.route("/new")
def new():
    return render_template("another.html")

if __name__=='__main__':
    app.run(debug=True)
```
We modified our previous code and added the new function. The new function returns another html file which we now will create in ``templates`` folder. The folder 
contains:
```html+jinja
{% extends 'base.html' %}

{% block body %}
    
<!-- We can put css folder directory to any directory here using url_for -->


<img src="{{url_for('static',filename='sample.png')}}" width="500px" height="300px" alt="" srcset="">

{% endblock body %}

```

So what happened here? In the first portion of the url_for(), we write the folder name where the file is located. Then in the second part we define where the file
is or the location of the file.If we run the app, we will a picture like down below:

![image](https://github.com/isfar17/Flask_Tutorial/blob/master/1.Basics/4.Statics/image/static_image.jpg)
