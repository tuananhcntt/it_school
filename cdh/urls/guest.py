from django.conf.urls import url

from cdh.views.guest import trangchu, danhmuc, khoahoc, baiviet, index, lienhe

urlpatterns = [
    url(r'^$', index.index),
    url(r'^lienhe', lienhe.index, name='lienhe'),
    url(r'^trangchu', trangchu.index, name='trangchu'),
    url(r'^danhmuc/(?P<chuyen_nganh_id>[0-9]+)/', danhmuc.index),
    url(r'^khoahoc/(?P<khoa_hoc_id>[0-9]+)/', khoahoc.index),
    url(r'^baiviet/(?P<bai_viet_id>[0-9]+)/', baiviet.index),
    url(r'^login', index.index),
]