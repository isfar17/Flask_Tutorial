from flask import Blueprint,redirect,render_template,url_for,request
from myproject import db
from myproject.model import SecondClass
from sqlalchemy import exc


secondapp=Blueprint("secondapp",__name__,template_folder="templates/secondapp")


@secondapp.route("/second",methods=["GET","POST"])
def index():
    return render_template("second_index.html")


@secondapp.route("/second/connect",methods=["GET","POST"])
def connect():
    try:
        data=SecondClass(name=request.form.get("name"))
        db.session.add(data)
        db.session.commit()

    except exc.SQLAlchemyError as e:
        print(type(e))
        return redirect(url_for("second.index"))
    
    
    return redirect(url_for('firstapp.new'))