from app import app, login, utils
from flask import render_template, request, send_file
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
    msg_err = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.tentaikhoan == username.strip(),
                                 User.matkhau == password).first()
        if user:
            login_user(user=user)
            return redirect('/admin')
        else:
            msg_err = 'Tên tài khoản hoặc mật khẩu không đúng!!!'
            return render_template('admin/login.html', msg_err=msg_err)

@app.route("/admin/bangxephangview/xuatbxh")
def xuat_bxh():
    return send_file(utils.xuat_bxh_csv())


@app.route("/admin/danh-sach-cau-thu-ghi-ban.html/xuatctgb")
def xuat_ct_gb():
    return send_file(utils.xuat_ct_gb_csv())

@app.route("/admin/loaibanthang/themloaibanthang")
def them_loai_banthang():
    return render_template('admin/create/create-loai-ban-thang.html')


if __name__ == "__main__":
    from app.admin import *

    app.run(debug=True, port=8800)
