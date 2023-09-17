# Registration and User login with Flask
We previously had seen how ``flask_login`` works. In order to work with ``flask_login``, we had to create new user beofre running the app, or in the database
so that we can have pre registered user in our database. From there, we could use user and password value and log in. But in a real life project, There are 
no pre-built username and password. A new user has to register in the site, and then can log in easily in the webpage. Now we will create a simple registration
form with flask and embed it with flask login. 

First we create our app as usual, with ``templates`` directory:
