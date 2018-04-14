from django.db import models
from ckeditor.fields import RichTextField, RichTextFormField, CKEditorWidget

class LoaiUser(models.Model):
    ma_loai = models.AutoField(primary_key=True)
    ten_loai = models.CharField(max_length=50)

class User(models.Model):
    username = models.CharField(primary_key=True, max_length=20)
    ho_ten = models.CharField(max_length=50)
    mat_khau = models.CharField(max_length=200)
    img = models.CharField(max_length=250)
    gioi_tinh = models.CharField(max_length=3)
    dia_chi = models.CharField(max_length=250)
    loai_user = models.ForeignKey('LoaiUser', on_delete=models.CASCADE)

class ChuyenNganh(models.Model):
    ma_chuyen_nganh = models.AutoField(primary_key=True)
    ten_chuyen_nganh = models.CharField(max_length=50)

class KhoaHoc(models.Model):
    ma_khoa_hoc = models.AutoField(primary_key=True)
    ten_khoa_hoc = models.CharField(max_length=50)
    img = models.ImageField(upload_to='uploads/')
    le_phi = models.IntegerField()
    gioi_thieu = models.TextField()
    tac_gia = models.ForeignKey('User', on_delete=models.CASCADE)
    chuyen_nganh = models.ForeignKey('ChuyenNganh', on_delete=models.CASCADE)

class BaiViet(models.Model):
    ma_bai = models.AutoField(primary_key=True)
    trang_thai = models.CharField(max_length=3)
    ten_bai = models.CharField(max_length=50)
    noi_dung = RichTextField('Soạn thảo theo cách của riêng bạn')
    tong_so_view = models.IntegerField(default=0)
    tong_so_binh_luan = models.IntegerField(default=0)
    khoa_hoc = models.ForeignKey('KhoaHoc')
    tac_gia = models.ForeignKey('User')

class DangKi(models.Model):
    ma_dang_ki = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    khoa_hoc = models.ForeignKey('KhoaHoc', on_delete=models.CASCADE)
    trang_thai = models.CharField(max_length=3)

class TuongTac(models.Model):
    ma_tuong_tac = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    bai_viet = models.ForeignKey('BaiViet', on_delete=models.CASCADE)
    so_view = models.IntegerField(default=0)
    so_binh_luan = models.IntegerField(default=0)

class BinhLuan(models.Model):
    ma_binh_luan = models.AutoField(primary_key=True)
    noi_dung = models.TextField(max_length=1000)
    tuong_tac = models.ForeignKey('TuongTac', on_delete=models.CASCADE)

class Customer(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=20)