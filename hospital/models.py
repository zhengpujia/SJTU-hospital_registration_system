from django.db import models
from django.contrib import admin
# Create your models here.

from django.db import models

STATUS_CHOICES = [
    ('a', 'ratify'),
]
class Patient(models.Model):
    phone = models.CharField(u'患者电话', max_length=11)
    password = models.CharField(u'患者密码', max_length=30)
    name = models.CharField(u'患者姓名', max_length=10)
    sex = models.CharField(u'患者性别', max_length=1)
    age = models.CharField(u'患者年龄', max_length=3)

    class Meta:
        verbose_name = '患者'
        verbose_name_plural = '患者列表'


class Department(models.Model):
    name = models.CharField(u'科室名字', max_length=10)
    parentid = models.IntegerField(u'上级科室id')
    address = models.CharField(u'科室地址', max_length=30)

    class Meta:
        verbose_name = '科室'
        verbose_name_plural = '科室列表'


class Doctor(models.Model):
    phone = models.CharField(u'医生电话', max_length=11)
    password = models.CharField(u'医生密码', max_length=30)
    name = models.CharField(u'医生姓名', max_length=10)
    sex = models.CharField(u'医生性别', max_length=1)
    age = models.CharField(u'医生年龄', max_length=3)
    img = models.ImageField(u'医生照片', upload_to='doctorimages/')
    level = models.CharField(u'职位等级', max_length=10)
    description = models.CharField(u'详细描述', max_length=50)
    registration_price = models.IntegerField(u'挂号价格')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def getDepartment(self):
        return Department.objects.get(id=self.department)

    class Meta:
        verbose_name = '医生'
        verbose_name_plural = '医生列表'


class CheckInRecord(models.Model):
    date = models.DateTimeField(u'打卡时间')
    name = models.CharField(u'医生姓名', max_length=10)
    class Meta:
        verbose_name = '签到记录'
        verbose_name_plural = '签到记录'


class TimeNumber(models.Model):
    eight = models.PositiveSmallIntegerField(u'八点可预约人数',blank=True,default=10)
    nine = models.PositiveSmallIntegerField(u'九点可预约人数',blank=True,default=10)
    ten = models.PositiveSmallIntegerField(u'十点可预约人数',blank=True,default=10)
    eleven = models.PositiveSmallIntegerField(u'十一点可预约人数',blank=True,default=10)
    fourteen = models.PositiveSmallIntegerField(u'十四点可预约人数',blank=True,default=10)
    fifteen = models.PositiveSmallIntegerField(u'十五点可预约人数',blank=True,default=10)
    sixteen = models.PositiveSmallIntegerField(u'十六点可预约人数',blank=True,default=10)
    seventeen = models.PositiveSmallIntegerField(u'十七点可预约人数',blank=True,default=10)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    default_number = models.PositiveSmallIntegerField(u'默认一个时间点可预约人数',blank=True,default=10)

    def allNumberSetDefault(self):
        '''每天晚上0点可以调用此方法重置可预约人数'''
        self.eight = self.default_number
        self.nine = self.default_number
        self.ten = self.default_number
        self.eleven = self.default_number
        self.fourteen = self.default_number
        self.fifteen = self.default_number
        self.sixteen = self.default_number
        self.seventeen = self.default_number

    class Meta:
        verbose_name = '某时间点可预约人数'
        verbose_name_plural = '某时间点可预约人数列表'


class Register(models.Model):
    patient_name = models.CharField(u'患者姓名', max_length=10)
    doctor_name = models.CharField(u'医生姓名', max_length=10)
    registration_time = models.DateTimeField(u'挂号时间')
    consultation_hours = models.DateTimeField(u'会诊时间')
    illness = models.CharField(u'病情概要', max_length=50)
    address = models.CharField(u'会诊地址', max_length=30)
    isdelete = models.BooleanField(u'挂号是否已经删除', default=False)
    out_trade_num = models.UUIDField(u'商户订单号')
    status = models.CharField(u'状态', max_length=10, default='待支付')
    payway = models.CharField(u'支付方式', max_length=10, default='alipay')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def getPatient(self):
        return Patient.objects.get(id=self.patient)

    def getDoctor(self):
        return Doctor.objects.get(id=self.doctor)

    class Meta:
        verbose_name = '挂号单'
        verbose_name_plural = '挂号单列表'

class DoctorAffair(models.Model):
    name =  models.CharField(u'医生名字',max_length=10)
    leave = models.CharField(u'请假',max_length=10)
    business = models.CharField(u'出差',max_length=10)
    apply = models.CharField(u'报销',max_length=10)
    solveleave = models.IntegerField(u'批准请假',max_length=10)
    solvebusiness = models.IntegerField(u'批准出差',max_length=10)
    solve = models.IntegerField(u'批准',max_length=10)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    class Meta:
        verbose_name = '医生事务'
        verbose_name_plural = '事务列表'
