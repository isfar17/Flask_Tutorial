from myproject import db
from flask_admin.contrib.sqla import ModelView

class SecondClass(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)

    def __init__(self,name):
        self.name=name

    def __repr__(self):
        return f"{self.id} -> {self.name}"

class Fun(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(200),nullable=False)


    def __repr__(self):
        return f"{self.id} -> {self.name}"
    
#--Modification for Admin View------
class Modified_Fun(ModelView):
    form_choice=["name","email"]
    column_list=["name","email"]