from django.contrib import admin
from .models import *
# Register your models here.


admin.site.site_header = '后台管理系统'
admin.site.index_title = '首页'

class DepartmentAdmin(admin.ModelAdmin):
    list_display=('id','name','address')
    search_fields=['name','address']
    list_filter=('name','address')
    ordering=['id']

class PatientAdmin(admin.ModelAdmin):
    list_display=('id','name','sex','age','phone','password')
    search_fields=['id','name','sex','age','phone','password']
    list_filter=('id','name','sex','age','phone','password')
    ordering=['id']


class DoctorAdmin(admin.ModelAdmin):
    list_display=('id','name','sex','age','department','level','registration_price','description','phone','password')
    search_fields=['id','name','sex','age','department','level','registration_price','description','phone','password']
    list_filter=('id','name','registration_price','age','level','department')
    ordering=['id']


class TimeNumberAdmin(admin.ModelAdmin):
    list_display=('id','doctor','eight','nine','ten','eleven','fourteen','fifteen','sixteen','seventeen','default_number')
    search_fields=['id','doctor__name']
    list_filter=('id','doctor__name')
    ordering=['id']

class RegisterAdmin(admin.ModelAdmin):
    list_display=('id','patient','doctor','registration_time','consultation_hours','illness','address','out_trade_num','status','payway')
    search_fields=['id','patient','doctor','registration_time','consultation_hours','illness','address','isdelete','out_trade_num','status','payway']
    list_filter=('id','patient','doctor','registration_time','consultation_hours','illness','address','out_trade_num','status','payway')
    ordering=['id']

class DoctorAffairAdmin(admin.ModelAdmin):
    list_display=['name','leave','business','apply','solvebusiness','solveleave','solve']
    actions = ['make_published']

    def make_published(self, request, queryset):
        queryset.delete()
    make_published.short_description = "批准"

admin.site.register(Patient,PatientAdmin)
admin.site.register(Department,DepartmentAdmin)
admin.site.register(Doctor,DoctorAdmin)
admin.site.register(TimeNumber,TimeNumberAdmin)
admin.site.register(Register,RegisterAdmin)
admin.site.register(DoctorAffair,DoctorAffairAdmin)
admin.site.register(CheckInRecord)
