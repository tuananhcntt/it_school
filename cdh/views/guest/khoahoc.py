from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from cdh.models import BaiViet, KhoaHoc, ChuyenNganh, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request, khoa_hoc_id):

    khoa_hoc = KhoaHoc.objects.get(ma_khoa_hoc = khoa_hoc_id)
    ds_chuyen_nganh = ChuyenNganh.objects.all()
    ds_bai = BaiViet.objects.filter(khoa_hoc_id = khoa_hoc_id, trang_thai = 'on').order_by('ma_bai')[::-1]
    temp = loader.get_template('web/khoahoc.html')
    query = request.GET.get("q")
    if query:
        ds_bai = BaiViet.objects.filter(ten_bai__icontains = query)
    paginator = Paginator(ds_bai, 6)
    pageNumber = request.GET.get('page')
    try:
        ds_bai = paginator.page(pageNumber)
    except PageNotAnInteger:
        ds_bai = paginator.page(1)
    except EmptyPage:
        ds_bai = paginator.page(paginator.num_pages)

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
        "khoa_hoc": khoa_hoc,
        "q": query,
        "ds_chuyen_nganh": ds_chuyen_nganh,
        "ds_bai": ds_bai,
        "user":user,
        # "username":username,
    }
    return HttpResponse(temp.render(context))