from django.http import HttpResponse
from django.template import loader


def index(resquest):
    temp = loader.get_template('index.html')
    context = {
        "ds_danhmuc": "",
    }
    return HttpResponse(temp.render(context))