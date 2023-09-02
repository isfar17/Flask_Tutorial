from project.model import User
from project import db,app

with app.app_context(): #Now we have to use app.app_Context() to work with database outside of app file
    for i in range(20):
        username=f"User {i}"
        password=f"Password {i}"
        data=User(name=username,password=password)
        db.session.add(data)
        db.session.commit()