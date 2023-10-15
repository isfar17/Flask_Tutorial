from flask import Flask,render_template,request,redirect,url_for,send_file#need sendfile to download
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO


#-----------------------------------------------------
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"
app.config["SECRET_KEY"]="secret"
db=SQLAlchemy(app)


class Upload(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    file=db.Column(db.LargeBinary)
#------------------------------------------------
@app.route('/')
def index():
    return render_template("index.html")

'''
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
'''
#send files parameters:
''' :param path_or_file: The path to the file to send, relative to the
        current working directory if a relative path is given.
        Alternatively, a file-like object opened in binary mode. Make
        sure the file pointer is seeked to the start of the data.
    :param mimetype: The MIME type to send for the file. If not
        provided, it will try to detect it from the file name.
    :param as_attachment: Indicate to a browser that it should offer to
        save the file instead of displaying it.'''
@app.route("/download/<int:id>")
def download(id):
    query_image=Upload.query.filter_by(id=id).first()
    
    return send_file(query_image.file,download_name=query_image.name,as_attachment=True)


    #or return send_file(path_or_file=BytesIO(query_image.file),download_name=query_image.name, as_attachment=True)


if __name__=='__main__':
    app.run(debug=True)