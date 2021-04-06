from flask import Flask
from flask_login import LoginManager
from .config import Config
from flaskext.mysql import MySQL


app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'MealPlanOrganizer'

#login_manager = LoginManager()
#login_manager.init_app(app)
#login_manager.login_view = 'login'

app.config.from_object(Config)
from app import views