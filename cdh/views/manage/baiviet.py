from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from cdh.models import BaiViet, KhoaHoc, User, LoaiUser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
import hashlib


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

    ds_baiviet = BaiViet.objects.all().order_by('ma_bai')[::-1]
    ds_baiviet_user = BaiViet.objects.filter(tac_gia_id = username).order_by('ma_bai')[::-1]

    temp = loader.get_template('baiviet_ds.html')
    query = request.GET.get("q")
    if query:
        ds_baiviet = BaiViet.objects.filter(ten_bai__icontains=query)
        ds_baiviet_user = BaiViet.objects.filter(ten_bai__icontains=query, tac_gia_id = username)
    paginator = Paginator(ds_baiviet, 5)
    paginator_user = Paginator(ds_baiviet_user, 5)
    pageNumber = request.GET.get('page')
    try:
        ds_baiviet = paginator.page(pageNumber)
        ds_baiviet_user = paginator_user.page(pageNumber)
    except PageNotAnInteger:
        ds_baiviet = paginator.page(1)
        ds_baiviet_user = paginator_user.page(1)
    except EmptyPage:
        ds_baiviet = paginator.page(paginator.num_pages)
        ds_baiviet_user = paginator_user.page(paginator_user.num_pages)
    context = {
        "ds_baiviet_user": ds_baiviet_user,
        "ds_baiviet": ds_baiviet,
        "q": query,
        "user":user,
        "loaiuser": loaiuser,
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
    ds_khoahoc = KhoaHoc.objects.filter(tac_gia_id = user.username).order_by('ma_khoa_hoc')[::-1]
    if request.POST.get("btnLuu"):
        bv = BaiViet()
        bv.ten_bai = request.POST['txttenbai']
        bv.noi_dung = request.POST['txtnoidung']
        bv.khoa_hoc_id = request.POST['select_khoahoc']
        bv.tac_gia_id = user.username
        bv.tong_so_view = 0
        bv.tong_so_binh_luan = 0
        bv.trang_thai = "off"
        bv.save()
        return redirect('baiviet_ds')
    if request.POST.get("btnDang"):
        bv = BaiViet()
        bv.ten_bai = request.POST['txttenbai']
        bv.noi_dung = request.POST['txtnoidung']
        bv.khoa_hoc_id = request.POST['select_khoahoc']
        bv.tac_gia_id = user.username
        bv.tong_so_view = 0
        bv.tong_so_binh_luan = 0
        bv.trang_thai = "on"
        bv.save()
        return redirect('baiviet_ds')

    context = {"ds_khoahoc": ds_khoahoc, "user":user}
    template = loader.get_template('baiviet_them.html')
    return HttpResponse(template.render(context, request))

def sua(request, bai_viet_id):
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

    ds_khoahoc = KhoaHoc.objects.all()
    bv = BaiViet.objects.get(pk=bai_viet_id)
    if request.POST.get("btnLuu"):
        bv.ten_bai = request.POST['txttenbai']
        bv.noi_dung = request.POST['txtnoidung']
        bv.khoa_hoc_id = request.POST['select_khoahoc']
        bv.trang_thai = "off"
        bv.save()
        return redirect('baiviet_ds')
    if request.POST.get("btnDang"):
        bv.ten_bai = request.POST['txttenbai']
        bv.noi_dung = request.POST['txtnoidung']
        bv.khoa_hoc_id = request.POST['select_khoahoc']
        bv.trang_thai = "on"
        bv.save()
        return redirect('baiviet_ds')


    context = {"baiviet": bv, "ds_khoahoc": ds_khoahoc, "user":user}
    template = loader.get_template('baiviet_sua.html')
    return HttpResponse(template.render(context, request))

def xoa(request, bai_viet_id):
    BaiViet.objects.get(pk=bai_viet_id).delete()
    return redirect('baiviet_ds')