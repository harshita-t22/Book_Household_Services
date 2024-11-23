#starting of app
from flask import Flask
from backend.models import db
from flask_sqlalchemy import SQLAlchemy

app=None

def setup_app():
    global app
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///house_services.sqlite3" #having db file
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push() #direct access to other modules
    print("App context pushed")
    db.init_app(app) #Flask app connected to db(SQL Alchemy)
    print("SQLAlchemy initiaized")
    app.debug=True
    print("Household Service app is started....")


setup_app()

from backend.controllers import *
if __name__=="__main__":
    app.run()