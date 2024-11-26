from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("payment/", views.PaymentView.as_view(), name="payment"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("treatment/", views.TreatmentView.as_view(), name="treatment"),
    path("coverage-policy/", views.CoveragePolicyView.as_view(), name="coverage_policy"),
    path("insurance/", views.InsuranceView.as_view(), name="insurance"),
    path("patient/", views.PatientView.as_view(), name="patient"),
    path("appointment/", views.AppointmentView.as_view(), name="appointment"),
    path("diseases/", views.DiseasesView.as_view(), name="diseases"),
    path("medical-record/", views.MedicalRecordView.as_view(), name="medical_record"),
    path("medicine/", views.MedicineView.as_view(), name="medicine"),
    path("medicine-record/", views.MedicineRecordView.as_view(), name="medicine_record"),
    path("doctor/", views.DoctorView.as_view(), name="doctor"),
    path("dosage/", views.DosageView.as_view(), name="dosage"),
    path("availability/", views.AvailabilityView.as_view(), name="availability"),
]
