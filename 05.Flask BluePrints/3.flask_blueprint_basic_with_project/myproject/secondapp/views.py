from flask import Blueprint,redirect,render_template,url_for,request
from myproject import db
from myproject.model import SecondClass
from sqlalchemy import exc


secondapp=Blueprint("secondapp",__name__,template_folder="templates/secondapp")


@secondapp.route("/second",methods=["GET","POST"])
def index():
    return render_template("second_index.html")


@secondapp.route("/second/data_entry",methods=["GET","POST"])
def data_entry():
    try:
        data=SecondClass(name=request.form.get("name"))
        db.session.add(data)
        db.session.commit()
        return "You have successfully inserted data !"
    
    except exc.SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
        return redirect(url_for("secondapp.index"))
'''
<class 'sqlalchemy.exc.IntegrityError'>
127.0.0.1 - - [08/Sep/2023 11:50:58] "GET /second/data_entry HTTP/1.1" 302 -
'''    
