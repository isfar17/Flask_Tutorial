from flask import Flask,render_template

app=Flask(__name__)

@app.route("/")
def index():
    list1=[i for i in range(1,100)]
    return render_template("index.html",list1=list1)


if __name__=="__main__":
    app.run(debug=True)