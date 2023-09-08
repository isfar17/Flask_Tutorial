from flask import Flask
from firstapp.views import firstapp


app=Flask(__name__)

#importing the blurprint variable from the app and then registering
app.register_blueprint(firstapp,url_prefix="/")


if __name__=="__main__":
    app.run(debug=True)