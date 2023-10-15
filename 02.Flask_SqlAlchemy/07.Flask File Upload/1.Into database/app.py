from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"
app.config["SECRET_KEY"]="secret"
db=SQLAlchemy(app)


class Upload(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    file=db.Column(db.LargeBinary)

@app.route('/')
def index():
    return render_template("index.html")
    
@app.route('/upload',methods=["GET","POST"])
def upload_file():
    if request.method=="POST":
        file=request.files["file"]
        if file.filename=="":
            print("No file provided")
        else:
            data=Upload(name=file.filename,file=file.read())
            db.session.add(data)
            db.session.commit()
            return redirect(url_for("index"))
         
    return render_template("form.html")



if __name__=='__main__':
    app.run(debug=True)