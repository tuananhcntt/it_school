from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from cdh.models import ChuyenNganh, KhoaHoc, BaiViet, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import hashlib

def index(request):
    """

    :type request: object
    """
    temp = loader.get_template('hopthu.html')
    ds_khoa_hoc = ""
    query = request.GET.get("q")
    if query:
        ds_khoa_hoc = KhoaHoc.objects.filter(ten_khoa_hoc__icontains = query)

    user = ""
    if request.session.has_key('username'):
        username = request.session['username']
        user = User.objects.get(username=username)
        if request.GET.get("btnlogout"):
            del request.session['username']
            user = ""
            return redirect('trangchu')
    else:
        if request.GET.get("btnlogin"):
            u = User()
            u.username = request.GET['username']
            u.mat_khau = request.GET['password']
            u.mat_khau = hashlib.sha256(b"u.mat_khau").hexdigest()
            try:
                user = User.objects.get(username=u.username, mat_khau= u.mat_khau)
            except:
                user = ""
            if user:
                request.session['username'] = user.username
            return redirect('hopthu')
    context = {

        "ds_khoa_hoc": ds_khoa_hoc,
        "user":user,
        "q": query,
    }
    return HttpResponse(temp.render(context))