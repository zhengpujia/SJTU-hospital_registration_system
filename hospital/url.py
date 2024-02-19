#coding = utf-8
from django.urls import path
from .views import *
from .views import ChooseDepartmentView,ChooseDoctorAndTimeView,ConfirmRegistrationView

urlpatterns=[
    path('', ChooseLoginView.as_view(), name='choose_login'),
    path('patientlogin/', PatientLoginView.as_view(), name='patient_login'),
    path('doctorlogin/', DoctorLoginView.as_view(), name='doctor_login'),
    path('patientregister/', PatientRegisterView.as_view(), name='patient_register'),

    path('patientcenter/', PatientCenterView.as_view(), name='patient_center'),
    path('choosedepartment/', ChooseDepartmentView.as_view(), name='choose_department'),
    path('choosedoctorandtime/<int:department_id>/', ChooseDoctorAndTimeView.as_view(), name='choose_doctor_and_time'),
    path('confirmregistration/<int:department_id>/<int:doctor_id>/<str:consultation_hours>', ConfirmRegistrationView.as_view(), name='confirm_registration'),
    path('confirmregistration/',ConfirmRegistrationView.as_view(), name='confirm_registration'),
    path('checkpay/', CheckPayView.as_view(), name='check_pay'),
    path('patientshowregistration/',PatientShowRegistrationView.as_view(),name='patientshowregistration'),
    path('guide/',GuideView.as_view(),name='guide'),
    path('traffic/',TrafficView.as_view(),name='traffic'),
    path('doctorcenter/',DoctorCenterView.as_view(),name='doctorcenter/'),
    path('doctorshowregistration/', DoctorShowRegistrationView.as_view(), name='doctor_show_registration'),
    path('doctorsignin/', DoctorSigninView.as_view()),
    path('doctoraskforleave/',DoctorAskForLeave.as_view()),
    path('doctorbusiness/',DoctorBusiness.as_view()),
    path('doctorreimbursementregistration/',DoctorReimbursementRegistration.as_view()),
    path('search/',search),
    path('solve/',DoctorAskForLeave.as_view()),
]