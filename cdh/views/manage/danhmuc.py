from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from cdh.models import ChuyenNganh, Customer, User,LoaiUser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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

    ds_danhmuc = ChuyenNganh.objects.all().order_by('ma_chuyen_nganh')[::-1]
    temp = loader.get_template('danhmuc_ds.html')
    query = request.GET.get("q")
    if query:
        ds_danhmuc = ChuyenNganh.objects.filter(ten_chuyen_nganh__icontains = query)
    paginator = Paginator(ds_danhmuc, 5)
    pageNumber = request.GET.get('page')
    try:
        ds_danhmuc = paginator.page(pageNumber)
    except PageNotAnInteger:
        ds_danhmuc = paginator.page(1)
    except EmptyPage:
        ds_danhmuc = paginator.page(paginator.num_pages)

    context = {
        "ds_danhmuc": ds_danhmuc,
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
        dm = ChuyenNganh()
        dm.ten_chuyen_nganh = request.POST['txttendm']
        dm.save()
        return redirect('danhmuc_ds')

    context = {"title": "danh muc | them", "user":user}
    template = loader.get_template('danhmuc_them.html')
    return HttpResponse(template.render(context, request))

def sua(request, danh_muc_id):
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

    danhmuc = ChuyenNganh.objects.get(pk=danh_muc_id)
    if request.method == "POST":
        danhmuc.ten_chuyen_nganh = request.POST['txttendm']
        danhmuc.save()
        return redirect('danhmuc_ds')

    context = {"danh_muc": danhmuc, "user":user}
    template = loader.get_template('danhmuc_sua.html')
    return HttpResponse(template.render(context, request))

def xoa(request, danh_muc_id):
    ChuyenNganh.objects.get(pk=danh_muc_id).delete()
    return redirect('danhmuc_ds')


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