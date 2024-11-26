from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path('appointments/', views.AppointmentListView.as_view(),
         name='appointment_list'),
    path('availabilities/', views.AvailabilityListView.as_view(),
         name='availability_list'),
    path('coverage_policies/', views.CoveragePolicyListView.as_view(), name='coverage_policy_list'),
    path('insurances/', views.InsuranceListView.as_view(), name='insurance_list'),
    path('doctors/', views.DoctorListView.as_view(), name='doctor_list'),
    path('payments/', views.PaymentListView.as_view(), name='payment_list'),
    path('diseases/', views.DiseaseListView.as_view(), name='disease_list'),
    path('treatments/', views.TreatmentListView.as_view(), name='treatment_list'),
    path('medicines/', views.MedicineListView.as_view(), name='medicine_list'),
    path('dosages/', views.DosageListView.as_view(), name='dosage_list'),
    path('patients/', views.PatientListView.as_view(), name='patient_list'),
    path('medical_records/', views.MedicalRecordListView.as_view(), name='medical_record_list'),
    path('medicine_records/', views.MedicineRecordListView.as_view(), name='medicine_record_list'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('add_medical_record/', views.add_medical_record, name='add_medical_record'),
    path('add_medicine_record/', views.add_medicine_record, name='add_medicine_record'),
    path('add_medicine/', views.add_medicine, name='add_medicine'),
    path('add_dosage/', views.add_dosage, name='add_dosage'),
    path('add_coverage_policy/', views.add_coverage_policy, name='add_coverage_policy'),
    path('add_insurance/', views.add_insurance, name='add_insurance'),
    path('add_payment/', views.add_payment, name='add_payment'),
    path('add_disease/', views.add_disease, name='add_disease'),
    path('add_treatment/', views.add_treatment, name='add_treatment'),
    path('add_appointment/', views.add_appointment, name='add_appointment'),
    path('add_availability/', views.add_availability, name='add_availability'),


]
