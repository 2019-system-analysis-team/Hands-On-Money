from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
<<<<<<< HEAD
=======
db.create_all()
>>>>>>> a4d987957e36ec7e3ab39334ce4193bff60c8ff5
bcrypt = Bcrypt(app)

from moneyapp import routes 



