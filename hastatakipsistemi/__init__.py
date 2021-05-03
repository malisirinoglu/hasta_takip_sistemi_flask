from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xab\xf1\x1aT\x99;\xb1~1\xb1\x86I\xd9\xc7\x9c[Lz\xcdL&\xc1\xd4\x93'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)

from hastatakipsistemi import routes