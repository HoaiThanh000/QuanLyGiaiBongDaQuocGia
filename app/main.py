from pip._vendor.requests.compat import str

from app import app, login
from flask import render_template, redirect, request
from flask_login import login_user
from app.models import *
import hashlib


@app.route("/")
def index():
    return render_template("index.html")


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/login-admin", methods=['post', 'get'])
def login_admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.tentaikhoan == username.strip(),
                                 User.matkhau == password).first()
        if user:
            login_user(user=user)
    return redirect("/admin")


if __name__ == "__main__":
    from app.admin import *

    app.run(debug=True, port=8800)
