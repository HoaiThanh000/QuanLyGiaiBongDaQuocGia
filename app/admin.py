from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect

from app import admin, db
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
    column_display_pk = False
    can_delete = True
    can_export = True
    list_template = 'admin/list/listdoibong.html'
    create_template = 'admin/create/createdoibong.html'


# Cầu thủ
class CauThuModelView(AuthenticatedView):
    column_display_pk = False
    can_delete = True
    can_export = True
    list_template = 'admin/list/listcauthu.html'
    create_template = 'admin/create/createcauthu.html'


# Loại cầu thủ
class LoaiCauThuModelView(AuthenticatedView):
    column_display_pk = False
    can_delete = True
    can_export = True
    can_edit = False
    fast_mass_delete = False
    column_editable_list = ['tenloaicauthu']
    list_template = 'admin/list/listloaicauthu.html'
    create_template = 'admin/create/createloaicauthu.html'


# Bàn Thắng
class BanThangModelView(AuthenticatedView):
    column_display_pk = False
    can_delete = True
    can_export = True
    list_template = 'admin/list/listbanthang.html'
    create_template = 'admin/create/createbanthang.html'


# Loại Bàn Thắng
class LoaiBanThangModelView(AuthenticatedView):
    can_export = True
    can_edit = False
    fast_mass_delete = False
    column_editable_list = ['tenloaibanthang']
    create_modal = False
    list_template = 'admin/list/listLoaiBanThang.html'
    create_template = 'admin/create/CreateLoaiBanThang.html'


# Trận đấu
class TranDauModelView(AuthenticatedView):
    column_display_pk = False
    can_delete = True
    can_export = True
    can_edit = True
    list_template = 'admin/list/ListTranDau.html'
    create_template = 'admin/create/createtrandau.html'
    # edit_template = 'admin/editquidinh.html'

# Tham gia
class ThamGiaModelView(AuthenticatedView):
    column_display_pk = False
    can_delete = True
    can_export = True
    can_edit = True
    list_template = 'admin/list/listThamGia.html'
    create_template = 'admin/create/createThamGia.html'


# Vòng đấu
class VongDauModelView(AuthenticatedView):
    column_display_pk = False
    can_edit = False
    fast_mass_delete = False
    column_editable_list = ['tenvongdau']
    create_modal = False
    can_delete = True
    can_export = True
    list_template = 'admin/list/ListVongDau.html'
    create_template = 'admin/create/createvongdau.html'


# Qui Định
class QuiDinhModelView(AuthenticatedView):
    can_export = True
    can_edit = True
    list_template = 'admin/list/ListQuiDinh.html'
    create_template = 'admin/create/createquidinh.html'
    # edit_template = 'admin/editquidinh.html'


admin.add_view(DoiBongModelView(DoiBong, db.session, name="Đội Bóng"))
admin.add_view(CauThuModelView(CauThu, db.session, name="Cầu Thủ"))
admin.add_view(LoaiCauThuModelView(LoaiCauThu, db.session, name="Loại Cầu Thủ"))
admin.add_view(BanThangModelView(BanThang, db.session, name="Bàn Thắng"))
admin.add_view(LoaiBanThangModelView(LoaiBanThang, db.session, name="Loại Bàn Thắng"))
admin.add_view(ThamGiaModelView(ThamGia, db.session, name="ThamGia"))
admin.add_view(TranDauModelView(TranDau, db.session, name="Trận Đấu"))
admin.add_view(VongDauModelView(VongDau, db.session, name="Vòng Đấu"))
admin.add_view(QuiDinhModelView(QuiDinh, db.session, name="Qui Định"))
admin.add_view(LogoutView(name="Đăng xuất"))
