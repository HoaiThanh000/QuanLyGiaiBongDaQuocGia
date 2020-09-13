import json
from datetime import date, time

from app import db
from app.models import CauThu, DoiBong, LoaiCauThu, BanThang, ThamGia, QuiDinh, LoaiBanThang, TranDau


def read_cauthu():
    ds_cauthu = CauThu.query

    return ds_cauthu.all()


def read_doibong():
    ds_doibong = DoiBong.query

    return ds_doibong.all()


def read_loaicauthu():
    ds_loaicauthu = LoaiCauThu.query

    return ds_loaicauthu.all()


def read_loaibanthang():
    return LoaiBanThang.query.all()


def read_trandau():
    return TranDau.query.all()


def read_sobanthang(macauthu):
    ds_banthang = BanThang.query.filter_by(macauthu=macauthu).all()
    sobanthang = len(ds_banthang)

    return sobanthang


def read_soluongtranthang(madoibong):
    sotranthang = 0
    ds_vaitrochunha = ThamGia.query.filter_by(doichunha=madoibong).all()
    # vtcn : vai trò chủ nhà
    for vtcn in ds_vaitrochunha:
        if vtcn.tyso and int(vtcn.tyso[0]) > int(vtcn.tyso[2]):
            sotranthang = sotranthang + 1
    ds_vaitrokhach = ThamGia.query.filter_by(doikhach=madoibong).all()
    # vtk : vai trò khách
    for vtk in ds_vaitrokhach:
        if vtk.tyso and int(vtk.tyso[0]) > int(vtk.tyso[2]):
            sotranthang = sotranthang + 1
    return sotranthang


def read_soluongtranthua(madoibong):
    sotranthua = 0
    ds_vaitrochunha = ThamGia.query.filter_by(doichunha=madoibong).all()
    # vtcn : vai trò chủ nhà
    for vtcn in ds_vaitrochunha:
        if vtcn.tyso and int(vtcn.tyso[0]) < int(vtcn.tyso[2]):
            sotranthua = sotranthua + 1
    ds_vaitrokhach = ThamGia.query.filter_by(doikhach=madoibong).all()
    # vtk : vai trò khách
    for vtk in ds_vaitrokhach:
        if vtk.tyso and int(vtk.tyso[0]) < int(vtk.tyso[2]):
            sotranthua = sotranthua + 1
    return sotranthua


def read_soluongtranhoa(madoibong):
    sotranhoa = 0
    ds_vaitrochunha = ThamGia.query.filter_by(doichunha=madoibong).all()
    # vtcn : vai trò chủ nhà
    for vtcn in ds_vaitrochunha:
        if vtcn.tyso and int(vtcn.tyso[0]) == int(vtcn.tyso[2]):
            sotranhoa = sotranhoa + 1
    ds_vaitrokhach = ThamGia.query.filter_by(doikhach=madoibong).all()
    # vtk : vai trò khách
    for vtk in ds_vaitrokhach:
        if vtk.tyso and int(vtk.tyso[0]) == int(vtk.tyso[2]):
            sotranhoa = sotranhoa + 1
    return sotranhoa


def them_ds_ct_gb():
    ds_ct_gb = []
    ds_cauthu = read_cauthu()
    for cauthu in ds_cauthu:
        ds_ct_gb.append({
            "stt": len(ds_ct_gb) + 1,
            "tencauthu": cauthu.tencauthu,
            "doi": cauthu.madoi,
            "loaicauthu": cauthu.maloaicauthu,
            "sobanthang": read_sobanthang(cauthu.macauthu)
        })
    return ds_ct_gb


def them_ds_bxh():
    ds_bxh = []
    ds_doibong = read_doibong()
    for doibong in ds_doibong:
        thang = read_soluongtranthang(doibong.madoi)
        thua = read_soluongtranthua(doibong.madoi)
        ds_bxh.append({
            "stt": len(ds_bxh) + 1,
            "doibong": doibong.tendoi,
            "thang": read_soluongtranthang(doibong.madoi),
            "hoa": read_soluongtranhoa(doibong.madoi),
            "thua": read_soluongtranthua(doibong.madoi),
            "hieuso": thang - thua,
            "hang": 0
        })
    return ds_bxh


def read_quidinh1():
    ds_quidinh = QuiDinh.query.all()
    quidinh1 = {
        "tuoitoithieu": ds_quidinh[0].tuoitoithieu,
        "tuoitoida": ds_quidinh[0].tuoitoida,
        "socauthutoithieu": ds_quidinh[0].socauthutoithieu,
        "socauthutoida": ds_quidinh[0].socauthutoida,
        "socauthunuocngoaitoida": ds_quidinh[0].socauthunuocngoaitoida,
    }
    return quidinh1


def read_quidinh3():
    ds_quidinh = QuiDinh.query.all()
    quidinh3 = {
        "soluongcacloaibanthang": ds_quidinh[0].soluongcacloaibanthang,
        "thoidiemghibantoida": ds_quidinh[0].thoidiemghibantoida
    }
    return quidinh3


def read_quidinh5():
    ds_quidinh = QuiDinh.query.all()
    quidinh5 = {
        "diemsothang": ds_quidinh[0].diemsothang,
        "diemsohoa": ds_quidinh[0].diemsohoa,
        "diemsothua": ds_quidinh[0].diemsothua,
        "thutuuutien": ds_quidinh[0].thutuuutien
    }
    return quidinh5


def update_quidinh1(tuoitoithieu, tuoitoida, socauthutoithieu, socauthutoida, socauthunuocngoai):
    r = QuiDinh.query.get(1)
    r.tuoitoithieu = tuoitoithieu
    r.tuoitoida = tuoitoida
    r.socauthutoithieu = socauthutoithieu
    r.socauthutoida = socauthutoida
    r.socauthunuocngoaitoida = socauthunuocngoai
    db.session.add(r)
    db.session.commit()
    return 0


def update_quidinh3(soluongcacloaibanthang, thoidiemghibantoida):
    r = QuiDinh.query.get(1)
    r.soluongcacloaibanthang = soluongcacloaibanthang
    r.thoidiemghibantoida = thoidiemghibantoida
    db.session.add(r)
    db.session.commit()
    return 0


def update_quidinh5(diemsothang, diemsohoa, diemsothua, thutuuutien):
    r = QuiDinh.query.get(1)
    r.diemsothang = diemsothang
    r.diemsohoa = diemsohoa
    r.diemsothua = diemsothua
    r.thutuuutien = thutuuutien
    db.session.add(r)
    db.session.commit()
    return 0


def check_loaibanthang():
    QuiDinh.soluongcacloaibanthang
    ds_loaibanthang = LoaiBanThang.query.all()
    ds_quidinh = QuiDinh.query.all()
    sodongdaco = len(ds_loaibanthang)
    if sodongdaco < ds_quidinh[0].soluongcacloaibanthang:
        return True
    return False


def add_loaibanthang(tenloaibanthang):
    if check_loaibanthang():
        p = LoaiBanThang(tenloaibanthang=tenloaibanthang)
        db.session.add(p)
        db.session.commit()
        return True
    return False


def check_cauthu(ngaysinh, madoibong, maloaicauthu):
    msg = None
    ns = int(ngaysinh[:4])
    ds_quidinh = QuiDinh.query.all()
    ds_cauthu = CauThu.query.join(DoiBong, DoiBong.madoi == CauThu.madoi).filter_by(madoi=madoibong).all()
    if ds_quidinh[0].tuoitoithieu <= date.today().year - ns <= ds_quidinh[0].tuoitoida:
        if len(ds_cauthu) < ds_quidinh[0].socauthutoida:
            if maloaicauthu == 2:
                ds_cauthu = CauThu.query \
                    .filter_by(madoi=madoibong, maloaicauthu=2).all()
                if len(ds_cauthu) >= ds_quidinh[0].socauthunuocngoaitoida:
                    msg = "Số lượng cầu thủ nước ngoài trong đội đã vượt qui định!"
        else:
            msg = "Số lượng cầu thủ trong đội đã vượt qui định"
    else:
        msg = "Tuổi của cầu thủ không đủ để tham gia!"
    return msg


def add_cauthu(tencauthu, ngaysinh, ghichu, madoibong, maloaicauthu):
    msg = check_cauthu(ngaysinh=ngaysinh, madoibong=madoibong, maloaicauthu=maloaicauthu)
    if msg is None:
        p = CauThu(tencauthu=tencauthu, ngaysinh=ngaysinh, ghichu=ghichu, madoi=madoibong,
                   maloaicauthu=maloaicauthu)
        db.session.add(p)
        db.session.commit()
    return msg


def check_banthang(thoidiem):
    td = int(thoidiem)
    ds_quidinh = QuiDinh.query.all()
    if td < ds_quidinh[0].thoidiemghibantoida:
        return True
    return False


def add_banthang(thoidiem, macauthu, matrandau, maloaibanthang):
    td = int(thoidiem)
    if check_banthang(thoidiem=td):
        p = BanThang(thoidiem=thoidiem, matrandau=matrandau, maloaibanthang=maloaibanthang
                     , macauthu=macauthu)
        db.session.add(p)
        db.session.commit()
        return True
    return False


def check_lichthidau(ngaythidau, doinha, doikhach):
    msg = None
    ngay = int(ngaythidau[8:])
    thang = int(ngaythidau[5:7])
    nam = int(ngaythidau[:4])
    ntd = date(nam, thang, ngay)
    if ntd <= date.today():
        msg = "Ngày thi đấu không hợp lệ!"
    else:
        if doinha == doikhach:
            msg = "Đội nhà và đội khách phải khác nhau!"
    return msg


def add_thamgia(ngaythidau, giothidau, santhidau, doinha, doikhach, trandau):
    msg = check_lichthidau(ngaythidau=ngaythidau, doinha=doinha, doikhach=doikhach)
    if msg is None:
        p = ThamGia(ngaythidau=ngaythidau, giothidau=giothidau, santhidau=santhidau,
                    doichunha=doinha, doikhach=doikhach, matrandau=trandau, tyso='')
        db.session.add(p)
        db.session.commit()
    return msg


def read_tendoibong(madoi):
    ds_doibong = DoiBong.query.filter_by(madoi=madoi).all()
    return ds_doibong[0].tendoi


def read_sdt_db(madoi):
    ds_doibong = DoiBong.query.filter_by(madoi=madoi).all()
    return ds_doibong[0].sodt
