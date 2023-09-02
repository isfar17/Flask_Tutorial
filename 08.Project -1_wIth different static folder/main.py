from project import app

#it just runs the whole project. everytime we need to run the project, we just run main.py
#other files running will return error
if __name__=='__main__':
    app.run(debug=True)