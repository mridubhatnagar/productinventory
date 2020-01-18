from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect

csrf = CsrfProtect()
app = Flask(__name__)
app.config['SECRET_KEY']='mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost:3306/inventory'
db=SQLAlchemy(app)
csrf.init_app(app)
from inventory import routes
