import warnings
from datetime import timedelta
from flask import Flask
from pymongo import MongoClient
from flask_cors import CORS


warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__)
app.secret_key = 'gazwsxedcrfvtgbyhnujmik10p123456 '
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
client = MongoClient("mongodb://localhost:27017") #host uri
db = client.aksharDB
CORS(app, resources={r"*": {"origins": "*"}})

app.app_context().push()

from base.com import controller
