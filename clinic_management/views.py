from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic


# Create your views here.

class HomePageView(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PaymentView(generic.TemplateView):
    template_name = "payment.html"


class TreatmentView(generic.TemplateView):
    template_name = "treatment.html"


class CoveragePolicyView(generic.TemplateView):
    template_name = "coverage_policy.html"


class InsuranceView(generic.TemplateView):
    template_name = "insurance.html"


class PatientView(generic.TemplateView):
    template_name = "patient.html"


class AppointmentView(generic.TemplateView):
    template_name = "appointment.html"


class DiseasesView(generic.TemplateView):
    template_name = "diseases.html"


class MedicalRecordView(generic.TemplateView):
    template_name = "medical_record.html"


class MedicineView(generic.TemplateView):
    template_name = "medicine.html"


class MedicineRecordView(generic.TemplateView):
    template_name = "medicine_record.html"


class DoctorView(generic.TemplateView):
    template_name = "doctor.html"


class DosageView(generic.TemplateView):
    template_name = "dosage.html"


class AvailabilityView(generic.TemplateView):
    template_name = "availability.html"
