from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from cdh.models import ChuyenNganh, KhoaHoc, BaiViet, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    """

    :type request: object
    """
    ds_chuyen_nganh = ChuyenNganh.objects.all()
    ds_khoa_hoc = KhoaHoc.objects.order_by("ma_khoa_hoc")[:6]
    temp = loader.get_template('web/home.html')

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
    else:
        if request.GET.get("btnlogin"):
            username = request.GET['username']
            matkhau = request.GET['password']
            try:
                user = User.objects.get(username=username, mat_khau=matkhau)
            except:
                user = ""
            if user:
                request.session['username'] = user.username



        if request.GET.get("btndangki"):
            u = User()
            u.username = request.GET.get('txtusername')
            u.mat_khau = request.GET.get('txtpassword1')
            u.ho_ten = request.GET.get('txthoten')
            u.img = "uploads/imguser.png"
            u.gioi_tinh = " "
            u.loai_user_id = 2
            u.save()
    context = {
        "ds_chuyen_nganh": ds_chuyen_nganh,
        "ds_khoa_hoc": ds_khoa_hoc,
        "user":user,

        "q": query,
    }
    return HttpResponse(temp.render(context))

def login(request):
    user = User.objects.get(username=request.POST['username'])
    if user.password == request.POST['password']:
        request.session['username'] = user.username
        request.session.set_expiry(15);
        return HttpResponse("Đã đăng nhập")
    else:
        return HttpResponse("user và pass chưa đúng")
#
# def logout(request):
#     try:
#         del request.session['username']
#     except KeyError:
#         pass
#     return HttpResponse("Bạn đã đăng xuất")