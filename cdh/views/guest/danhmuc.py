from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from cdh.models import BaiViet, KhoaHoc, ChuyenNganh, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import hashlib


def index(request, chuyen_nganh_id):
    danh_muc = ChuyenNganh.objects.get(ma_chuyen_nganh = chuyen_nganh_id)
    ds_chuyen_nganh = ChuyenNganh.objects.all()
    ds_khoa_hoc = KhoaHoc.objects.filter(chuyen_nganh_id = chuyen_nganh_id).order_by('ma_khoa_hoc')[::-1]
    temp = loader.get_template('web/danhmuc.html')
    query = request.GET.get("q")
    if query:
        ds_khoa_hoc = KhoaHoc.objects.filter(ten_khoa_hoc__icontains = query)
    paginator = Paginator(ds_khoa_hoc, 6)
    pageNumber = request.GET.get('page')
    try:
        ds_khoa_hoc = paginator.page(pageNumber)
    except PageNotAnInteger:
        ds_khoa_hoc = paginator.page(1)
    except EmptyPage:
        ds_khoa_hoc = paginator.page(paginator.num_pages)

    user = ""
    if request.session.has_key('username'):
        username = request.session['username']
        user = User.objects.get(username=username)
        if request.GET.get("btnlogout"):
            del request.session['username']
            user = ""
            return redirect('trangchu')
    if request.GET.get("btnlogin"):
        u = User()
        u.username = request.GET['username']
        u.mat_khau = request.GET['password']
        u.mat_khau = hashlib.sha256(b"u.mat_khau").hexdigest()
        try:
            user = User.objects.get(username=u.username, mat_khau=u.mat_khau)
        except:
            user = ""
        return redirect('trangchu')

    if request.GET.get("btndangki"):
        u = User()
        u.username = request.GET.get('txtusername')
        u.mat_khau = request.GET.get('txtpassword1')
        u.mat_khau = hashlib.sha256(b"u.mat_khau").hexdigest()
        u.ho_ten = request.GET.get('txthoten')
        u.img = "uploads/imguser.png"
        u.gioi_tinh = " "
        u.loai_user_id = 2
        u.save()
        return redirect('trangchu')

    context = {
        "ds_khoa_hoc": ds_khoa_hoc,
        "q": query,
        "ds_chuyen_nganh": ds_chuyen_nganh,
        "danh_muc": danh_muc,
        "user":user,
        # "username":username,
    }
    return HttpResponse(temp.render(context))