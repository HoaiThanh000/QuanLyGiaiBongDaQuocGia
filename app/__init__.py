from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
from twilio.rest import Client


app = Flask(__name__)

app.secret_key = "\x0f\xc8\xf8hNvH\xb6[R\xd2\xf3\x90B\xfdK"

app.config[
    "SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:ithades1@localhost/db_quanlygiaibongdaquocgia?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)

admin = Admin(app=app, name="QUAN LY GIAI BONG DA QUOC GIA", template_mode="bootstrap3")

login = LoginManager(app=app)

account_sid = "ACdd5c869458bf4ef18f8eeee1c6efbe82"
auth_token = "bc7fcec21af2c74f4b5819f63cc1b401"

client = Client(account_sid, auth_token)
