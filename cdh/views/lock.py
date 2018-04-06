from django.shortcuts import redirect
from cdh.models import User



def login(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        matkhau = request.GET.get('password')
        try:
            user = User.objects.get(username=username, mat_khau=matkhau)

        except:
            user = ""
        if user:
            request.session['username'] = user.username
            redirect('trangchu')
