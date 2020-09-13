from sqlalchemy import Column, String, Integer, ForeignKey, Date, Time, Boolean
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app import db


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(50), nullable=False)
    ngaysinh = Column(Date, nullable=False)
    sodt = Column(String(10), nullable=False)
    diachi = Column(String(100), nullable=False)
    tentaikhoan = Column(String(50), nullable=False)
    matkhau = Column(String(50), nullable=False)

    def __str__(self):
        return self.ten


class DoiBong(db.Model):
    __tablename__ = "doibong"

    madoi = Column(Integer, primary_key=True, autoincrement=True)
    tendoi = Column(String(50), nullable=False)
    sannha = Column(String(100), nullable=False)
    sodt = Column(String(10), nullable=False)
    ds_cauthu = relationship('CauThu', backref='doibong', lazy=True)
    doi_nha = relationship('ThamGia', backref='doi_nha', foreign_keys='ThamGia.doichunha')
    doi_khach = relationship('ThamGia', backref='doi_khach', foreign_keys='ThamGia.doikhach')

    def __str__(self):
        return self.tendoi


class LoaiCauThu(db.Model):
    __tablename__ = "loaicauthu"

    maloaicauthu = Column(Integer, primary_key=True, autoincrement=True)
    tenloaicauthu = Column(String(50), nullable=False)
    ds_cauthu = relationship('CauThu', backref='loaicauthu', lazy=True)

    def __str__(self):
        return self.tenloaicauthu


class CauThu(db.Model):
    __tablename__ = "cauthu"

    macauthu = Column(Integer, primary_key=True, autoincrement=True)
    tencauthu = Column(String(50), nullable=False)
    ngaysinh = Column(Date, nullable=False)
    ghichu = Column(String(100), nullable=True)
    maloaicauthu = Column(Integer, ForeignKey(LoaiCauThu.maloaicauthu), nullable=False)
    madoi = Column(Integer, ForeignKey(DoiBong.madoi), nullable=False)
    ds_banthang = relationship('BanThang', backref='cauthu', lazy=True)

    def __str__(self):
        return self.tencauthu


class VongDau(db.Model):
    __tablename__ = "vongdau"

    mavongdau = Column(Integer, primary_key=True, autoincrement=True)
    tenvongdau = Column(String(50), nullable=False)
    ds_trandau = relationship('TranDau', backref='vongdau', lazy=True)

    def __str__(self):
        return self.tenvongdau


class TranDau(db.Model):
    __tablename__ = "trandau"

    matrandau = Column(Integer, primary_key=True, autoincrement=True)
    tentrandau = Column(String(50), nullable=False)
    mavongdau = Column(Integer, ForeignKey(VongDau.mavongdau), nullable=False)
    ds_banthang = relationship('BanThang', backref='trandau', lazy=True)
    ds_thamgia = relationship('ThamGia', backref='trandau', lazy=True)

    def __str__(self):
        return self.tentrandau


class ThamGia(db.Model):
    __tablename__ = "thamgia"

    doichunha = Column(Integer, ForeignKey(DoiBong.madoi), primary_key=True, nullable=False)
    doikhach = Column(Integer, ForeignKey(DoiBong.madoi), primary_key=True, nullable=False)
    matrandau = Column(Integer, ForeignKey(TranDau.matrandau), primary_key=True, nullable=False)
    ngaythidau = Column(Date, nullable=False)
    giothidau = Column(Time, nullable=False)
    santhidau = Column(String(50), nullable=False)
    tyso = Column(String(10), nullable=True)


class LoaiBanThang(db.Model):
    __tablename__ = "loaibanthang"

    maloaibanthang = Column(Integer, primary_key=True, autoincrement=True)
    tenloaibanthang = Column(String(50), nullable=False)
    ds_banthang = relationship('BanThang', backref='loaibanthang', lazy=True)

    def __str__(self):
        return self.tenloaibanthang


class BanThang(db.Model):
    __tablename__ = "banthang"

    mabanthang = Column(Integer, primary_key=True, autoincrement=True)
    macauthu = Column(Integer, ForeignKey(CauThu.macauthu), nullable=False)
    maloaibanthang = Column(Integer, ForeignKey(LoaiBanThang.maloaibanthang), nullable=False)
    thoidiem = Column(Integer, nullable=False)
    matrandau = Column(Integer, ForeignKey(TranDau.matrandau), nullable=False)


class QuiDinh(db.Model):
    __tablename__ = "quidinh"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tuoitoithieu = Column(Integer, nullable=False)
    tuoitoida = Column(Integer, nullable=False)
    socauthutoithieu = Column(Integer, nullable=False)
    socauthutoida = Column(Integer, nullable=False)
    socauthunuocngoaitoida = Column(Integer, nullable=False)
    soluongcacloaibanthang = Column(Integer, nullable=False)
    thoidiemghibantoida = Column(Integer, nullable=False)
    diemsothang = Column(Integer, nullable=False)
    diemsothua = Column(Integer, nullable=False)
    diemsohoa = Column(Integer, nullable=False)
    ## 1: bàn thắng
    ## 2: Hiệu số
    ## 3: Điểm
    ## 4: Đối Kháng
    ## lưu: "1234"
    thutuuutien = Column(String(10), nullable=False)


if __name__ == "__main__":
    db.create_all()
