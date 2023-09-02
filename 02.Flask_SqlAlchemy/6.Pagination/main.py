from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///databse.db"
db=SQLAlchemy(app)


class Blog(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200))
    content=db.Column(db.String(200))
    
'''
required only once to run

ll=[i for i in range(100)]

for i in ll:
    with app.app_context(): #see commands.txt for the reason of using this
        title=f"Title number {i}"
        content=f"Content number {i}"
        data=Blog(title=title,content=content)
        db.session.add(data)
        db.session.commit()
        print(title,content)
'''

@app.route("/")
def hello():
    return "Hello! use /numbers to go through the query data show"


@app.route('/<int:page_val>')
def index(page_val):
    # query=Blog.query.all()
    query=Blog.query.paginate(per_page=3,page=page_val)
    return render_template("index.html",query=query)

''' from the internal code doc (param=parameter)
    :param select: The ``select`` statement to paginate.
        :param page: The current page, used to calculate the offset. Defaults to the
            ``page`` query arg during a request, or 1 otherwise.
        :param per_page: The maximum number of items on a page, used to calculate the
            offset and limit. Defaults to the ``per_page`` query arg during a request,
            or 20 otherwise.
        :param max_per_page: The maximum allowed value for ``per_page``, to limit a
            user-provided value. Use ``None`` for no limit. Defaults to 100.
        :param error_out: Abort with a ``404 Not Found`` error if no items are returned
            and ``page`` is not 1, or if ``page`` or ``per_page`` is less than 1, or if
            either are not ints.
        :param count: Calculate the total number of values by issuing an extra count
            query. For very complex queries this may be inaccurate or slow, so it can be
            disabled and set manually if necessary.

'''

if __name__=='__main__':
    app.run(debug=True)