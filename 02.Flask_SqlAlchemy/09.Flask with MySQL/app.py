from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="mysql://root:@localhost/testdb"
                            #="databasename://username:password(in our case its null)@servername/databasename
db=SQLAlchemy(app)

class Test_Table(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(200),nullable=False)
    password=db.Column(db.String(200),nullable=False)

    def __init__(self,name,email,password):
        self.name=name
        self.email=email
        self.password=generate_password_hash(password)




@app.route('/')
def index():
    #run only once to input data while running the app
    # for i in range(10):
    #     with app.app_context():
    #         name=f"Name {i}"
    #         email=f"email{i}@gmail.com"
    #         password=f"Password {i}"
    #         user=Test_Table(name=name,email=email,password=password)
    #         db.session.add(user)
    #         db.session.commit()
    #         print(f"Added user {name} -> {email}")
    print("App Finished putting data into databse") 
    return 'hello world'

#pagination review
@app.route("/page/<int:number>") # type: ignore
def pagination(number):
    query=Test_Table.query.paginate(page=number,per_page=4)
    return render_template("index.html",queries=query)

if __name__=='__main__':
    app.run(debug=True)
    
#we only had to learn sqlalchemy basic commands. that worked for sqlite and mysql in the same way
#except for their connections. thats it!