from myproject import db

class SecondClass(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)

    def __init__(self,name):
        self.name=name

    def __repr__(self):
        return f"{self.id} -> {self.name}"