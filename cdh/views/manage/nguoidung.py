from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from cdh.models import ChuyenNganh, Customer, User,LoaiUser
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


    temp = loader.get_template('nguoidung_ds.html')
    query = request.GET.get("q")
    if user.loai_user_id == 0:
        ds_nguoidung = User.objects.filter(loai_user_id = 1).order_by('username')[::-1]

    if user.loai_user_id == 1:
        ds_nguoidung = User.objects.filter(loai_user_id=2).order_by('username')[::-1]

    if query and user.loai_user_id == 0 :
        ds_nguoidung = User.objects.filter(loai_user_id=1, ho_ten__icontains = query).order_by('username')[::-1]

    if query and user.loai_user_id == 1:
        ds_nguoidung = User.objects.filter(loai_user_id=2, ho_ten__icontains = query).order_by('username')[::-1]
    paginator = Paginator(ds_nguoidung, 5)
    pageNumber = request.GET.get('page')
    try:
        ds_nguoidung = paginator.page(pageNumber)
    except PageNotAnInteger:
        ds_nguoidung = paginator.page(1)
    except EmptyPage:
        ds_nguoidung = paginator.page(paginator.num_pages)

    context = {
        "ds_nguoidung": ds_nguoidung,
        "q": query,
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

    if request.method == "POST":
        u = User()
        u.username = request.GET.get('txtusername')
        u.mat_khau = request.GET.get('txtpassword1')
        u.mat_khau = hashlib.sha256(b"u.mat_khau").hexdigest()
        u.ho_ten = request.GET.get('txthoten')
        u.img = "uploads/imguser.png"
        u.gioi_tinh = " "
        u.loai_user_id = 1
        u.save()
        return redirect('nguoidung_ds')

    context = {"title": "nguoi dung | them", "user":user}
    template = loader.get_template('nguoidung_them.html')
    return HttpResponse(template.render(context, request))

def sua(request, nguoi_dung_id):
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

    nguoidung = User.objects.get(pk=nguoi_dung_id)
    if request.method == "POST":
        nguoidung.mat_khau = request.GET.get('txtpassword1')
        nguoidung.mat_khau = hashlib.sha256(b"u.mat_khau").hexdigest()
        nguoidung.ho_ten = request.GET.get('txthoten')
        nguoidung.img = request.GET.get('fileimg')
        nguoidung.gioi_tinh = request.GET.get('txtgioitinh')
        nguoidung.loai_user_id = 1
        nguoidung.save()
        return redirect('nguoidung_ds')

    context = {"nguoi_dung": nguoidung, "user":user}
    template = loader.get_template('nguoidung_sua.html')
    return HttpResponse(template.render(context, request))

def xoa(request, nguoi_dung_id):
    User.objects.get(pk=nguoi_dung_id).delete()
    return redirect('nguoidung_ds')


def listing(request):
    customer_list = Customer.objects.all()
    paginator = Paginator(customer_list, 5)

    pageNumber = request.GET.get('page')
    try:
        customers = paginator.page(pageNumber)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)

    return render(request, 'list.html', {'customers': customers})