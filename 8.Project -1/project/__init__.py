from flask import Flask


app=Flask(__name__)

from project.blog.views import blog


app.register_blueprint(blog,url_prefix="/")