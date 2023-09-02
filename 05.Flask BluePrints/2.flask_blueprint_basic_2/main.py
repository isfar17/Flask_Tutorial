from flask import Flask

app=Flask(__name__)

from firstapp.views import firstapp
from secondapp.views import secondapp

# now in the main app we have to imoprt the blueprint variables we set earlier
# to register them into blurprint
app.register_blueprint(firstapp)
app.register_blueprint(secondapp)


if __name__=="__main__":
    app.run(debug=True) #we dont have to define any views here. because it will automatically redirect to "/" where
                        #we earlier in the first app, set index as "/" here. so app will go to firstapp first