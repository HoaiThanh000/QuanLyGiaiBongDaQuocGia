from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Time, Boolean
from sqlalchemy.orm import relationship
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import UserMixin, logout_user, current_user
from app import db, admin
from flask import redirect


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class DoiBong(db.Model):
    __tablename__ = "doibong"

    MaDoi = Column(Integer, primary_key=True, autoincrement=True)
    TenDoi = Column(String(50), nullable=False)
    SanNha = Column(String(100), nullable=False)
    ds_cauthu = relationship('CauThu', backref='doibong', lazy=True)


class LoaiCauThu(db.Model):
    __tablename__ = "loaicauthu"

    MaLoaiCauThu = Column(Integer, primary_key=True, autoincrement=True)
    TenLoaiCauThu = Column(String(50), nullable=False)
    ds_cauthu = relationship('CauThu', backref='loaicauthu', lazy=True)


class CauThu(db.Model):
    __tablename__ = "cauthu"

    MaCauThu = Column(Integer, primary_key=True, autoincrement=True)
    TenCauThu = Column(String(50), nullable=False)
    NgaySinh = Column(DateTime, nullable=False)
    GhiChu = Column(String(100), nullable=True)
    maloaicauthu = Column(Integer, ForeignKey(LoaiCauThu.MaLoaiCauThu), nullable=False)
    madoi = Column(Integer, ForeignKey(DoiBong.MaDoi), nullable=False)
    ds_banthang = relationship('BanThang', backref='cauthu', lazy=True)


class VongDau(db.Model):
    __tablename__ = "vongdau"

    MaVongDau = Column(Integer, primary_key=True, autoincrement=True)
    TenVongDau = Column(String(50), nullable=False)
    ds_trandau = relationship('TranDau', backref='vongdau', lazy=True)


class TranDau(db.Model):
    __tablename__ = "trandau"

    MaTranDau = Column(Integer, primary_key=True, autoincrement=True)
    DoiChuNha = Column(Integer, ForeignKey(DoiBong.MaDoi), nullable=False)
    DoiKhach = Column(Integer, ForeignKey(DoiBong.MaDoi), nullable=False)
    NgayThiDau = Column(DateTime, nullable=False)
    GioThiDau = Column(Time, nullable=False)
    SanThiDau = Column(String(50), nullable=False)
    TySo = Column(String(10), nullable=True)
    mavongdau = Column(Integer, ForeignKey(VongDau.MaVongDau), nullable=False)


class LoaiBanThang(db.Model):
    __tablename__ = "loaibanthang"

    MaLoaiBanThang = Column(Integer, primary_key=True, autoincrement=True)
    TenLoaiBanThang = Column(String(50), nullable=False)
    ds_banthang = relationship('BanThang', backref='loaibanthang', lazy=True)


class BanThang(db.Model):
    __tablename__ = "banthang"

    MaBanThang = Column(Integer, primary_key=True, autoincrement=True)
    MaCauThu = Column(Integer, ForeignKey(CauThu.MaCauThu), nullable=False)
    MaLoaiBanThang = Column(Integer, ForeignKey(LoaiBanThang.MaLoaiBanThang), nullable=False)
    ThoiDiem = Column(String(10), nullable=False)
    MaTranDau = Column(Integer, ForeignKey(TranDau.MaTranDau), nullable=False)


class QuiDinh(db.Model):
    __tablename__ = "quidinh"

    MaMuaGiai = Column(Integer, primary_key=True, autoincrement=True)
    TuoiToiThieu = Column(Integer, nullable=False)
    TuoiToiDa = Column(Integer, nullable=False)
    SoCauThuToiThieu = Column(Integer, nullable=False)
    SoCauThuToiDa = Column(Integer, nullable=False)
    SoCauThuNuocNgoaiToiDa = Column(Integer, nullable=False)
    SoLuongCacLoaiBanThang = Column(Integer, nullable=False)
    ThoiDiemGhiBanToiDa = Column(Integer, nullable=False)
    DiemSoThang = Column(Integer, nullable=False)
    DiemSoThua = Column(Integer, nullable=False)
    DiemSoHoa = Column(Integer, nullable=False)
    ## 1: bàn thắng
    ## 2: Hiệu số
    ## 3: Điểm
    ## 4: Đối Kháng
    ## lưu: "1234"
    ThuTuUuTien = Column(String(10), nullable=False)


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated


# Đội bóng
class DoiBongModelView(AuthenticatedView):
    column_display_pk = False
    can_delete = True
    can_export = True


# Cầu thủ
class CauThuModelView(AuthenticatedView):
    column_display_pk = False
    can_delete = True
    can_export = True


# Loại cầu thủ
class LoaiCauThuModelView(AuthenticatedView):
    column_display_pk = False
    can_delete = True
    can_export = True


# Bàn Thắng
class BanThangModelView(AuthenticatedView):
    column_display_pk = False
    can_delete = True
    can_export = True


# Loại Bàn Thắng
class LoaiBanThangModelView(AuthenticatedView):
    column_display_pk = False
    can_delete = True
    can_export = True


# Trận đấu
class TranDauModelView(AuthenticatedView):
    column_display_pk = False
    can_delete = True
    can_export = True


# Vòng đấu
class VongDauModelView(AuthenticatedView):
    column_display_pk = False
    can_delete = True
    can_export = True


# Qui Định
class QuiDinhModelView(AuthenticatedView):
    column_display_pk = False
    can_delete = True
    can_export = True


admin.add_view(DoiBongModelView(DoiBong, db.session))
admin.add_view(CauThuModelView(CauThu, db.session))
admin.add_view(LoaiCauThuModelView(LoaiCauThu, db.session))
admin.add_view(BanThangModelView(BanThang, db.session))
admin.add_view(LoaiBanThangModelView(LoaiBanThang, db.session))
admin.add_view(TranDauModelView(TranDau, db.session))
admin.add_view(VongDauModelView(VongDau, db.session))
admin.add_view(QuiDinhModelView(QuiDinh, db.session))
admin.add_view(LogoutView(name="Đăng xuất"))

if __name__ == "__main__":
    db.create_all()
