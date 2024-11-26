from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from clinic_management.models import *


# Create your views here.

class HomePageView(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Prefetch related fixtures to minimize queries
        appointments = Appointment.objects.select_related('PatientID', 'DoctorID').all()
        insurances = Insurance.objects.select_related('PatientID').all()
        coverage_policies = CoveragePolicy.objects.select_related('InsuranceID').all()
        medical_records = MedicalRecord.objects.select_related('PatientID', 'DoctorID', 'DiseaseID').all()
        payments = Payment.objects.select_related('MedicalRecordID').all()
        medicines = Medicine.objects.all()
        medicine_records = MedicineRecord.objects.select_related('MedicalRecordID', 'MedicationID', 'DosageID').all()
        treatments = Treatment.objects.all()  # Fetch treatments
        diseases = Diseases.objects.all()
        dosages = Dosage.objects.all()
        availabilities = Availability.objects.select_related('DoctorID').all()

        # Create a mapping for easy access
        insurance_mapping = {insurance.PatientID_id: insurance for insurance in insurances}
        medical_record_mapping = {record.MedicalRecordID: record for record in medical_records}
        payment_mapping = {record.MedicalRecordID_id: record for record in payments}
        coverage_policy_mapping = {policy.InsuranceID_id: policy for policy in coverage_policies}
        disease_mapping = {disease.DiseaseID: disease for disease in diseases}
        dosage_mapping = {dosage.DosageID: dosage for dosage in dosages}
        treatment_mapping = {treatment.TreatmentID: treatment for treatment in treatments}

        merged_data = []
        for appointment in appointments:
            patient = appointment.PatientID
            doctor = appointment.DoctorID
            insurance = insurance_mapping.get(patient.PatientID)
            medical_record = medical_record_mapping.get(patient.PatientID)
            coverage_policy = coverage_policy_mapping.get(insurance.InsuranceID) if insurance else None
            disease = disease_mapping.get(medical_record.DiseaseID) if medical_record else None
            payment = payment_mapping.get(medical_record.MedicalRecordID) if medical_record else None

            treatment_for_appointment = treatment_mapping.get(medical_record.TreatmentID) if medical_record else None

            # Medicine details and dosage (same as your previous logic)
            medicine_records_for_appointment = medicine_records.filter(MedicalRecordID=medical_record) if medical_record else []
            medicine_dosages = []
            medicines_for_appointment = []

            for medicine_record in medicine_records_for_appointment:
                dosage = dosage_mapping.get(medicine_record.DosageID)
                medicine_dosages.append({
                    'DosageID': dosage.DosageID if dosage else "N/A",
                    'MinWeight': dosage.MinWeight if dosage else "N/A",
                    'MaxWeight': dosage.MaxWeight if dosage else "N/A",
                    'MinAge': dosage.MinAge if dosage else "N/A",
                    'MaxAge': dosage.MaxAge if dosage else "N/A",
                    'RecommendDosage': dosage.RecommendDosage if dosage else "N/A",
                    'Units': dosage.Units if dosage else "N/A",
                    'Notes': dosage.Notes if dosage else "N/A"
                })

                medicine_obj = medicine_record.MedicationID
                medicines_for_appointment.append({
                    'MedicineRecordID': medicine_record.MedicineRecordID,
                    'MedicineID': medicine_obj.MedicationID,
                    'MedicineName': medicine_obj.Name,
                    'MedicineBrand': medicine_obj.Brand,
                    'MedicineInstructions': medicine_obj.Instructions,
                    'MedicineDefaultDosage': medicine_obj.DefaultDosage,
                    'MedicinePrice': medicine_obj.Price,
                    'Quantity': medicine_record.Quantity,
                    'Cost': medicine_record.Cost
                })

            merged_data.append({
                'patient_id': patient.PatientID,
                'patient_name': patient.Name,
                'patient_phone': patient.Phone,
                'patient_email': patient.Email,
                'patient_birthdate': patient.Birthdate,
                'patient_weight': patient.Weight,
                'patient_height': patient.Height,
                'patient_emergency': patient.EmergencyContact,

                'doctor_id': doctor.DoctorID,
                'doctor_name': doctor.Name,
                'doctor_phone': doctor.Phone,
                'doctor_email': doctor.Email,
                'doctor_birthdate': doctor.Birthdate,
                'doctor_specialization': doctor.Specialization,

                'appointment_id': appointment.AppointmentID,
                'appointment_date': appointment.Date,
                'appointment_start_time': appointment.StartTime,
                'appointment_end_time': appointment.EndTime,

                'insurance_id': insurance.InsuranceID if insurance else "No insurance",
                'insurance_provider': insurance.Provider if insurance else "No insurance",
                'insurance_coverage_amount': insurance.CoverageAmount if insurance else "N/A",
                'insurance_expire_date': insurance.ExpireDate if insurance else "N/A",
                'insurance_type': insurance.Type if insurance else "N/A",

                'coverage_policy_id': coverage_policy.PolicyID if coverage_policy else "N/A",
                'coverage_percentage': coverage_policy.CoveragePercentage if coverage_policy else "N/A",
                'max_coverage_amount': coverage_policy.MaxCoverageAmount if coverage_policy else "N/A",

                'medical_record_id': medical_record.MedicalRecordID if medical_record else "N/A",
                'medical_record_visit_reason': medical_record.VisitReason if medical_record else "N/A",
                'medical_record_summary': medical_record.Summary if medical_record else "N/A",
                'medical_record_status': medical_record.Status if medical_record else "N/A",
                'medical_record_date_visit': medical_record.DateVisit if medical_record else "N/A",

                'disease_id': disease.DiseaseID if disease else "N/A",
                'disease_name': disease.Name if disease else "N/A",
                'disease_description': disease.Description if disease else "N/A",

                'medicines_for_appointment': medicines_for_appointment if medicines_for_appointment else "N/A",
                'medicine_dosages': medicine_dosages if medicine_dosages else "N/A",

                'treatment_id': treatment_for_appointment.TreatmentID if treatment_for_appointment else "N/A",
                'treatment_type': treatment_for_appointment.Type if treatment_for_appointment else "N/A",
                'treatment_base_charge': treatment_for_appointment.BaseCharge if treatment_for_appointment else "N/A",

                'payment_id': payment.PaymentID if payment else "N/A",
                'payment_status': payment.Status if payment else "N/A",
                'payment_base_charge': payment.BaseCharge if payment else "N/A",
                'payment_medicine_cost': payment.MedicineCost if payment else "N/A",
                'payment_insurance_discount': payment.InsuranceDiscount if payment else "N/A",
                'payment_total_cost': payment.TotalCost if payment else "N/A",
                'payment_date_paid': payment.DatePaid if payment else "N/A",
            })

        context['merged_data'] = merged_data
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


class LoginView(generic.TemplateView):
    template_name = "login.html"
