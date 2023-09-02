from flask import Flask


#importing the admin module. needs to be installed.
from flask_admin import Admin
#modelview is neccessary to show and view database in admin panel
from flask_admin.contrib.sqla import ModelView

app=Flask(__name__)
admin=Admin()#define
admin.init_app(app=app)#initialization in the server

@app.route('/')
def index(): 
    return 'hello world'

#go to /admin to view the admin panel. it runs on bootstrap 4.so to modify
#the admin panels look, we need to change the internal code which is advanced

if __name__=='__main__':
    app.run(debug=True)