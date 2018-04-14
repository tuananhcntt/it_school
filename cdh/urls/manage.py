from django.conf.urls import url
from cdh.views.manage import index, danhmuc, khoahoc, baiviet, tuongtac, binhluan, loaiuser, nguoidung, hopthu

urlpatterns = [
    url(r'^index/$', index.index, name='index'),
    url(r'^hopthu', hopthu.index, name='hopthu'),

    url(r'^danhmuc_ds/', danhmuc.danhsach, name='danhmuc_ds'),
    url(r'^danhmuc_them/', danhmuc.them, name='danhmuc_them'),
    url(r'^danhmuc_sua/(?P<danh_muc_id>[0-9]+)', danhmuc.sua, name='danhmuc_sua'),
    url(r'^danhmuc_xoa/(?P<danh_muc_id>[0-9]+)', danhmuc.xoa, name='danhmuc_xoa'),

    url(r'^khoahoc_ds/', khoahoc.danhsach, name='khoahoc_ds'),
    url(r'^khoahoc_them/', khoahoc.them, name='khoahoc_them'),
    url(r'^khoahoc_sua/(?P<khoa_hoc_id>[0-9]+)', khoahoc.sua, name='khoahoc_sua'),
    url(r'^khoahoc_xoa/(?P<khoa_hoc_id>[0-9]+)', khoahoc.xoa, name='khoahoc_xoa'),

    url(r'^baiviet_ds/', baiviet.danhsach, name='baiviet_ds'),
    url(r'^baiviet_them/', baiviet.them, name='baiviet_them'),
    url(r'^baiviet_sua/(?P<bai_viet_id>[0-9]+)', baiviet.sua, name='baiviet_sua'),
    url(r'^baiviet_xoa/(?P<bai_viet_id>[0-9]+)', baiviet.xoa, name='baiviet_xoa'),

    url(r'^nguoidung_ds/', nguoidung.danhsach, name='nguoidung_ds'),
    url(r'^nguoidung_them/', nguoidung.them, name='nguoidung_them'),
    url(r'^nguoidung_sua/(?P<nguoi_dung_id>[0-9]+)', nguoidung.sua, name='nguoidung_sua'),
    url(r'^nguoidung_xoa/(?P<nguoi_dung_id>[0-9]+)', nguoidung.xoa, name='nguoidung_xoa'),
]