from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path('appointments/', views.AppointmentListView.as_view(),
         name='appointment_list'),
    path('availabilities/', views.AvailabilityListView.as_view(),
         name='availability_list'),
    path('coverage_policies/', views.CoveragePolicyListView.as_view(),
         name='coverage_policy_list'),
    path('insurances/', views.InsuranceListView.as_view(),
         name='insurance_list'),
    path('doctors/', views.DoctorListView.as_view(), name='doctor_list'),
    path('payments/', views.PaymentListView.as_view(), name='payment_list'),
    path('diseases/', views.DiseaseListView.as_view(), name='disease_list'),
    path('treatments/', views.TreatmentListView.as_view(),
         name='treatment_list'),
    path('medicines/', views.MedicineListView.as_view(), name='medicine_list'),
    path('dosages/', views.DosageListView.as_view(), name='dosage_list'),
    path('patients/', views.PatientListView.as_view(), name='patient_list'),
    path('medical_records/', views.MedicalRecordListView.as_view(),
         name='medical_record_list'),
    path('medicine_records/', views.MedicineRecordListView.as_view(),
         name='medicine_record_list'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('add_medical_record/', views.add_medical_record,
         name='add_medical_record'),
    path('add_medicine_record/', views.add_medicine_record,
         name='add_medicine_record'),
    path('add_medicine/', views.add_medicine, name='add_medicine'),
    path('add_dosage/', views.add_dosage, name='add_dosage'),
    path('add_coverage_policy/', views.add_coverage_policy,
         name='add_coverage_policy'),
    path('add_insurance/', views.add_insurance, name='add_insurance'),
    path('add_payment/', views.add_payment, name='add_payment'),
    path('add_disease/', views.add_disease, name='add_disease'),
    path('add_treatment/', views.add_treatment, name='add_treatment'),
    path('add_appointment/', views.add_appointment, name='add_appointment'),
    path('add_availability/', views.add_availability, name='add_availability'),
    path('appointments/delete/<str:appointment_id>/', views.delete_appointment,
         name='delete_appointment'),
    path('delete_coverage_policy/<str:policy_id>/',
         views.delete_coverage_policy, name='delete_coverage_policy'),
    path('delete_doctor/<str:doctor_id>/', views.delete_doctor,
         name='delete_doctor'),
    path('delete_medical_record/<str:medical_record_id>/',
         views.delete_medical_record, name='delete_medical_record'),
    path('delete_medicine_record/<str:medical_record_id>/',
         views.delete_medicine_record, name='delete_medicine_record'),
    path('delete_insurance/<str:insurance_id>/', views.delete_insurance,
         name='delete_insurance'),
    path('delete_payment/<str:payment_id>/', views.delete_payment,
         name='delete_payment'),
    path('delete_disease/<str:disease_id>/', views.delete_disease,
         name='delete_disease'),
    path('delete_treatment/<str:treatment_id>/', views.delete_treatment,
         name='delete_treatment'),
    path('delete_medicine/<str:medicine_id>/', views.delete_medicine,
         name='delete_medicine'),
    path('delete_dosage/<str:dosage_id>/', views.delete_dosage,
         name='delete_dosage'),
    path('delete_patient/<str:patient_id>/', views.delete_patient,
         name='delete_patient'),
    path('delete_availability/<str:availability_id>/',
         views.delete_availability, name='delete_availability'),
    path('edit_appointment/<str:appointment_id>/', views.edit_appointment,
         name='edit_appointment'),
    path('edit_availability/<str:availability_id>/', views.edit_availability,
         name='edit_availability'),
    path('edit_medicine_record/<str:medicine_record_id>/',
         views.edit_medicine_record, name='edit_medicine_record'),
    path('edit_medical_record/<str:medical_record_id>/',
         views.edit_medical_record, name='edit_medical_record'),
    path('edit_doctor/<str:doctor_id>/', views.edit_doctor,
         name='edit_doctor'),
    path('edit_patient/<str:patient_id>/', views.edit_patient,
         name='edit_patient'),
    path('edit_dosage/<str:dosage_id>/', views.edit_dosage,
         name='edit_dosage'),
    path('edit_medicine/<str:medicine_id>/', views.edit_medicine,
         name='edit_medicine'),
    path('edit_treatment/<str:treatment_id>/', views.edit_treatment,
         name='edit_treatment'),
    path('edit_disease/<str:disease_id>/', views.edit_disease,
         name='edit_disease'),
    path('edit_payment/<str:payment_id>/', views.edit_payment,
         name='edit_payment'),
    path('edit_insurance/<str:insurance_id>/', views.edit_insurance,
         name='edit_insurance'),
    path('edit_coverage_policy/<str:policy_id>/', views.edit_coverage_policy,
         name='edit_coverage_policy'),
    path('doctor/<str:doctor_id>/doctor_timetable/', views.doctor_timetable,
         name='doctor_timetable'),
]
