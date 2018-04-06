from django import forms
from django.db import models
from  ckeditor.fields import RichTextField

class UploadFileForm(forms.Form):
    file = forms.FileField()

class baiviet_form(forms.Form):
    noidung = forms.CharField(max_length=10)

class KhoaHoc_form(forms.Form):
    ma_khoa_hoc = models.IntegerField()
    ten_khoa_hoc = models.CharField(max_length=50)
    img = models.CharField(max_length=200)
    le_phi = models.CharField()
    gioi_thieu = RichTextField()
    tac_gia = models.CharField()
    chuyen_nganh = models.CharField()
