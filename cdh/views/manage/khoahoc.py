from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from cdh.models import KhoaHoc, ChuyenNganh,User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cdh.forms import KhoaHoc_form

from django.shortcuts import render


def danhsach(request):
    ds_khoahoc = KhoaHoc.objects.all().order_by('ma_khoa_hoc')[::-1]
    temp = loader.get_template('khoahoc_ds.html')
    query = request.GET.get("q")
    if query:
        ds_khoahoc = KhoaHoc.objects.filter(ten_khoa_hoc__icontains = query,
                                            # chuyen_nganh__ten_chuyen_nganh__icontains = query,
                                            # tac_gia__ho_ten__icontains = query
                                            )

    paginator = Paginator(ds_khoahoc, 5)
    pageNumber = request.GET.get('page')
    try:
        ds_khoahoc = paginator.page(pageNumber)
    except PageNotAnInteger:
        ds_khoahoc = paginator.page(1)
    except EmptyPage:
        ds_khoahoc = paginator.page(paginator.num_pages)
    user = ""
    if request.session.has_key('username'):
        username = request.session['username']
        user = User.objects.get(username=username)
    if request.GET.get("btnlogin"):
        username = request.GET.get('username')
        matkhau = request.GET.get('password')
        try:
            user = User.objects.get(username=username, mat_khau=matkhau)
            request.session['username'] = user.username
        except:
            user = ""

    if request.GET.get("btnlogout"):
        del request.session['username']
        user = ""
    context = {
        "ds_khoahoc": ds_khoahoc,
        "q": query,
        "dem": 0,
        "user":user
    }
    return HttpResponse(temp.render(context))

def them(request):
    ds_chuyennganh = ChuyenNganh.objects.all().order_by('ma_chuyen_nganh')
    if request.method == "POST":
        kh = KhoaHoc()
        kh.ten_khoa_hoc = request.POST['txttieude']
        # kh.gioi_thieu = "Đang cập nhật"
        kh.gioi_thieu = request.POST['txtgioithieu']

        kh.img = request.FILES['txtfile']
        # upload(kh.img)

        kh.le_phi = request.POST['txtlephi']
        kh.tac_gia_id = "anhtuan"
        kh.chuyen_nganh_id = request.POST['select_danhmuc']
        kh.save()
        return redirect('khoahoc_ds')
    user = ""
    if request.session.has_key('username'):
        username = request.session['username']
        user = User.objects.get(username=username)
    if request.GET.get("btnlogin"):
        username = request.GET.get('username')
        matkhau = request.GET.get('password')
        try:
            user = User.objects.get(username=username, mat_khau=matkhau)
            request.session['username'] = user.username
        except:
            user = ""

    if request.GET.get("btnlogout"):
        del request.session['username']
        user = ""
    context = {"ds_chuyennganh": ds_chuyennganh, "user":user}
    template = loader.get_template('khoahoc_them.html')
    return HttpResponse(template.render(context, request))

def sua(request, khoa_hoc_id):
    khoahoc = KhoaHoc.objects.get(pk=khoa_hoc_id)
    danhmuc = ChuyenNganh.objects.get(pk=khoahoc.chuyen_nganh_id)
    ds_chuyennganh = ChuyenNganh.objects.all()
    if request.method == "POST":

        khoahoc.ten_khoa_hoc = request.POST['txttieude']
        # kh.gioi_thieu = "Đang cập nhật"
        khoahoc.gioi_thieu = request.POST['txtgioithieu']

        khoahoc.img = request.FILES['txtfile']
        # upload(khoahoc.img)

        khoahoc.le_phi = request.POST['txtlephi']
        khoahoc.tac_gia_id = "anhtuan"
        khoahoc.chuyen_nganh_id = request.POST['select_danhmuc']
        khoahoc.save()
        return redirect('khoahoc_ds')
    context = {"khoahoc": khoahoc, "danhmuc": danhmuc, "ds_chuyennganh": ds_chuyennganh}
    template = loader.get_template('khoahoc_sua.html')
    return HttpResponse(template.render(context, request))

def xoa(request, khoa_hoc_id):
    KhoaHoc.objects.get(pk=khoa_hoc_id).delete()
    return redirect('khoahoc_ds')

def upload(f):
    file = open(f.name, 'wb+')
    for chunk in f.chunks():
        file.write(chunk)