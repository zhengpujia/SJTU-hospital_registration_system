from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render
from django.utils.datetime_safe import date
from django.views import View
from .models import *
import datetime
import uuid
from alipay import AliPay
from django.db.models import Q
from navigation import PlotLineOnMap 
import pymysql

# Create your views here.
def search(request):
    # 获取用户输入的科室名称和医生姓名
    department = request.GET.get("department")
    doctor = request.GET.get("doctor")
    # 查询数据库中符合条件的科室对象
    departments = Department.objects.filter(name__contains=department)
    # 查询数据库中符合条件的医生对象
    doctors = Doctor.objects.filter(name__contains=doctor, department__in=departments)
    # 返回一个包含查询结果的HTML模板
    return render(request, "search.html", {"doctors": doctors})


class ChooseLoginView(View):
    '''选择身份登录'''

    def get(self, request):
        return render(request, 'chooselogin.html')


class PatientLoginView(View):
    '''患者登录'''

    def get(self, request):
        return render(request, 'patientlogin.html')

    def post(self, request):
        phone = request.POST.get('phone', '')
        password = request.POST.get('password', '')

        patient_list = Patient.objects.filter(phone=phone, password=password)
        if patient_list:
            request.session['patient'] = patient_list[0]

            return HttpResponseRedirect("/patientcenter/")

        return HttpResponse("登录有问题")


class DoctorLoginView(View):
    '''医生登录'''

    def get(self, request):
        return render(request, 'doctorlogin.html')

    def post(self, request):
        phone = request.POST.get('phone', '')
        password = request.POST.get('password', '')

        doctor_list = Doctor.objects.filter(phone=phone, password=password)
        if doctor_list:
            request.session['doctor'] = doctor_list[0]

            return HttpResponseRedirect("/doctorcenter/")

        return HttpResponse("登录有问题")


class PatientRegisterView(View):
    '''患者注册'''

    def get(self, request):
        return render(request, 'patientregister.html')

    def post(self, request):
        # 只能注册患者账号 医生账号只能由管理员添加
        phone = request.POST.get('phone', '')

        patientlist = Patient.objects.filter(phone=phone)
        if patientlist:
            return render(request, 'patientregister.html', {"err": 1, "tips": "*该号码已经被注册"})
        else:
            password = request.POST.get('password', '')
            name = request.POST.get('name', '')
            sex = request.POST.get('sex', '')
            age = request.POST.get('age', '')

            patient = Patient.objects.create(phone=phone, password=password, name=name, sex=sex, age=age)

            if patient:
                return HttpResponseRedirect("/patientlogin/")

            return HttpResponseRedirect("/patientregister/")


class PatientCenterView(View):
    '''患者界面'''

    def get(self, request):
        patient = request.session.get('patient', '')

        return render(request, 'patientcenter.html', {'patient_name': patient.name})


class ChooseDepartmentView(View):
    '''选择科室'''

    def get(self, request):
        parentid_department_list = [o.id for o in Department.objects.filter(parentid=0)]
        #print(parentid_department_list)
        all_department_list = dict()
        for id in parentid_department_list:
            all_department_list[Department.objects.filter(id=id)[0].name] = Department.objects.filter(parentid=id)

            #print(Department.objects)

        return render(request, 'choosedepartment.html', {'all_department_list': all_department_list})


class ChooseDoctorAndTimeView(View):
    '''选择医生和时间'''

    def get(self, request, department_id):
        department_id = int(department_id)

        department_name = Department.objects.get(id=department_id).name  # 科室名字

        doctor_list = Doctor.objects.filter(department_id=department_id)  # 当前科室里的医生

        doctor_time_number_list = []  # 此医生及其的可预约时间和人数列表
        for doctor in doctor_list:
            doctor_id = doctor.id
            doctor_time_number_list.append([doctor, TimeNumber.objects.get(doctor_id=doctor_id)])

        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        
        return render(request, 'choosedoctorandtime.html',
                      {'department_name': department_name, 'doctor_time_number_list': doctor_time_number_list,
                       'department_id': department_id, 'tomorrow': tomorrow})

# 支付宝公钥
alipay_public_key = '-----BEGIN PUBLIC KEY-----\n'\
+'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoURjWSKmxPhVCifg/rchD11TSMkttEbNurfWVQB1HedkdH0wNkJcZZTJQZ4Z3cCoLjkeG9vIsFuEjEOyC+uJLrf+iktC4W99YuLHPwrcntPs2qqBwfMpjzdZgFS3gPbnjM4fZ0JB4V1AUdNd4YDCOW9prTfcoFse1Dce5Mov30IrFyDX2BAdj7CBMzbHq/5m2dk8zu9Qy8TOYRaJlycxPGTwBkBGFxQuxgbAtk0CNGtGLaYGH+j3ycPlkGWymSZFw2Xf9iCo63+qIwGt39zpai3TV45E0EF3kjYfR3P74qVQ41hWSei9bn/gSccOh8ohv4vRyQv3KwBoLh3bGeMKTQIDAQAB'\
+'\n-----END PUBLIC KEY-----'

# 应用私钥
my_private_key = '-----BEGIN RSA PRIVATE KEY-----\n'\
+'MIIEowIBAAKCAQEAwZBaxmwDkDoISiwC7vMMn/CD2vrgAM/Gfq6XPCbaRXNNu57R3lXpc/o7zqr16Hv2XPR4Ixcl7nQZkOq6lu4mD6ks39dmFuXdc5OhRvplxELBeyjg+GLfoRBsEykJykDIVWJt57SFRWTnsYOkUDQt45kxtEaGK/WkzDq32OJRLjNms2xK0CzYJ6ojuAPLZ9oDAwGW5lq75AaXA7Q9iuyKeDmsgV9zkmzyc3g7Q+SVHsFcqz4l0V5mWTkjMDT0TGyamypgChVZTwobwQ37RTkoVjBnPKyojsMYluD3MzZ0d910o3PJ6SIjpKktCDGfbc7TFjAK4WheKMDcm7dPG9cK+QIDAQABAoIBAHy7gUOMJ1+xhdYGNn20sdX/L3jVYbQkME1CRMLGZrGKc/ULi0IzKpVKE3BCSuTdvQx5nVE/gXn/5tmz6TmJjY1Z/0jfjTIEPohUAgGzKhEm03eCCDcHwAQSiRJvx5dF19Lt8tT1R0xIkeWaZzAn78pS1ezN5Xg+e0wAKqjgbl/OLuYsvf/hNpa0uVAFhgPBAtY9Zq+AZHtL8lkSzJes2+znaqAQjIBbQTZbktgue69l6vNG5FeHU5qXtyky6uQvchybIZ+SvMQuXo+RQHFhQYXqv9ByRzBr02N433svCyRDduZgESdZ5qYnVe+UhRbfozNs0WMAJiTm1X5QYKijeOECgYEA+mS8cO7ww0ty8gKt12nVOqOzVIQDq/pJ01jz5dUUwO1oAHjH3+KAK8ony5PBSqprr6Q1w1xrpCPOOrMzIF+fNUXREE6AxdwJNineTeU0N5G4e9pUaVQxSBHA3DPVViFqAz7tna2m3xCepZt/hrS2vLWLg2lsQOKwksK0WGKU3GsCgYEAxeXehon/qs3jyMl3w+1LTTO1R36qi3QWluzRR/u2yh0OiO1Rt8LjNpNqFRQTdVYEJKeurEY57csM0bDJQk2IpEEL7PuEf4ZVZ8LU/kuwo+jQJNSJFSsIgTyNcQzFzWGQhSrGI6cF09RO1RHyzswsDevFnxYdU2kxDlB3HPqzTysCgYBGpcORbalawN/2rpDUFZVHDUcc0n6iuGS6EAAI2d0YLiPI9ksWvTaCpHAj/VVtNrZZgVB2BY6NaljWsRb8zF4ETuWU30FwEgw7TwbdHY1lHGVb9JcafNnGxtOOjcVkntrlfYzXj1Zk27CXc09A954TknmBo24axJsjXXI6+d2cbwKBgCSxDQQW2/9YMy6MJBeAjKCgwLCjzI0UlgefmuHkyqxInORIVAllKel5hYao9T6hFx2QtXMdhioPpq3OQFJ5u6bwpHxo2dUnG/ikCAeqEvMg/E6H1W7GTspfZr4aJyaAO2JlXt1HX246A++/ZyxucJCYMUjguck4TK8hviPyW4KHAoGBANBTkxV6oxO52OBESGp8yYXiePW/Mu0+y0gQj8AWCvUI7Kdot0EGnXkHEkVDbCeK6vPA6c6Pn/LSbDc35zqNJcXPbk4T7duj6PnWl37hPr6MdHxj0wYD6eD1khRyqpRCTqWv79t+b5wEYfzW5fsHy9+BmtN2liSifyqZ+CJeRt26'\
+'\n-----END RSA PRIVATE KEY-----'

# 创建AliPay对象
alipay = AliPay(
    appid='9021000129613354',	
    #app_notify_url='http://127.0.0.1:8000/checkpay/',
    app_private_key_string=my_private_key,
    alipay_public_key_string=alipay_public_key,
    sign_type='RSA2',
    debug=True,
    config={
        'use_sandbox': True
    }
)


class ConfirmRegistrationView(View):
    '''确认挂号信息'''

    def get(self, request, department_id, doctor_id, consultation_hours):
        department_id = int(department_id)
        doctor_id = int(doctor_id)

        patient = request.session.get('patient', '')
        doctor = Doctor.objects.get(id=doctor_id)
        department = Department.objects.get(id=department_id)

        patient_name = patient.name
        doctor_name = doctor.name
        registration_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        consultation_hours = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime(
            "%Y-%m-%d") + " " + consultation_hours
        # doctor_id
        patient_id = patient.id
        address = department.address
        registration_price = doctor.registration_price
        # print(patient_name,doctor_name,registration_time,consultation_hours,doctor_id,patient_id,address)

        return render(request, 'confirmregistration.html', {'patient_name': patient_name, 'doctor_name': doctor_name,
                                                            'registration_time': registration_time,
                                                            'consultation_hours': consultation_hours,
                                                            'doctor_id': doctor_id, 'patient_id': patient_id,
                                                            'address': address,
                                                            'registration_price': registration_price})

    def post(self, request):
        patient_name = request.POST.get('patient_name', '')
        doctor_name = request.POST.get('doctor_name', '')
        registration_time = request.POST.get('registration_time', '')
        consultation_hours = request.POST.get('consultation_hours', '')
        illness = request.POST.get('illness', '')
        doctor_id = request.POST.get('doctor_id', '')
        patient_id = request.POST.get('patient_id', '')
        address = request.POST.get('address', '')
        out_trade_num = uuid.uuid4().hex
        payway = 'alipay'
        status = '待支付'
        isdelete = 1

        register = Register.objects.create(patient_name=patient_name, doctor_name=doctor_name,
                                           registration_time=registration_time,
                                           consultation_hours=consultation_hours, illness=illness, doctor_id=doctor_id,
                                           patient_id=patient_id, address=address, isdelete=isdelete,
                                           out_trade_num=out_trade_num,
                                           payway=payway, status=status)

        registration_price = request.POST.get('registration_price', '')
        params = alipay.api_alipay_trade_page_pay(
            subject='医院挂号',
            out_trade_no=register.out_trade_num,
            total_amount=registration_price,
            return_url='http://127.0.0.1:8000/checkpay/'
        )
        url = 'https://openapi-sandbox.dl.alipaydev.com/gateway.do' + '?' + params
        #url = 'https://openapi-sandbox.dl.alipaydev.com/gateway.do'
        return HttpResponseRedirect(url)


class CheckPayView(View):
    def get(self, request):
        params = request.GET.dict()
        sign = params.pop('sign')
        if alipay.verify(params, sign):
            out_trade_no = params.get('out_trade_no', '')
            register = Register.objects.get(out_trade_num=out_trade_no)
            register.status = '待检查'
            register.isdelete = 0
            register.save()

            doctor_time_number = TimeNumber.objects.get(doctor_id=register.doctor_id)
            consultation_hours_time = str(register.consultation_hours)[11:]
            if consultation_hours_time == '08:00:00':
                doctor_time_number.eight -= 1
            elif consultation_hours_time == '09:00:00':
                doctor_time_number.nine -= 1
            elif consultation_hours_time == '10:00:00':
                doctor_time_number.ten -= 1
            elif consultation_hours_time == '11:00:00':
                doctor_time_number.eleven -= 1
            elif consultation_hours_time == '14:00:00':
                doctor_time_number.fourteen -= 1
            elif consultation_hours_time == '15:00:00':
                doctor_time_number.fifteen -= 1
            elif consultation_hours_time == '16:00:00':
                doctor_time_number.sixteen -= 1
            elif consultation_hours_time == '17:00:00':
                doctor_time_number.seventeen -= 1
            doctor_time_number.save()

            return HttpResponseRedirect('/patientshowregistration/')
        out_trade_no = params.get('out_trade_no', '')
        register = Register.objects.get(out_trade_num=out_trade_no)
        register.isdelete = 1
        register.save()

        return HttpResponseRedirect('/choosedepartment/')


class PatientShowRegistrationView(View):
    '''患者展示挂号信息'''

    def get(self, request):
        patient = request.session.get('patient')
        register_list = patient.register_set.order_by('-consultation_hours').filter(
            Q(isdelete=False, status='待检查') | Q(isdelete=False, status='已检查')).all()

        return render(request, 'patientshowregistration.html', {'register_list': register_list})


class GuideView(View):
    def get(self, request):
        return render(request, 'guide.html')


class TrafficView(View):
    def get(self, request):
        return render(request, 'choosepoint.html')
    def post(self, request):
        num = request.POST.get('num', '')
        lat = request.POST.get('lat', '')
        lon = request.POST.get('lon', '')
        if num=='1':
            return render(request, 'showpoint1.html')
        elif num=='2':
            return render(request, 'showpoint2.html')
        elif num=='3':
            return render(request, 'showpoint3.html')
        else:
            if lat!='' and lon !='':
                PlotLineOnMap(lat,lon)
                return render(request, 'choosepoint1.html')
            return HttpResponse("请输入有效位置序号")
        

        
    
class DoctorCenterView(View):
    '''医生界面'''

    def get(self, request):
        doctor = request.session.get('doctor', '')

        return render(request, 'doctorcenter.html', {'doctor_name': doctor.name})


class DoctorShowRegistrationView(View):
    '''医生展示挂号信息'''

    def get(self, request):
        doctor = request.session.get('doctor')
        try:
            register_list = doctor.register_set.order_by('consultation_hours').filter(isdelete=0, status='待检查').all()
        except:
            register_list = []

        return render(request, 'doctorshowregistration.html', {'register_list': register_list})

    def post(self, request):
        register_id = request.POST.get('register_id', '')
        register = Register.objects.get(id=register_id)
        register.status = '已检查'
        register.save()

        doctor = request.session.get('doctor')
        try:
            register_list = doctor.register_set.order_by('consultation_hours').filter(isdelete=0, status='待检查').all()
        except:
            register_list = []

        return render(request, 'doctorshowregistration.html', {'register_list': register_list})

class DoctorSigninView(View):
    '''打卡签到'''

    def get(self, request):
        doctor = request.session.get('doctor', '')

        if CheckInRecord.objects.filter(name=doctor.name, date=date.today()).exists():
            return render(request, 'signinalready.html', {'doctor_name': doctor.name})

        name = doctor.name
        CheckInRecord.objects.create(name=name, date=date.today())
        return render(request, 'signinsuccessfully.html', {'doctor_name': doctor.name})
    
class DoctorClockin(View):
    def get(self,request):
        list = request.session.get('doctor')
        doctorin = list.clockin
        name = list.name
        if doctorin != 0:
            return render(request,'doctorclockinalready.html',{'name' : name})
        else:
            conn = pymysql.connect(host='localhost', user='root', password='123456', database='hospital')
            # 创建游标对象
            cursor = conn.cursor()
            # 执行SQL语句更新数据
            sql = "UPDATE hospital_doctor SET clockin = '1' WHERE id = 1"
            cursor.execute(sql)
            # 提交修改
            conn.commit()
            # 关闭游标和数据库连接
            cursor.close()
            conn.close()
            return render(request,'doctorclockin.html',{'name' : name})

class DoctorAskForLeave(View):
    def get(self,request):
        doctor = request.session.get('doctor')
        name = doctor.name
        solve = DoctorAffair.objects.filter(name=name)
        ##print(solve[0].solveleave)
        if not solve:
            return render(request,'doctoraskforleave.html',{'name' :name})
        else:
            for i in range(0,len(solve)):
                if solve[i].solveleave == 1:
                    return render(request,'solve.html')
            return render(request,'doctoraskforleave.html',{'name' :name})
    
    def post(self,request):
        leave = request.POST.get('reason','')
        doctor = request.session.get('doctor')
        name = doctor.name
        affair = DoctorAffair.objects.create(name=name,leave=leave,business='',apply='',solveleave=1,solvebusiness=3,solve=3)
        if affair:
            return HttpResponseRedirect('/doctoraskforleave/')

class DoctorBusiness(View):
    def get(self,request):
        doctor = request.session.get('doctor')
        name = doctor.name
        solve = DoctorAffair.objects.filter(name=name)
        if not solve:
            #return render(request,'doctoraskforleave.html',{'name' :name})
            return render(request,'doctor_business1.html',{'name' : name})
        else:
            for i in range(0,len(solve)):
                if solve[i].solvebusiness == 0:
                    return render(request,'solve.html')
            return render(request,'doctor_business1.html',{'name' : name})
    def post(self,request):
        business = request.POST.get('reason','')
        doctor = request.session.get('doctor')
        name = doctor.name
        affair = DoctorAffair.objects.create(name=name,leave='',business=business,apply='',solveleave=3,solvebusiness=0,solve=3)
        if affair:
            return HttpResponseRedirect('/doctorbusiness/')


class DoctorReimbursementRegistration(View):
    def get(self,request):
        doctor = request.session.get('doctor')
        name = doctor.name
        solve = DoctorAffair.objects.filter(name=name)
        if not solve:
            #return render(request,'doctoraskforleave.html',{'name' :name})
            return render(request,'doctor_reimbursementregistration.html',{'name' : name})
        else:
            for i in range(0,len(solve)):
                if solve[i].solve == 2:
                    return render(request,'solve.html')
            return render(request,'doctor_reimbursementregistration.html',{'name' : name})
    def post(self,request):
        apply = request.POST.get('reason','')
        doctor = request.session.get('doctor')
        name = doctor.name
        affair = DoctorAffair.objects.create(name=name,leave='',business='',apply=apply,solveleave=3,solvebusiness=3,solve=2)
        if affair:
            return HttpResponseRedirect('/doctorreimbursementregistration/')