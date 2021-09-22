from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://yuhrdsirwpolco:7aea924be590abbc9796942fd42780af1247a9e441f8b6695c1178de7b458d72@ec2-18-215-44-132.compute-1.amazonaws.com:5432/drbpddj3emimv'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from meetingRoomBooking import routes
