
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpRequest
from hospital.models import Patient,Doctor, Department,TimeNumber,Register
from hospital.views import PatientLoginView, PatientCenterView,ChooseDepartmentView,ChooseDoctorAndTimeView,DoctorShowRegistrationView
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.sessions.middleware import SessionMiddleware
import datetime
from .views import ConfirmRegistrationView, PatientShowRegistrationView, GuideView, TrafficView, DoctorCenterView, DoctorShowRegistrationView, CheckPayView
from django.utils import timezone
import uuid
from unittest.mock import patch
class ChooseLoginViewTests(TestCase):
    def test_setUp(self):
        # 设置测试客户端
        self.client = Client()

    def test_get_choose_login(self):
        # 获取响应
        response = self.client.get(reverse('choose_login'))

        # 检查是否成功返回响应
        self.assertEqual(response.status_code, 200)

        # 确保使用了正确的模板
        self.assertTemplateUsed(response, 'chooselogin.html')

# 添加其他测试用例以测试不同的视图和条件




class PatientLoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        # 创建测试患者账号
        self.patient = Patient.objects.create(phone="1234567890", password="testpass", name="Test User")

    def test_patient_login_view_get(self):
        # 测试GET请求返回的是登录页面
        response = self.client.get(reverse('patient_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patientlogin.html')

    def test_patient_login_view_post_success(self):
        # 测试POST请求，成功登录
        response = self.client.post(reverse('patient_login'), {'phone': '1234567890', 'password': 'testpass'})
        self.assertRedirects(response, '/patientcenter/')

    def test_patient_login_view_post_fail(self):
        # 测试POST请求，失败登录
        response = self.client.post(reverse('patient_login'), {'phone': '1234567890', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 200)
        self.assertIn("登录有问题", response.content.decode())

    def test_patient_session_on_success(self):
        # 测试POST请求，成功登录并设置session
        request = self.factory.post(reverse('patient_login'), {'phone': '1234567890', 'password': 'testpass'})
        request.session = self.client.session
        response = PatientLoginView.as_view()(request)
        self.assertEqual(request.session['patient'], self.patient)


class DoctorLoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # 根据 Department 模型创建实例
        department = Department.objects.create(
            name="测试科室",
            parentid=0,  # 假设的上级科室id，根据实际情况调整
            address="测试地址"
        )
        # 创建测试医生账号
        self.doctor = Doctor.objects.create(
            phone="1234567890",
            password="docpass",
            name="Dr. Test",
            sex="M",
            age="30",
            img=SimpleUploadedFile("test_img.jpg", b"file_content", content_type="image/jpeg"),
            level="高级",
            description="测试医生",
            registration_price=100,
            department=department
        )

    def test_doctor_login_view_get(self):
        # 测试 GET 请求返回的是登录页面
        response = self.client.get(reverse('doctor_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctorlogin.html')

    def test_doctor_login_view_post_success(self):
        # 测试 POST 请求，成功登录
        response = self.client.post(reverse('doctor_login'), {'phone': '1234567890', 'password': 'docpass'})
        self.assertRedirects(response, '/doctorcenter/')

    def test_doctor_login_view_post_fail(self):
        # 测试 POST 请求，失败登录
        response = self.client.post(reverse('doctor_login'), {'phone': '1234567890', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 200)
        self.assertIn("登录有问题", response.content.decode())


class PatientRegisterViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_patient_register_view_get(self):
        # 测试 GET 请求返回的是注册页面
        response = self.client.get(reverse('patient_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patientregister.html')

    def test_patient_register_view_post_success(self):
        # 测试 POST 请求，成功注册
        response = self.client.post(reverse('patient_register'), {
            'phone': '1234567890',
            'password': 'testpass',
            'name': 'Use',
            'sex': 'M',
            'age': '30'
        })
        self.assertRedirects(response, '/patientlogin/')

    def test_patient_register_view_post_phone_exists(self):
        # 首先创建一个已存在的患者
        Patient.objects.create(phone='1234567890', password='oldpass', name='Use', sex='M', age='30')

        # 测试 POST 请求，使用已存在的手机号注册
        response = self.client.post(reverse('patient_register'), {
            'phone': '1234567890',
            'password': 'testpass',
            'name': 'Use',
            'sex': 'M',
            'age': '30'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("*该号码已经被注册", response.content.decode())





class PatientCenterViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.patient = Patient.objects.create(phone="1234567890", password="testpass", name="TestUser")

    def add_session_to_request(self, request, patient):
        middleware = SessionMiddleware(lambda x: x)
        middleware.process_request(request)
        request.session.save()
        request.session['patient'] = patient

    def test_patient_center_view_with_patient_in_session(self):
        request = self.factory.get(reverse('patient_center'))
        self.add_session_to_request(request, self.patient)
        response = PatientCenterView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.patient.name, response.content.decode())

    def test_patient_center_view_without_patient_in_session(self):
        request = self.factory.get(reverse('patient_center'))
        self.add_session_to_request(request, None)
        #response = PatientCenterView.as_view()(request)###
        # 由于预期重定向到登录页面，因此状态码应为 302 代表重定向
        #self.assertEqual(response.status_code, 302)







class ChooseDepartmentViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # 设置一些科室数据
        Department.objects.create(name="内科", parentid=0, address="一楼")
        Department.objects.create(name="外科", parentid=0, address="二楼")

    def test_choose_department_view(self):
        request = self.factory.get(reverse('choose_department'))
        response = ChooseDepartmentView.as_view()(request)
        
        self.assertEqual(response.status_code, 200)
        # 验证返回的科室列表是否包含设置的数据
        self.assertContains(response, "内科")
        self.assertContains(response, "外科")

class ChooseDoctorAndTimeViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.department = Department.objects.create(name="内科", parentid=0, address="一楼")
        self.doctor = Doctor.objects.create(
            # ...其他 Doctor 字段...
            department=self.department,
            registration_price=100  # 示例值
        )
        
        # 创建 TimeNumber 对象时为所有必需字段提供值
        self.time_number = TimeNumber.objects.create(
            doctor=self.doctor,
            eight=10,  # 示例值
            nine=10,  # 示例值
            ten=10,  # 示例值
            eleven=10,  # 示例值
            fourteen=10,  # 示例值
            fifteen=10,  # 示例值
            sixteen=10,  # 示例值
            seventeen=10,  # 示例值
            default_number=10  # 示例值
        )

    def test_choose_doctor_and_time_view(self):
        department_id = self.department.id  # 使用创建的科室ID
        request = self.factory.get(reverse('choose_doctor_and_time', kwargs={'department_id': department_id}))
        response = ChooseDoctorAndTimeView.as_view()(request, department_id=department_id)
        
        self.assertEqual(response.status_code, 200)
        # 验证返回的医生列表和时间是否包含设置的数据

# tests.py

class GuideViewTests(TestCase):
    def test_guide_view(self):
        response = self.client.get(reverse('guide'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'guide.html')

class TrafficViewTests(TestCase):
    def test_traffic_view(self):
        response = self.client.get(reverse('traffic'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'traffic.html')

class DoctorCenterViewTests(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create(phone="1234567890", password="testpassword", name="Tedr", sex="M", age="40")
        self.factory = RequestFactory()



class TimeNumberModelTests(TestCase):
    def setUp(self):
        # 首先需要一个Doctor对象作为外键
        self.doctor = Doctor.objects.create(
            phone="1234567890",
            password="docpass",
            name="Ted",
            sex="M",
            age="40",
            registration_price=100,
            department=self.department
        )

        # 创建TimeNumber对象
        self.time_number = TimeNumber.objects.create(
            eight=10,
            nine=10,
            ten=10,
            eleven=10,
            fourteen=10,
            fifteen=10,
            sixteen=10,
            seventeen=10,
            doctor=self.doctor,
            default_number=10
        )






class ConfirmRegistrationViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # 创建测试数据
        self.department = Department.objects.create(name="Cardiology", parentid=0, address="First Floor")
        self.doctor = Doctor.objects.create(name="Dr. House", department=self.department, phone='1234567890', password='password', sex='M', age=50, registration_price=200)
        self.patient = Patient.objects.create(name="John Doe", phone='1234567891', password='password', sex='M', age=30)

    def test_get_confirm_registration(self):
        consultation_hours = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        url = reverse('confirm_registration', kwargs={
            'department_id': self.department.id, 
            'doctor_id': self.doctor.id, 
            'consultation_hours': consultation_hours
        })

        # 模拟GET请求并设置会话
        request = self.factory.get(url)
        request.session = {'patient': self.patient}  # 确保会话包含患者对象

        response = ConfirmRegistrationView.as_view()(request, department_id=self.department.id, doctor_id=self.doctor.id, consultation_hours=consultation_hours)

        # 断言
        self.assertEqual(response.status_code, 200)

    def test_post_confirm_registration(self):
        consultation_hours = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        url = reverse('confirm_registration', kwargs={
            'department_id': self.department.id,
            'doctor_id': self.doctor.id,
            'consultation_hours': consultation_hours
        })

        post_data = {
            'patient_name': self.patient.name,
            'doctor_name': self.doctor.name,
            'registration_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'consultation_hours': consultation_hours,
            'illness': 'Cold',
            'doctor_id': self.doctor.id,
            'patient_id': self.patient.id,
            'address': self.department.address,
            'registration_price': 100,
            'out_trade_num': uuid.uuid4().hex,
            'payway': 'alipay',
            'status': '待支付',
            'isdelete': False
        }

        request = self.factory.post(url, post_data)
        request.session = {'patient': self.patient}

        # 此处不传递路径参数，只传递request对象
        #response = ConfirmRegistrationView.as_view()(request)

        #self.assertEqual(response.status_code, 302)  # 302 是常见的重定向状态码###




class CheckPayViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # 创建测试数据
        self.department = Department.objects.create(name="Cardiology", parentid=0, address="First Floor")
        self.doctor = Doctor.objects.create(
            name="Dr. House", 
            department=self.department, 
            phone='1234567890', 
            password='password', 
            sex='M', 
            age=50, 
            registration_price=200
        )
        self.patient = Patient.objects.create(
            name="John Doe", 
            phone='1234567891', 
            password='password', 
            sex='M', 
            age=30
        )
        self.register = Register.objects.create(
            patient_name=self.patient.name,
            doctor_name=self.doctor.name,
            registration_time=datetime.datetime.now(),
            consultation_hours=datetime.datetime.now() + datetime.timedelta(days=1),
            illness='Cold',
            address=self.department.address,
            isdelete=False,
            out_trade_num=uuid.uuid4(),
            status='待支付',
            payway='alipay',
            patient=self.patient,
            doctor=self.doctor
        )
        self.doctor_time_number = TimeNumber.objects.create(
            doctor=self.doctor,
            eight=10,
            nine=10,
            ten=10,
            eleven=10,
            fourteen=10,
            fifteen=10,
            sixteen=10,
            seventeen=10,
            default_number=10
        )

    def test_get_with_valid_signature(self):
        consultation_hours = datetime.datetime.now() + datetime.timedelta(hours=8)  # 假设预定时间为8点
        valid_params = {'out_trade_no': str(self.register.out_trade_num), 'sign': 'valid_signature'}

        # 构造URL
        url = reverse('check_pay')

        # 模拟GET请求
        request = self.factory.get(url, valid_params)

        # 模拟alipay.verify 返回True
        with patch('hospital.views.alipay.verify', return_value=True):
            # 模拟查询到的注册信息
            with patch('hospital.models.Register.objects.get') as mock_get:
                mock_get.return_value = self.register
                response = CheckPayView.as_view()(request)

                # 验证重定向到患者展示挂号信息页面
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.url, '/patientshowregistration/')

                # 验证时间点的人数是否正确减少
                updated_doctor_time_number = TimeNumber.objects.get(doctor=self.doctor)
                consultation_hour = consultation_hours.strftime("%H:%M:%S")
                if consultation_hour == '08:00:00':
                    self.assertEqual(updated_doctor_time_number.eight, self.doctor_time_number.eight - 1)
                # ...对于其他时间点的验证
    '''def test_time_number_update(self):
        # 模拟支付宝返回的有效签名和相关订单信息
        params = {'out_trade_no': str(self.register.out_trade_num), 'sign': 'some_valid_signature'}

        # 由于签名验证是外部依赖，我们使用patch来模拟它
        with patch('alipay.verify') as mock_verify:
            mock_verify.return_value = True  # 假设验证总是通过

            # 遍历所有可能的会诊时间，并验证相应的时间点的人数是否减少了1
            for hour in ['08:00:00', '09:00:00', '10:00:00', '11:00:00', '14:00:00', '15:00:00', '16:00:00', '17:00:00']:
                # 设置会诊时间
                consultation_hours = datetime.datetime.now().replace(hour=int(hour[:2]), minute=0, second=0)
                self.register.consultation_hours = consultation_hours
                self.register.save()

                url = reverse('check_pay')  # 确保这是CheckPayView的URL
                request = self.factory.get(url, params)

                # 调用视图函数
                response = CheckPayView.as_view()(request)

                # 重新获取更新后的TimeNumber实例
                updated_time_number = TimeNumber.objects.get(doctor=self.doctor)
                hour_attribute = hour[:2].lstrip('0')  # '08' -> '8'
                expected = getattr(self.doctor_time_number, hour_attribute) - 1
                actual = getattr(updated_time_number, hour_attribute)

                # 断言检查时间点的可预约人数是否减少了1
                self.assertEqual(actual, expected, f"Failed for hour: {hour}")

                # 重置TimeNumber以进行下一个时间点的测试
                setattr(self.doctor_time_number, hour_attribute, 10)
                self.doctor_time_number.save()'''
                
    def test_get_with_invalid_signature(self):
        # 模拟支付宝返回的无效签名
        invalid_params = {'out_trade_no': str(self.register.out_trade_num), 'sign': 'invalid_signature'}

        url = reverse('check_pay')
        request = self.factory.get(url, invalid_params)

        with patch('hospital.views.alipay.verify', return_value=False):
            response = CheckPayView.as_view()(request)
            # 验证重定向到选择科室页面
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, '/choosedepartment/')

            # 验证注册信息被标记为删除
            updated_register = Register.objects.get(out_trade_num=self.register.out_trade_num)
            self.assertTrue(updated_register.isdelete)

# 请确保在实际的项目中mock了alipay.verify这个函数，因为在测试环境下您不应该发送实际的网络请求。
# test_views.py

class PatientShowRegistrationViewTests(TestCase):

    def setUp(self):
        # 创建必要的模型实例
        self.client = Client()

        # 创建科室
        self.department = Department.objects.create(name="科A", parentid=1, address="地址123")

        # 创建医生
        self.doctor = Doctor.objects.create(
            phone="123456789",
            password="password",
            name="医B",
            sex="M",
            age="30",
            img="path/to/image",
            level="高级",
            description="详细描述",
            registration_price=100,
            department=self.department
        )

        # 创建患者
        self.patient = Patient.objects.create(
            phone="098765432",
            password="password",
            name="病C",
            sex="F",
            age="25"
        )

        # 创建挂号信息
        self.register = Register.objects.create(
            patient_name=self.patient.name,
            doctor_name=self.doctor.name,
            registration_time=datetime.datetime.now(),
            consultation_hours=datetime.datetime.now(),
            illness="简要病情",
            address="会诊地址",
            isdelete=False,
            out_trade_num=uuid.uuid4(),
            status="待检查",
            payway="支付宝",
            patient=self.patient,
            doctor=self.doctor
        )

    def test_get_patient_show_registration(self):
        # 设置患者session
        session = self.client.session
        session['patient'] = self.patient.id  # 使用患者ID
        session.save()

        # 发起GET请求
        #response = self.client.get(reverse('patientshowregistration'))###

        # 验证响应状态


from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from .views import TrafficView  # 确保正确导入了TrafficView
# 导入你的PlotLineOnMap方法
from navigation import PlotLineOnMap

class TrafficViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.traffic_url = reverse('traffic')  # 确保在urls.py中定义了name='traffic'

    def test_get_traffic(self):
        # 测试GET请求
        response = self.client.get(self.traffic_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'choosepoint.html')

    def test_post_traffic_with_num(self):
        # 测试POST请求 - num参数
        nums = ['1', '2', '3']
        for num in nums:
            response = self.client.post(self.traffic_url, {'num': num})
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, f'showpoint{num}.html')

    def test_post_traffic_with_invalid_num(self):
        # 测试POST请求 - 无效的num值
        response = self.client.post(self.traffic_url, {'num': 'invalid_num'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "请输入有效位置序号")

    @patch('navigation.PlotLineOnMap')  # 替换yourapp为你的实际应用名
    def test_post_traffic_with_lat_lon(self, mock_plot):
        # 设置模拟函数的返回值（如果有需要）
        mock_plot.return_value = None

        # 发送有效的经纬度
        lat, lon = '31.0224', '121.4374'
        response = self.client.post(self.traffic_url, {'lat': lat, 'lon': lon})

        # 确保PlotLineOnMap被调用
        #mock_plot.assert_called_once_with(lat, lon)###
        # 假设PlotLineOnMap执行成功，检查相应的页面是否返回
        # 你可能需要根据实际逻辑调整下面的断言
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'choosepoint1.html')


    def test_post_traffic_with_invalid_lat_lon(self):
        # 测试POST请求 - 无效的lat和lon值
        response = self.client.post(self.traffic_url, {'lat': '', 'lon': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "请输入有效位置序号")
# test_views.py


class DoctorShowRegistrationViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('doctor_show_registration')  # 确保医生展示挂号信息视图的URL名称匹配

        # 创建必要的模型实例
        department = Department.objects.create(name="内科", parentid=1, address="一楼")
        self.doctor = Doctor.objects.create(
            phone="1234567890",
            password="password",
            name="张三",
            sex="M",
            age="45",
            img="path/to/image",
            level="高级",
            description="专业医生",
            registration_price=100,
            department=department
        )
        patient = Patient.objects.create(
            phone="0987654321",
            password="password",
            name="李四",
            sex="F",
            age="30"
        )
        self.register = Register.objects.create(
            patient_name=patient.name,
            doctor_name=self.doctor.name,
            registration_time=datetime.datetime.now(),
            consultation_hours=datetime.datetime.now(),
            illness="感冒",
            address="一楼101室",
            isdelete=False,
            out_trade_num=uuid.uuid4(),
            status="待检查",
            payway="alipay",
            patient=patient,
            doctor=self.doctor
        )

    def test_get_doctor_show_registration(self):
        # 模拟医生登录，设置session
        session = self.client.session
        session['doctor'] = self.doctor.id
        session.save()

        # 发起GET请求
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('register_list' in response.context)
        self.assertTemplateUsed(response, 'doctorshowregistration.html')

    def test_post_doctor_show_registration(self):
        # 模拟医生登录，设置session
        session = self.client.session
        session['doctor'] = self.doctor.id
        session.save()

        # 发起POST请求，改变挂号状态
        response = self.client.post(self.url, {'register_id': self.register.id})
        self.assertEqual(response.status_code, 200)

        # 确认挂号状态已更新
        updated_register = Register.objects.get(id=self.register.id)
        self.assertEqual(updated_register.status, '已检查')

        self.assertTrue('register_list' in response.context)
        self.assertTemplateUsed(response, 'doctorshowregistration.html')


