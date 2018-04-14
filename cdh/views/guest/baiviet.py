from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from cdh.models import BaiViet, KhoaHoc, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import hashlib


def index(request, bai_viet_id):
    if not request.session.has_key('username'):
        return redirect('trangchu')
    ct_bai_viet = BaiViet.objects.get(pk=bai_viet_id)
    khoa_hoc = KhoaHoc.objects.get(pk=ct_bai_viet.khoa_hoc_id)
    ds_khoa_hoc = KhoaHoc.objects.filter(chuyen_nganh_id = khoa_hoc.chuyen_nganh_id)[:4]
    ds_bai_viet = BaiViet.objects.filter(khoa_hoc_id= khoa_hoc.ma_khoa_hoc).order_by('ma_bai')[::1]
    temp = loader.get_template('web/baiviet.html')
    query = request.GET.get("q")
    if query:
        ds_bai_viet = BaiViet.objects.filter(ten_bai__icontains = query)
    paginator = Paginator(ds_bai_viet, 6)
    pageNumber = request.GET.get('page')
    try:
        ds_bai_viet = paginator.page(pageNumber)
    except PageNotAnInteger:
        ds_bai_viet = paginator.page(1)
    except EmptyPage:
        ds_bai_viet = paginator.page(paginator.num_pages)

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


    context = {
        "khoa_hoc": khoa_hoc,
        "ct_bai_viet": ct_bai_viet,
        "ds_bai_viet": ds_bai_viet,
        "q": query,
        "user": user,
        "ds_khoa_hoc": ds_khoa_hoc,
        # "username": username,
    }
    return HttpResponse(temp.render(context))