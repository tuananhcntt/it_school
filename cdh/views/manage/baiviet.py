from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from cdh.models import BaiViet, KhoaHoc, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


def danhsach(request):
    ds_baiviet = BaiViet.objects.all().order_by('ma_bai')[::-1]
    temp = loader.get_template('baiviet_ds.html')
    query = request.GET.get("q")
    if query:
        ds_baiviet = BaiViet.objects.filter(ten_bai__icontains = query)
    paginator = Paginator(ds_baiviet, 5)
    pageNumber = request.GET.get('page')
    try:
        ds_baiviet = paginator.page(pageNumber)
    except PageNotAnInteger:
        ds_baiviet = paginator.page(1)
    except EmptyPage:
        ds_baiviet = paginator.page(paginator.num_pages)

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
        "ds_baiviet": ds_baiviet,
        "q": query,
        "user":user,
    }
    return HttpResponse(temp.render(context))

def them(request):
    ds_khoahoc = KhoaHoc.objects.all()
    if request.POST.get("btnLuu"):
        bv = BaiViet()
        bv.ten_bai = request.POST['txttenbai']
        bv.noi_dung = request.POST['txtnoidung']
        bv.khoa_hoc_id = request.POST['select_khoahoc']
        bv.tac_gia_id = "anhtuan"
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
        bv.tac_gia_id = "anhtuan"
        bv.tong_so_view = 0
        bv.tong_so_binh_luan = 0
        bv.trang_thai = "on"
        bv.save()
        return redirect('baiviet_ds')
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
    context = {"ds_khoahoc": ds_khoahoc, "user":user}
    template = loader.get_template('baiviet_them.html')
    return HttpResponse(template.render(context, request))

def sua(request, bai_viet_id):
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
    context = {"baiviet": bv, "ds_khoahoc": ds_khoahoc, "user":user}
    template = loader.get_template('baiviet_sua.html')
    return HttpResponse(template.render(context, request))

def xoa(request, bai_viet_id):
    BaiViet.objects.get(pk=bai_viet_id).delete()
    return redirect('baiviet_ds')