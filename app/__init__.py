from flask import Flask
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

app.config['SECRET_KEY']='your_secret_key'

from app import routes