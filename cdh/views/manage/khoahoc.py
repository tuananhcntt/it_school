from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from cdh.models import KhoaHoc, ChuyenNganh,User, LoaiUser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cdh.forms import KhoaHoc_form

from django.shortcuts import render


def danhsach(request):
    user = ""
    loaiuser = ""
    if request.session.has_key('username'):
        username = request.session['username']
        user = User.objects.get(username=username)
        loaiuser = LoaiUser.objects.get(pk=user.loai_user_id)
        if request.GET.get("btnlogout"):
            del request.session['username']
            user = loaiuser = ""
            return redirect('trangchu')
    else:
        return redirect('index')

    ds_khoahoc_user = KhoaHoc.objects.filter(tac_gia_id = username).order_by('ma_khoa_hoc')[::-1]
    ds_khoahoc = KhoaHoc.objects.all().order_by('ma_khoa_hoc')[::-1]
    temp = loader.get_template('khoahoc_ds.html')
    query = request.GET.get("q")
    if query:
        ds_khoahoc = KhoaHoc.objects.filter(ten_khoa_hoc__icontains = query,
                                            # chuyen_nganh__ten_chuyen_nganh__icontains = query,
                                            # tac_gia__ho_ten__icontains = query
                                            )
        ds_khoahoc_user = KhoaHoc.objects.filter(ten_khoa_hoc__icontains = query, tac_gia_id = username)


    paginator = Paginator(ds_khoahoc, 5)
    paginator_user = Paginator(ds_khoahoc_user, 5)
    pageNumber = request.GET.get('page')
    try:
        ds_khoahoc = paginator.page(pageNumber)
        ds_khoahoc_user = paginator_user.page(pageNumber)
    except PageNotAnInteger:
        ds_khoahoc = paginator.page(1)
        ds_khoahoc_user = paginator_user.page(1)
    except EmptyPage:
        ds_khoahoc = paginator.page(paginator.num_pages)
        ds_khoahoc_user = paginator_user.page(paginator_user.num_pages)

    context = {
        "ds_khoahoc_user": ds_khoahoc_user,
        "ds_khoahoc": ds_khoahoc,
        "q": query,
        "dem": 0,
        "user":user
    }
    return HttpResponse(temp.render(context))

def them(request):
    user = ""
    loaiuser = ""
    if request.session.has_key('username'):
        username = request.session['username']
        user = User.objects.get(username=username)
        loaiuser = LoaiUser.objects.get(pk=user.loai_user_id)
        if request.GET.get("btnlogout"):
            del request.session['username']
            user = loaiuser = ""
            return redirect('trangchu')
    else:
        return redirect('index')

    ds_chuyennganh = ChuyenNganh.objects.all().order_by('ma_chuyen_nganh')
    if request.method == "POST":
        kh = KhoaHoc()
        kh.ten_khoa_hoc = request.POST['txttieude']
        # kh.gioi_thieu = "Đang cập nhật"
        kh.gioi_thieu = request.POST['txtgioithieu']

        kh.img = request.FILES['txtfile']
        # upload(kh.img)

        kh.le_phi = request.POST['txtlephi']
        kh.tac_gia_id = username
        kh.chuyen_nganh_id = request.POST['select_danhmuc']
        kh.save()
        return redirect('khoahoc_ds')

    context = {"ds_chuyennganh": ds_chuyennganh, "user":user}
    template = loader.get_template('khoahoc_them.html')
    return HttpResponse(template.render(context, request))

def sua(request, khoa_hoc_id):
    user = ""
    loaiuser = ""
    if request.session.has_key('username'):
        username = request.session['username']
        user = User.objects.get(username=username)
        loaiuser = LoaiUser.objects.get(pk=user.loai_user_id)
        if request.GET.get("btnlogout"):
            del request.session['username']
            user = loaiuser = ""
            return redirect('trangchu')
    else:
        return redirect('index')

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
    context = {"khoahoc": khoahoc, "danhmuc": danhmuc, "ds_chuyennganh": ds_chuyennganh,"user":user}
    template = loader.get_template('khoahoc_sua.html')
    return HttpResponse(template.render(context, request))

def xoa(request, khoa_hoc_id):
    KhoaHoc.objects.get(pk=khoa_hoc_id).delete()
    return redirect('khoahoc_ds')

# def upload(f):
#     file = open(f.name, 'wb+')
#     for chunk in f.chunks():
#         file.write(chunk)