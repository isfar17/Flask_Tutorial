from flask import Flask,render_template,request,send_file
import os
from faker import Faker
fake_data=Faker()
app=Flask(__name__)
app.config['UPLOAD_FOLDER']=os.path.abspath('image')#WITHOUT It flask would return permission denied

'''
first case

from flask import Flask,render_template,request
import os
app=Flask(__name__)
app.config['UPLOAD_FOLDER']=os.path.abspath('image')#WITHOUT It flask would return permission denied

@app.route('/',methods=["GET","POST"])
def index(): 
    if request.method=="POST":
        file=request.files["file"]
        
        if file.filename=="":
            print("NO fILE PROVIDED")
            
        else:
            file.save(os.path.join('image',file.filename))#instead of file.filename
                                                        #if i use only file, it would return error

    return render_template("index.html")

'''
'''
second case

import os

app=Flask(__name__)
app.config['UPLOAD_FOLDER']=os.path.abspath('image')#WITHOUT It flask would return permission denied

@app.route('/',methods=["GET","POST"])
def index(): 
    if request.method=="POST":
        file=request.files["file"]
        if file.filename=="":
            print("No file detected")
        else:
        #before that we will make another Users folder must, or will return error
            fakename="Jubayer"
            if os.path.isdir(f"image/Users/{fakename}"): #returns if the foldewr exists or not
                print("Yes")
                directory=os.path.abspath(f"image/Users/{fakename}")
                print(directory)
                file.save(os.path.join(directory,file.filename)) # type: ignore #instead of file.filename
                                                                 #if i use only file, it would return error
                
            else:                                              
                os.mkdir(f'image/Users/{fakename}') #or else it wil make a new folder
                
                directory=os.path.abspath(f"image/Users/{fakename}")
                print(directory)
                file.save(os.path.join(directory,file.filename))#joins adds a file into an existing folder 
                
    return render_template("index.html")

'''

'''#final version
@app.route('/',methods=["GET","POST"])
def index(): 
    if request.method=="POST":
        # os.mkdir(f'image/{user}')
        file=request.files["file"]
        if file.filename=="":
            print("No file detected")
        else:
            fakename=fake_data.name()
            os.mkdir(f'image/Users/{fakename}')
            if os.path.isdir(f"image/{fakename}"):
                print("Yes")
                directory=os.path.abspath(f"image/Users/{fakename}")
                print(directory)
                file.save(os.path.join(directory,file.filename)) # type: ignore #instead of file.filename
                                                                                #if i use only file, it would return error
            else:
                print("creating a new folder for user")
                directory=os.path.abspath(f"image/Users/{fakename}")
                print(directory)
                file.save(os.path.join(directory,file.filename)) # type: ignore #instead of file.filename
                                      
    return render_template("index.html")

'''
@app.route("/download/<string:user>/<string:name>")
def download(user,name):
    file_dir=os.path.abspath(f'image/Users/{user}/{name}')#gives the directory
    filename=os.path.basename(file_dir) #gives the name of the file
    return send_file(path_or_file=file_dir,download_name=filename,as_attachment=True)

#127.0.0.1/download/Sara White/demo.jpg gives download page to download
if __name__=='__main__':
    app.run(debug=True)