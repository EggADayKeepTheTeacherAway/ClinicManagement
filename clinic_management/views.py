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
        patient = Patient.objects.all()
        doctor = Doctor.objects.all()
        appointments = Appointment.objects.select_related('PatientID',
                                                          'DoctorID').all()
        insurances = Insurance.objects.select_related('PatientID').all()
        coverage_policies = CoveragePolicy.objects.select_related(
            'InsuranceID').all()
        diseases = Diseases.objects.all()
        medical_records = MedicalRecord.objects.select_related('PatientID',
                                                               'DoctorID',
                                                               'DiseaseID').all()
        payments = Payment.objects.select_related('MedicalRecordID').all()
        medicines = Medicine.objects.all()
        medicine_records = MedicineRecord.objects.select_related(
            'MedicalRecordID', 'MedicationID', 'DosageID').all()
        treatments = Treatment.objects.all()  # Fetch treatments
        dosages = Dosage.objects.all()
        availabilities = Availability.objects.select_related('DoctorID').all()

        # Create a mapping for easy access
        insurance_mapping = {insurance.PatientID_id: insurance for insurance in
                             insurances}
        payment_mapping = {record.MedicalRecordID_id: record for record in
                           payments}
        coverage_policy_mapping = {policy.InsuranceID_id: policy for policy in
                                   coverage_policies}
        disease_mapping = {disease.DiseaseID: disease for disease in diseases}
        dosage_mapping = {dosage.DosageID: dosage for dosage in dosages}
        treatment_mapping = {treatment.TreatmentID: treatment for treatment in
                             treatments}

        merged_data = []
        for appointment in appointments:
            patient = appointment.PatientID
            doctor = appointment.DoctorID

            # Get all medical records for the patient
            medical_records_for_patient = [
                record for record in medical_records if
                record.PatientID_id == patient.PatientID
            ]

            for medical_record in medical_records_for_patient:
                insurance = insurance_mapping.get(patient.PatientID, None)
                coverage_policy = coverage_policy_mapping.get(
                    insurance.InsuranceID) if insurance else None
                disease = disease_mapping.get(medical_record.DiseaseID_id,
                                              None)
                payment = payment_mapping.get(medical_record.MedicalRecordID,
                                              None)

                # Treatment for the specific medical record
                treatment = treatment_mapping.get(
                    disease.TreatmentID_id) if disease else None

                # Medicine details and dosage
                medicine_records_for_appointment = [
                    record for record in medicine_records if
                    record.MedicalRecordID_id == medical_record.MedicalRecordID
                ]

                medicines_for_appointment = []
                medicine_dosages = []

                for medicine_record in medicine_records_for_appointment:
                    dosage = dosage_mapping.get(medicine_record.DosageID_id,
                                                None)
                    medicine_obj = medicine_record.MedicationID
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

                # Append data for each medical record
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

                    'medical_record_id': medical_record.MedicalRecordID,
                    'medical_record_visit_reason': medical_record.VisitReason,
                    'medical_record_summary': medical_record.Summary,
                    'medical_record_status': medical_record.Status,
                    'medical_record_date_visit': medical_record.DateVisit,

                    'disease_id': disease.DiseaseID if disease else "N/A",
                    'disease_name': disease.Name if disease else "N/A",
                    'disease_description': disease.Description if disease else "N/A",

                    'medicines_for_appointment': medicines_for_appointment if medicines_for_appointment else "N/A",
                    'medicine_dosages': medicine_dosages if medicine_dosages else "N/A",

                    'treatment_id': treatment.TreatmentID if treatment else "N/A",
                    'treatment_type': treatment.Type if treatment else "N/A",
                    'treatment_base_charge': treatment.BaseCharge if treatment else "N/A",

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


# Views for each table
class CoveragePolicyListView(generic.ListView):
    model = CoveragePolicy
    template_name = 'coverage_policy_list.html'
    context_object_name = 'coverage_policies'


class InsuranceListView(generic.ListView):
    model = Insurance
    template_name = 'insurance_list.html'
    context_object_name = 'insurances'


class PaymentListView(generic.ListView):
    model = Payment
    template_name = 'payment_list.html'
    context_object_name = 'payments'


class DiseaseListView(generic.ListView):
    model = Diseases
    template_name = 'disease_list.html'
    context_object_name = 'diseases'


class TreatmentListView(generic.ListView):
    model = Treatment
    template_name = 'treatment_list.html'
    context_object_name = 'treatments'


class MedicineListView(generic.ListView):
    model = Medicine
    template_name = 'medicine_list.html'
    context_object_name = 'medicines'


class DosageListView(generic.ListView):
    model = Dosage
    template_name = 'dosage_list.html'
    context_object_name = 'dosages'


class PatientListView(generic.ListView):
    model = Patient
    template_name = 'patient_list.html'
    context_object_name = 'patients'


class DoctorListView(generic.ListView):
    model = Doctor
    template_name = 'doctor_list.html'
    context_object_name = 'doctors'


class MedicalRecordListView(generic.ListView):
    model = MedicalRecord
    template_name = 'medical_record_list.html'
    context_object_name = 'medical_records'


class MedicineRecordListView(generic.ListView):
    model = MedicineRecord
    template_name = 'medicine_record_list.html'
    context_object_name = 'medicine_records'


class AppointmentListView(generic.ListView):
    model = Appointment
    template_name = 'appointment_list.html'
    context_object_name = 'appointments'


class AvailabilityListView(generic.ListView):
    model = Availability
    template_name = 'availability_list.html'
    context_object_name = 'availabilities'
