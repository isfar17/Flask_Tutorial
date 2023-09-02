from flask import Flask
from firstapp.views import firstapp
from flask_admin import Admin
'''if we know about blueprints, we know that we create separate apps and then we use them with blueprint variable
declared within their folders python file. then we register them into the project __init__ file or main.py file() in
case of single app). Then we import Admin and admin.view and models from model.py file to view them into
/admin  route. we now can modify admin views unlike previous admin tutorial'''

app=Flask(__name__)
admin=Admin()
admin.init_app(app)


#importing the blurprint variable from the app and then registering
app.register_blueprint(firstapp)



if __name__=="__main__":
    app.run(debug=True)