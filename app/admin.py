from datetime import date

from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect, request, url_for

from app import admin, db, dao, client
from app.models import DoiBong, CauThu, LoaiCauThu, BanThang, LoaiBanThang, \
    TranDau, VongDau, QuiDinh, ThamGia


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect("/admin")


# Đội bóng
class DoiBongModelView(AuthenticatedView):
    can_delete = True
    form_columns = ['tendoi', 'sannha', 'sodt', ]
    list_template = 'admin/list/list-doi-bong.html'
    create_template = 'admin/create/create-doi-bong.html'
    edit_template = 'admin/edit/edit-doi-bong.html'


# Cầu thủ
class CauThuModelView(AuthenticatedView):
    can_delete = True
    column_searchable_list = ('tencauthu', 'ngaysinh')
    list_template = 'admin/list/list-cau-thu.html'
    create_template = 'admin/create/create-cau-thu.html'
    edit_template = 'admin/edit/edit-cau-thu.html'
    form_excluded_columns = ('ds_banthang', 'macauthu')


# Loại cầu thủ
class LoaiCauThuModelView(AuthenticatedView):
    can_delete = True
    can_edit = True
    form_columns = ['tenloaicauthu', ]
    list_template = 'admin/list/list-loai-cau-thu.html'
    create_template = 'admin/create/create-loai-cau-thu.html'
    edit_template = 'admin/edit/edit-loai-cau-thu.html'


# Bàn Thắng
class BanThangModelView(AuthenticatedView):
    can_delete = True
    can_edit = True
    list_template = 'admin/list/list-ban-thang.html'
    create_template = 'admin/create/create-ban-thang.html'
    edit_template = 'admin/edit/edit-ban-thang.html'


# Loại Bàn Thắng
class LoaiBanThangModelView(AuthenticatedView):
    can_edit = True
    form_excluded_columns = ('ds_banthang')
    list_template = 'admin/list/list-loai-ban-thang.html'
    create_template = 'admin/create/create-loai-ban-thang.html'
    edit_template = 'admin/edit/edit-loai-ban-thang.html'


# Trận đấu
class TranDauModelView(AuthenticatedView):
    can_delete = True
    can_edit = True
    form_excluded_columns = ('ds_banthang', 'ds_thamgia')
    list_template = 'admin/list/list-tran-dau.html'
    create_template = 'admin/create/create-tran-dau.html'
    edit_template = 'admin/edit/edit-tran-dau.html'


# Tham gia
class ThamGiaModelView(AuthenticatedView):
    can_delete = True
    can_edit = True
    list_template = 'admin/list/list-lich-thi-dau.html'
    create_template = 'admin/create/create-tham-gia.html'
    edit_template = 'admin/edit/edit-tham-gia.html'


# Vòng đấu
class VongDauModelView(AuthenticatedView):
    can_edit = True
    can_delete = True
    form_excluded_columns = ('ds_trandau')
    list_template = 'admin/list/list-vong-dau.html'
    create_template = 'admin/create/create-vong-dau.html'
    edit_template = 'admin/edit/edit-vong-dau.html'


# Qui Định
class QuiDinhModelView(AuthenticatedView):
    can_export = True
    can_edit = True
    list_template = 'admin/list/list-qui-dinh.html'
    create_template = 'admin/create/create-qui-dinh.html'
    edit_template = 'admin/edit/edit-qui-dinh.html'


class BangXepHangView(BaseView):
    @expose('/')
    def index(self):
        ngay = date.today().strftime("%d-%m-%Y")
        return self.render('admin/bang-xep-hang.html', ngay=ngay,
                           ds_bxh=dao.them_ds_bxh())


class DanhSachCauThuGhiBanView(BaseView):
    @expose('/')
    def index(self):
        ngay = date.today().strftime("%d-%m-%Y")
        return self.render('admin/danh-sach-cau-thu-ghi-ban.html', ngay=ngay,
                           ds_ct_gb=dao.them_ds_ct_gb(),
                           ds_doibong=dao.read_doibong(),
                           ds_loaicauthu=dao.read_loaicauthu())


class GhiNhanKetQuaTranDauView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/ghi-nhan-ket-qua-tran-dau.html')


class QuiDinh1View(BaseView):
    @expose('/', methods=['post', 'get'])
    def index(self):
        msg = None
        msg_c = 0
        if request.method.lower() == 'post':
            tuoitoithieu = int(request.form.get("tuoitoithieu", 0))
            tuoitoida = int(request.form.get("tuoitoida", 0))
            socauthutoithieu = int(request.form.get("socauthutoithieu", 0))
            socauthutoida = int(request.form.get("socauthutoida", 0))
            socauthunuocngoai = int(request.form.get("socauthunuocngoai", 0))
            if tuoitoithieu < 6:
                msg = 'Tuổi tối thiểu không hợp lệ!'
            else:
                if tuoitoida <= tuoitoithieu:
                    msg = 'Tuổi tối đa không thể lớn hơn tuổi tối thiểu!'
                else:
                    if socauthutoithieu < 0:
                        msg = 'Số cầu thủ tối thiểu không hợp lệ!'
                    else:
                        if socauthutoida <= socauthutoithieu:
                            msg = 'Số cầu thủ tối đa phải lớn hơn số cầu thủ tối thiểu!'
                        else:
                            if socauthunuocngoai < 0:
                                msg = 'Số cầu thủ nước ngoài không hợp lệ!'
                            else:
                                if dao.update_quidinh1(tuoitoithieu, tuoitoida, socauthutoithieu, socauthutoida,
                                                       socauthunuocngoai) == 0:
                                    msg = 'Cập nhật qui định thành công!'
                                    msg_c = 1
        return self.render('admin/qui-dinh-1.html', quidinh1=dao.read_quidinh1(), msg=msg, msg_c=msg_c)


class QuiDinh3View(BaseView):
    @expose('/', methods=['post', 'get'])
    def index(self):
        msg = None
        msg_c = 0
        if request.method.lower() == 'post':
            soluongcacloaibanthang = int(request.form.get("soluongcacloaibanthang", 0))
            thoidiemghibantoida = int(request.form.get("thoidiemghibantoida", 0))
            if soluongcacloaibanthang <= 0:
                msg = 'Số lượng các loại bàn thắng không hợp lệ!'
            else:
                if thoidiemghibantoida <= 0:
                    msg = 'Thời điểm ghi bàn tối đa không hợp lệ!'
                else:
                    if dao.update_quidinh3(soluongcacloaibanthang, thoidiemghibantoida) == 0:
                        msg = 'Cập nhật qui định thành công!'
                        msg_c = 1
        return self.render('admin/qui-dinh-3.html', quidinh3=dao.read_quidinh3(), msg=msg, msg_c=msg_c)


class QuiDinh5View(BaseView):
    @expose('/', methods=['post', 'get'])
    def index(self):
        msg = None
        msg_c = 0
        if request.method.lower() == 'post':
            diemsothang = int(request.form.get("diemsothang", 0))
            diemsohoa = int(request.form.get("diemsohoa", 0))
            diemsothua = int(request.form.get("diemsothua", 0))
            thutuuutien = request.form.get("thutuuutien").strip()
            if diemsothang <= 0:
                msg = 'Điểm số bàn thắng không hợp lệ!'
            else:
                if diemsohoa < 0:
                    msg = 'Điểm số bàn hòa không hợp lệ!'
                else:
                    if diemsothua < 0:
                        msg = 'Điểm số bàn thua không hợp lệ!'
                    else:
                        if diemsothang < diemsohoa:
                            msg = 'Điểm số bàn thắng phải lớn hơn điểm số hòa!'
                        else:
                            if diemsohoa < diemsothua:
                                msg = 'Điểm số hòa phải lớn hơn điểm số bàn thua!'
                            else:
                                if thutuuutien == '':
                                    msg = 'Thứ tự ưu tiên không hợp lệ'
                                else:
                                    if dao.update_quidinh5(diemsothang, diemsohoa, diemsothua, thutuuutien) == 0:
                                        msg = 'Cập nhật qui định thành công!'
                                        msg_c = 1
        return self.render('admin/qui-dinh-5.html', quidinh5=dao.read_quidinh5(), msg=msg, msg_c=msg_c)


class ThemLoaiBanThangView(BaseView):
    @expose('/', methods=['post', 'get'])
    def index(self):
        msg = None
        msg_c = 0
        if request.method.lower() == 'post':
            tenloaibanthang = request.form.get("tenloaibanthang")
            if dao.add_loaibanthang(tenloaibanthang=tenloaibanthang):
                msg = "Lưu dữ liệu thành công!"
                msg_c = 1
            else:
                msg = "Số loại bàn thắng đã đầy không thể thêm!"
        return self.render('admin/create/create-loai-ban-thang.html', msg=msg, msg_c=msg_c)


class ThemCauThuView(BaseView):
    @expose('/', methods=['post', 'get'])
    def index(self):
        msg = None
        msg_c = 0
        if request.method.lower() == 'post':
            tencauthu = request.form.get("tencauthu")
            ngaysinh = request.form.get("ngaysinh")
            ghichu = request.form.get("ghichu")
            doibong = int(request.form.get("doibong"))
            loaicauthu = int(request.form.get("loaicauthu"))
            msg = dao.add_cauthu(tencauthu=tencauthu, ngaysinh=ngaysinh, ghichu=ghichu
                                 , madoibong=doibong, maloaicauthu=loaicauthu)
            if msg is None:
                msg = "Thêm dữ liệu cầu thủ thành công!"
                msg_c = 1
        return self.render('admin/create/create-cau-thu.html', ds_loaicauthu=dao.read_loaicauthu(),
                           ds_doibong=dao.read_doibong(), msg=msg, msg_c=msg_c)


class ThemBanThangView(BaseView):
    @expose('/', methods=['get', 'post'])
    def index(self):
        msg = None
        msg_c = 0
        if request.method.lower() == 'post':
            thoidiem = request.form.get("thoidiem")
            cauthu = request.form.get("cauthu")
            trandau = request.form.get("trandau")
            loaibanthang = request.form.get("loaibanthang")
            if dao.add_banthang(thoidiem=thoidiem, macauthu=cauthu, matrandau=trandau
                    , maloaibanthang=loaibanthang):
                msg = "Thêm dữ liệu bàn thắng thành công!"
                msg_c = 1
            else:
                msg = "Thời điểm ghi bàn không đúng!"
        return self.render('admin/create/create-ban-thang.html', ds_cauthu=dao.read_cauthu(),
                           ds_loaibanthang=dao.read_loaibanthang(), ds_trandau=dao.read_trandau()
                           , msg=msg, msg_c=msg_c)


class ThemLichThiDauView(BaseView):
    @expose('/', methods=['post', 'get'])
    def index(self):
        msg = None
        msg_c = 0
        if request.method.lower() == 'post':
            ngaythidau = request.form.get("ngaythidau")
            giothidau = request.form.get("giothidau")
            santhidau = request.form.get("santhidau")
            doinha = request.form.get("doinha")
            doikhach = request.form.get("doikhach")
            trandau = request.form.get("trandau")
            tendoinha = dao.read_tendoibong(int(doinha))
            tendoikhach = dao.read_tendoibong(int(doikhach))
            sodtdn = "+84" + dao.read_sdt_db(int(doinha))[1:]
            sodtdk = "+84" + dao.read_sdt_db(int(doikhach))[1:]
            noidungtinnhan = "From: Quản lý giải vô địch bóng đá quốc gia - lịch thi đấu - %s với %s - ngày thi đấu: %s - giờ thi đấu: %s - sân thi đấu: %s" % (tendoinha, tendoikhach, ngaythidau, giothidau, santhidau)
            msg = dao.add_thamgia(ngaythidau=ngaythidau, giothidau=giothidau, santhidau=santhidau,
                                  doinha=doinha, doikhach=doikhach, trandau=trandau)
            if msg is None:
                msg = "Thêm dữ liệu thành công!"
                msg_c = 1
                sms_dn = client.messages.create(
                    from_="+14029994903",
                    body=noidungtinnhan,
                    to=sodtdn
                )
                sms_dk = client.messages.create(
                    from_="+14029994903",
                    body=noidungtinnhan,
                    to=sodtdk
                )
                print(sms_dn.sid)
                print(sms_dk.sid)
        return self.render('admin/create/create-tham-gia.html', ds_doibong=dao.read_doibong()
                           , ds_trandau=dao.read_trandau(), msg=msg, msg_c=msg_c)


admin.add_view(DoiBongModelView(DoiBong, db.session, name="Đội Bóng"))
admin.add_view(CauThuModelView(CauThu, db.session, name="Cầu Thủ"))
admin.add_view(LoaiCauThuModelView(LoaiCauThu, db.session, name="Loại Cầu Thủ"))
admin.add_view(BanThangModelView(BanThang, db.session, name="Bàn Thắng"))
admin.add_view(LoaiBanThangModelView(LoaiBanThang, db.session, name="Loại Bàn Thắng"))
admin.add_view(ThamGiaModelView(ThamGia, db.session, name="Lịch Thi Đấu"))
admin.add_view(TranDauModelView(TranDau, db.session, name="Trận Đấu"))
admin.add_view(VongDauModelView(VongDau, db.session, name="Vòng Đấu"))
admin.add_view(QuiDinhModelView(QuiDinh, db.session, name="Qui Định"))
admin.add_view(BangXepHangView(name="Bảng xếp hạng"))
admin.add_view(DanhSachCauThuGhiBanView(name="Danh sách cầu thủ ghi bàn"))
admin.add_view(GhiNhanKetQuaTranDauView(name="Ghi nhận kết quả trận đấu"))
admin.add_view(QuiDinh1View(name="Qui định 1"))
admin.add_view(QuiDinh3View(name="Qui định 3"))
admin.add_view(QuiDinh5View(name="Qui định 5"))
admin.add_view(ThemLoaiBanThangView(name="Thêm loại bàn thắng"))
admin.add_view(ThemCauThuView(name="Thêm cầu thủ"))
admin.add_view(ThemBanThangView(name="Thêm bàn thắng"))
admin.add_view(ThemLichThiDauView(name="Thêm lịch thi đấu"))
admin.add_view(LogoutView(name="Đăng xuất"))
