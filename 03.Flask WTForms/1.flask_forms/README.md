# Creating html forms with Flask WTForm

There are basically 2 types of creating form in flask. One is using normal html form tag, another is Flask WTForms. The first one is the basic one. We don't need any
tutorial on this. But the second one is neccessary. That is WTForms. We literally can create our forms in python file and can render the form in HTML file easily.

Let's create our basic app :
```python
from flask import Flask,render_template

app=Flask(__name__)

app.config["SECRET_KEY"]="abcd"

@app.route('/')
def index(): 
    return render_template("index.html")

if __name__=='__main__':
    app.run(debug=True)

```
While passing data from form to server, we need  a secret key to match. Because anyone can redirect form data from their sites to our server and can damage.
So we always need a  secret key.Then we also create ``templates`` folder to store our html files there. Now include and import modules of flask form :
```python
from flask_wtf import FlaskForm
#importing the fields.
from wtforms import (StringField,TextAreaField,IntegerField,BooleanField,
                     DateTimeField,SubmitField,RadioField,SelectField)
#VALIDATORS which will automatically check if given data fulfileld conditions
from wtforms.validators import DataRequired,Email
```
Here we are ipmorting FlaskForm class. The FlaskForm class imports the functionalities of forms. Now we also the fields such as an email field,password field,
textfield,submitfield etc. We import the form data types. Last we import some validators. This is very important in some cases. An Email validators checks if the
input value is an email. The DataRequired makes sure that data has been passed into the form or like we dont send empty form to python app.
Now we create our first Form with FaskForm  class:

```python
class Form(FlaskForm):
    #variable=FieldName("label",validators=[imported validators])
    name=StringField("What is your name?",validators=[DataRequired("There must be a name!")])
    text=TextAreaField("What is your TEXT?",validators=[DataRequired()])
    age=IntegerField("What is your age?",validators=[DataRequired()])
    bool_value=BooleanField("Are you human?",validators=[DataRequired()])           
    choice=RadioField("Choose your favourite game?",
                        choices=[("Cricket","Cricket"),("Football","Football")])#(value,label)
    select=SelectField("Select your favourite game?",
                        choices=[("Cricket","Cricket"),("Football","Football")])
    submit=SubmitField("Submit")

```

Its not neccessary to describe the things going on. Because they are easy to understand. The format is 
```python
variable=FieldName("label",validators=[imported validators])
```
where the label tag means the label of the input field. We will see those in pictures later on.
Now down below we need to use the form and send it in the website. Also we need data to pass in the server. We make a function and write down :
```python
@app.route("/",methods=["GET","POST"])
def index():

    form=Form()#creating the form object
    if form.validate_on_submit():#checking values

        name=form.name.data
        text=form.text.data
        age=form.age.data
        bool_value=form.bool_value.data
        choice=form.choice.data
        select=form.select.data
        submit=form.submit.data

        return render_template("view.html",name=name,text=text,age=age,bool_value=bool_value,
                                choice=choice,select=select,submit-submit)


    return render_template("index.html",form=form)

```
Now lets break down everything. We create a form essentially in a variable, then we validate that the if the form is submitted with validation/or the form
has sent any data. 
### Step 1:
**First Case:**
**When the program runs for the first time, there would be no data sent from form except None**. So the first time it will get to the last
line and render ``"index.html"`` file. With the file, we pass our form class in a variable. Then after running the file, we put data and send it here.
**Second Case:**
Now that data is being sent. We will access the form values using ``form.name_form_field.data``. Here as per the variables we created in flask form,
we fetch thier data one by one. Then send them into the ``view.html`` file.
### Step 2:
Now we go to ``index.html`` file and write code like down below:
```html+jinja
{% extends 'base.html' %}
{% block title  %}HomePage{% endblock title  %}

{% block body %}
<br>
<br>
    <div class="container">
        <form method="post">
            <!--Will show basic html structure of form-->
            <div class="form-group">
            {{form.hidden_tag()}}
            {{form.name.label}} {{form.name( class="form-control")}} <br>
            {{form.text.label}} {{form.text}} <br>
            {{form.age.label}} {{form.age}} <br>
            {{form.bool_value.label}} {{form.bool_value}} <br>
            {{form.choice.label}} {{form.choice}} <br>
            {{form.select.label}} {{form.select}} <br>
             {{form.submit}} <br>
            </form>
        </div>
    </div>
    
    {% endblock body %}

```
Let's understand what is going on. Flask has this value based tags to show form data in html file. So we first take ``{{form.hidden_tag}}``. This is the tag
we connect with ``app.config["SECRET_APP"]`` value. After that we use the ``label`` attribute to show the message we wan to. This is what we have mentioned 
about in the first place why we used this. In the next line, we will see the label and the data field.
![look](https://github.com/isfar17/Flask_Tutorial/blob/master/03.Flask%20WTForms/1.flask_forms/image/first.jpg)
Now, We will send data to our server by clicking submit. 2 things to notice :
***
1. We must use ``method=="post"`` to make sure data is sent in correct way.
2. In the python app, before the function, we use this part ,``methods=["GET","POST"]``. Thus data sent process will be ok.
---
After clicking, we will be taken to the ``view.html`` file where we will first write code :
```html+jinja
{% extends 'base.html' %}

{% block title %}View Page{% endblock title %}

{% block body %}

        {{name}} <br>   
        {{age}}<br>
        {{text}}<br>
        {bool_value}}<br>
        {{choice}}<br>
        {{select}}<br>
    </div>
{% endblock body %}
```
see the data like down below: 
![datashow](https://github.com/isfar17/Flask_Tutorial/blob/master/03.Flask%20WTForms/1.flask_forms/image/second.jpg)

**Ignore the Flash Image**. We will deal with it after this part.

