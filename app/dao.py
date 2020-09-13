from app import app, db
from app.models import CauThu, DoiBong, ThamGia, TranDau, VongDau, QuiDinh, BanThang
from sqlalchemy import and_, or_, desc, asc
import json
import os
import hashlib


def read_cauthu(keyword=None, date_start=None, date_end=None):
    ct = CauThu.query

    if keyword:
        ct = ct.filter(CauThu.tencauthu.contains(keyword))

    if date_start and date_end:
        ct = ct.filter(CauThu.ngaysinh.__gt__(date_start), CauThu.ngaysinh.__lt__(date_end))

    return ct.all()

def read_doibong():
    dbg = DoiBong.query

    return dbg.all()

def read_vongdau():
    vd = VongDau.query

    return vd.all()

def read_ketqua():
    tgs = ThamGia.query.all()

    return tgs

def read_banthang():
    bts = BanThang.query.all()

    return bts

def read_vongdau_dstrandau():
    tds = TranDau.query.all()

    return tds

def read_thamgia():
    tgs = ThamGia.query.order_by(and_(ThamGia.matrandau.asc())).all()

    return tgs

def read_quidinh():
    qds = QuiDinh.query.all()

    return qds


if __name__ == "__main__":
    print(read_cauthu())