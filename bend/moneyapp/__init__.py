from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
from moneyapp.routes import *
from moneyapp.models import db

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/profile_pics')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'thisisansecretkey'
app.config['JSON_SORT_KEYS'] = False

app.register_blueprint(routes)
db.init_app(app)


# from moneyapp import routes 



