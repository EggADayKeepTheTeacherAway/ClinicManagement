from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path('coverage_policies/', views.CoveragePolicyListView.as_view(),
         name='coverage_policy_list'),
    path('insurances/', views.InsuranceListView.as_view(),
         name='insurance_list'),
    path('payments/', views.PaymentListView.as_view(), name='payment_list'),
    path('diseases/', views.DiseaseListView.as_view(), name='disease_list'),
    path('treatments/', views.TreatmentListView.as_view(),
         name='treatment_list'),
    path('medicines/', views.MedicineListView.as_view(), name='medicine_list'),
    path('dosages/', views.DosageListView.as_view(), name='dosage_list'),
    path('patients/', views.PatientListView.as_view(), name='patient_list'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('doctors/', views.DoctorListView.as_view(), name='doctor_list'),
    path('medical_records/', views.MedicalRecordListView.as_view(),
         name='medical_record_list'),
    path('medicine_records/', views.MedicineRecordListView.as_view(),
         name='medicine_record_list'),
    path('appointments/', views.AppointmentListView.as_view(),
         name='appointment_list'),
    path('availabilities/', views.AvailabilityListView.as_view(),
         name='availability_list'),
]
