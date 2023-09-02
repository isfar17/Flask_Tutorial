from flask import Flask,render_template,redirect,url_for,session,flash
#importing the class
from flask_wtf import FlaskForm
#importing the fields.
from wtforms import (StringField,TextAreaField,IntegerField,BooleanField,
                     DateTimeField,SubmitField,RadioField,SelectField)
#VALIDATORS which will automatically check if given data fulfileld conditions
from wtforms.validators import DataRequired,Email
#ADVANCED flask module to look flask form look better with boostrap.
#if i want traditional and custom defined flask forms, i can cut line 11,13
from flask_bootstrap import Bootstrap
#boostrap is a tool installed which can beautify html files with boostrap class
#we want to beautify the html form. so we have used this.if we want custom
#made form, we can ignore it and remove it.

app=Flask(__name__)
Bootstrap(app)#bootstrap linked ,later rendered in html files. see in index.html
#as of now 2023 boostrap flask supports boostrap4 only

#While using wt_forms/any type of FORMS we have to configure secret key
app.config["SECRET_KEY"]="abcd"

#---------Creating The Tables of Fields-----#
class Form(FlaskForm):
    #variable=FieldName("label",validators=[imported validators])
    name=StringField("What is your name?",validators=[DataRequired("There must be a name!")])
    text=TextAreaField("What is your TEXT?",validators=[DataRequired()])
    age=IntegerField("What is your age?",validators=[DataRequired()])
    bool_value=BooleanField("Are you human?")           
    choice=RadioField("Choose your favourite game?",choices=[("Cricket","Cricket"),("Football","Football")])#(value,label)
    select=SelectField("Select your favourite game?",choices=[("Cricket","Cricket"),("Football","Football")])
    submit=SubmitField("Submit")


@app.route("/",methods=["GET","POST"])
def index():

    form=Form()#creating the form object
    if form.validate_on_submit():#checking values
        flash("you submitted form successfully!")
        session["name"]=form.name.data
        session["text"]=form.text.data
        session["age"]=form.age.data
        session["bool_value"]=form.bool_value.data
        session["choice"]=form.choice.data
        session["select"]=form.select.data
        session["submit"]=form.submit.data

        #session is a special thing. so we dont have to pass additional data into 
        #the other redirected function. session will store it and you can use it 
        #in your own html file and python function directly
        
        return redirect(url_for("view"))#use this function to redirect to another python function


    return render_template("index.html",form=form)


@app.route("/view",methods=["GET","POST"])
def view():
    return render_template("view.html")




if __name__=="__main__":
    app.run(debug=True)