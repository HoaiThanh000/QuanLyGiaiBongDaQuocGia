from pip._vendor.requests.compat import str
from app import dao
from app import app, login
from flask import render_template, redirect, request
from flask_login import login_user
from app.models import *
import hashlib


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cauthu")
def cauthu_list():

    keyword = request.args["keyword"] if request.args.get("keyword") else None
    #Nếu có truyền keyword thì bỏ giá trị keyword vào kw, còn ko truyền thì mặc định là none
    date_start = request.args["date_start"] if request.args.get("date_start") else None
    date_end = request.args["date_end"] if request.args.get("date_end") else None

    return render_template("pages/CauThu-List.html", ct=dao.read_cauthu(keyword=keyword,
                                                                  date_start=date_start,
                                                                  date_end=date_end))

@app.route("/ketqua")
def ketqua():

    return render_template("pages/KetQua.html", tgs=dao.read_thamgia(), bts=dao.read_banthang())

from app.models import *

@app.route("/doibong")
def doibong_list():

    return render_template("pages/DoiBong-List.html", dbg=dao.read_doibong(),vd=dao.read_vongdau())

@app.route("/lichthidau")
def lichthidau():

    return render_template("pages/LichThiDau.html", tds=dao.read_vongdau_dstrandau(), tgs=dao.read_thamgia())

@app.route("/quidinh")
def quidinh():

    return render_template("pages/QuiDinh.html", qds=dao.read_quidinh())


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
