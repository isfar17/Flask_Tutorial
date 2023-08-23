from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
app=Flask(__name__)
#-------------------------Added-------------------
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"
app.config["SECRET_KEY"]="cryptic"

login_manager=LoginManager()
db=SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view="auth.login" # type: ignore
#---------------------------------------------
from project.common.views import common
from project.profile.views import profile
from project.auth.views import auth #dont forget to add project.app.view (i always forget and get no module found error)


app.register_blueprint(common,url_prefix="/")
app.register_blueprint(profile,url_prefix="/profile")
app.register_blueprint(auth,url_prefix="/auth")