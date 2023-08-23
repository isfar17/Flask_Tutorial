from flask import Blueprint,render_template

blog=Blueprint("blog",__name__,template_folder="templates/blog",static_folder="static",static_url_path="blog/static")

@blog.route("/")
def index():
    #return "hellow world"
    return render_template("index.html")

@blog.route("/post")
def post():
    return render_template("post.html")

@blog.route("/about")
def about():
    return render_template("about.html")

@blog.route("/contact")
def contact():
    return render_template("contact.html")