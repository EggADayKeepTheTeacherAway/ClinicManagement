from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from clinic_management.models import *


class HomePageView(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
                treatment = treatment_mapping.get(
                    disease.TreatmentID_id) if disease else None
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


class CoveragePolicyListView(generic.ListView):
    model = CoveragePolicy
    template_name = 'coverage_policy_list.html'
    context_object_name = 'coverage_policies'


def add_coverage_policy(request):
    if request.method == 'POST':
        insurance_id = request.POST.get('InsuranceID').strip()
        treatment_id = request.POST.get('TreatmentID').strip()
        coverage_percentage = request.POST.get('CoveragePercentage')
        max_coverage_amount = request.POST.get('MaxCoverageAmount')

        coverage_policy = CoveragePolicy(
            InsuranceID_id=insurance_id,
            TreatmentID_id=treatment_id,
            CoveragePercentage=coverage_percentage,
            MaxCoverageAmount=max_coverage_amount
        )
        coverage_policy.save()

        return redirect('coverage_policy_list')

    fields = [
        ('InsuranceID', 'Insurance ID'),
        ('TreatmentID', 'Treatment ID'),
        ('CoveragePercentage', 'Coverage Percentage'),
        ('MaxCoverageAmount', 'Max Coverage Amount')
    ]
    input_types = {
        'InsuranceID': 'text',
        'TreatmentID': 'text',
        'CoveragePercentage': 'number',
        'MaxCoverageAmount': 'number'
    }

    context = {
        'model_name': 'CoveragePolicy',
        'add_url_name': 'add_coverage_policy',
        'fields': fields,
        'input_types': input_types
    }

    return render(request, 'insert_data/add_data.html', context)


def delete_coverage_policy(request, policy_id):
    policy = get_object_or_404(CoveragePolicy, PolicyID=policy_id)
    if request.method == 'POST':
        policy.delete()
        return redirect('coverage_policy_list')


def edit_coverage_policy(request, policy_id):
    coverage_policy = get_object_or_404(CoveragePolicy, PolicyID=policy_id)

    fields = [
        ('InsuranceID', 'Insurance ID'),
        ('TreatmentID', 'Treatment ID'),
        ('CoveragePercentage', 'Coverage Percentage'),
        ('MaxCoverageAmount', 'Max Coverage Amount')
    ]

    input_types = {
        'InsuranceID': 'text',
        'TreatmentID': 'text',
        'CoveragePercentage': 'number',
        'MaxCoverageAmount': 'number'
    }

    if request.method == 'POST':
        coverage_policy.InsuranceID_id = request.POST['InsuranceID'].strip()
        coverage_policy.TreatmentID_id = request.POST['TreatmentID'].strip()
        coverage_policy.CoveragePercentage = request.POST['CoveragePercentage']
        coverage_policy.MaxCoverageAmount = request.POST['MaxCoverageAmount']
        coverage_policy.save()
        return redirect('coverage_policy_list')

    context = {
        'model_name': 'CoveragePolicy',
        'fields': fields,
        'input_types': input_types,
        'object': coverage_policy,  # This is the object to edit
        'object_model_name': 'coverage_policy_list'
    }

    return render(request, 'edit_data/edit_data.html', context)


class InsuranceListView(generic.ListView):
    model = Insurance
    template_name = 'insurance_list.html'
    context_object_name = 'insurances'


def add_insurance(request):
    if request.method == 'POST':
        patient_id = request.POST.get('PatientID').strip()
        provider = request.POST.get('Provider').strip()
        coverage_amount = request.POST.get('CoverageAmount')
        expire_date = request.POST.get('ExpireDate')
        insurance_type = request.POST.get('Type').strip()

        insurance = Insurance(
            PatientID_id=patient_id,
            Provider=provider,
            CoverageAmount=coverage_amount,
            ExpireDate=expire_date,
            Type=insurance_type
        )
        insurance.save()

        return redirect('insurance_list')

    fields = [
        ('PatientID', 'Patient ID'),
        ('Provider', 'Provider'),
        ('CoverageAmount', 'Coverage Amount'),
        ('ExpireDate', 'Expire Date'),
        ('Type', 'Type')
    ]
    input_types = {
        'PatientID': 'text',
        'Provider': 'text',
        'CoverageAmount': 'number',
        'ExpireDate': 'date',
        'Type': 'text'
    }

    context = {
        'model_name': 'Insurance',
        'add_url_name': 'add_insurance',
        'fields': fields,
        'input_types': input_types
    }

    return render(request, 'insert_data/add_data.html', context)


def delete_insurance(request, insurance_id):
    insurance = get_object_or_404(Insurance, InsuranceID=insurance_id)
    if request.method == 'POST':
        insurance.delete()
        return redirect('insurance_list')


def edit_insurance(request, insurance_id):
    insurance = get_object_or_404(Insurance, InsuranceID=insurance_id)

    fields = [
        ('PatientID', 'Patient ID'),
        ('Provider', 'Provider'),
        ('CoverageAmount', 'Coverage Amount'),
        ('ExpireDate', 'Expire Date'),
        ('Type', 'Type')
    ]

    input_types = {
        'PatientID': 'text',
        'Provider': 'text',
        'CoverageAmount': 'number',
        'ExpireDate': 'date',
        'Type': 'text'
    }

    if request.method == 'POST':
        insurance.PatientID_id = request.POST['PatientID'].strip()
        insurance.Provider = request.POST['Provider'].strip()
        insurance.CoverageAmount = request.POST['CoverageAmount']
        insurance.ExpireDate = request.POST['ExpireDate']
        insurance.Type = request.POST['Type'].strip()
        insurance.save()
        return redirect('insurance_list')

    context = {
        'model_name': 'Insurance',
        'fields': fields,
        'input_types': input_types,
        'object': insurance,
        'object_model_name': 'insurance_list'
    }

    return render(request, 'edit_data/edit_data.html', context)


class PaymentListView(generic.ListView):
    model = Payment
    template_name = 'payment_list.html'
    context_object_name = 'payments'


def add_payment(request):
    if request.method == 'POST':
        medical_record_id = request.POST.get('MedicalRecordID').strip()
        insurance_id = request.POST.get('InsuranceID').strip()
        base_charge = request.POST.get('BaseCharge')
        medicine_cost = request.POST.get('MedicineCost')
        insurance_discount = request.POST.get('InsuranceDiscount')
        total_cost = request.POST.get('TotalCost')
        date_paid = request.POST.get('DatePaid')
        status = request.POST.get('Status').strip()

        payment = Payment(
            MedicalRecordID_id=medical_record_id,
            InsuranceID_id=insurance_id,
            BaseCharge=base_charge,
            MedicineCost=medicine_cost,
            InsuranceDiscount=insurance_discount,
            TotalCost=total_cost,
            DatePaid=date_paid,
            Status=status
        )
        payment.save()

        return redirect('payment_list')

    fields = [
        ('MedicalRecordID', 'Medical Record ID'),
        ('InsuranceID', 'Insurance ID'),
        ('BaseCharge', 'Base Charge'),
        ('MedicineCost', 'Medicine Cost'),
        ('InsuranceDiscount', 'Insurance Discount'),
        ('TotalCost', 'Total Cost'),
        ('DatePaid', 'Date Paid'),
        ('Status', 'Status')
    ]
    input_types = {
        'MedicalRecordID': 'text',
        'InsuranceID': 'text',
        'BaseCharge': 'number',
        'MedicineCost': 'number',
        'InsuranceDiscount': 'number',
        'TotalCost': 'number',
        'DatePaid': 'date',
        'Status': 'text'
    }

    context = {
        'model_name': 'Payment',
        'add_url_name': 'add_payment',
        'fields': fields,
        'input_types': input_types
    }

    return render(request, 'insert_data/add_data.html', context)


def edit_payment(request, payment_id):
    payment = get_object_or_404(Payment, PaymentID=payment_id)

    fields = [
        ('MedicalRecordID', 'Medical Record ID'),
        ('InsuranceID', 'Insurance ID'),
        ('BaseCharge', 'Base Charge'),
        ('MedicineCost', 'Medicine Cost'),
        ('InsuranceDiscount', 'Insurance Discount'),
        ('TotalCost', 'Total Cost'),
        ('DatePaid', 'Date Paid'),
        ('Status', 'Status')
    ]

    input_types = {
        'MedicalRecordID': 'text',
        'InsuranceID': 'text',
        'BaseCharge': 'number',
        'MedicineCost': 'number',
        'InsuranceDiscount': 'number',
        'TotalCost': 'number',
        'DatePaid': 'date',
        'Status': 'text'
    }

    if request.method == 'POST':
        payment.MedicalRecordID_id = request.POST['MedicalRecordID'].strip()
        payment.InsuranceID_id = request.POST['InsuranceID'].strip()
        payment.BaseCharge = request.POST['BaseCharge']
        payment.MedicineCost = request.POST['MedicineCost']
        payment.InsuranceDiscount = request.POST['InsuranceDiscount']
        payment.TotalCost = request.POST['TotalCost']
        payment.DatePaid = request.POST['DatePaid']
        payment.Status = request.POST['Status'].strip()
        payment.save()

        return redirect('payment_list')

    context = {
        'model_name': 'Payment',
        'fields': fields,
        'input_types': input_types,
        'object': payment,
        'object_model_name': 'payment_list'
    }

    return render(request, 'edit_data/edit_data.html', context)


def delete_payment(request, payment_id):
    payment = get_object_or_404(Payment, PaymentID=payment_id)
    if request.method == 'POST':
        payment.delete()
        return redirect('payment_list')


class DiseaseListView(generic.ListView):
    model = Diseases
    template_name = 'disease_list.html'
    context_object_name = 'diseases'


def add_disease(request):
    if request.method == 'POST':
        name = request.POST.get('Name').strip()
        description = request.POST.get('Description').strip()
        treatment_id = request.POST.get('TreatmentID').strip()

        disease = Diseases(
            Name=name,
            Description=description,
            TreatmentID_id=treatment_id
        )
        disease.save()

        return redirect('disease_list')

    fields = [
        ('Name', 'Name'),
        ('Description', 'Description'),
        ('TreatmentID', 'Treatment ID')
    ]
    input_types = {
        'Name': 'text',
        'Description': 'text',
        'TreatmentID': 'text'
    }

    context = {
        'model_name': 'Diseases',
        'add_url_name': 'add_disease',
        'fields': fields,
        'input_types': input_types
    }

    return render(request, 'insert_data/add_data.html', context)


def delete_disease(request, disease_id):
    disease = get_object_or_404(Diseases, DiseaseID=disease_id)
    if request.method == 'POST':
        disease.delete()
        return redirect('disease_list')


def edit_disease(request, disease_id):
    disease = get_object_or_404(Diseases, DiseaseID=disease_id)

    fields = [
        ('Name', 'Disease Name'),
        ('Description', 'Description'),
        ('TreatmentID', 'Treatment ID')
    ]

    input_types = {
        'Name': 'text',
        'Description': 'text',
        'TreatmentID': 'text'
    }

    if request.method == 'POST':
        disease.Name = request.POST['Name'].strip()
        disease.Description = request.POST['Description'].strip()
        disease.TreatmentID_id = request.POST['TreatmentID'].strip()
        disease.save()
        return redirect('disease_list')

    context = {
        'model_name': 'Diseases',
        'fields': fields,
        'input_types': input_types,
        'object': disease,
        'object_model_name': 'disease_list'
    }

    return render(request, 'edit_data/edit_data.html', context)


class TreatmentListView(generic.ListView):
    model = Treatment
    template_name = 'treatment_list.html'
    context_object_name = 'treatments'


def add_treatment(request):
    if request.method == 'POST':
        treatment_type = request.POST.get('Type').strip()
        base_charge = request.POST.get('BaseCharge')

        treatment = Treatment(
            Type=treatment_type,
            BaseCharge=base_charge
        )
        treatment.save()

        return redirect('treatment_list')

    fields = [
        ('Type', 'Type'),
        ('BaseCharge', 'Base Charge')
    ]
    input_types = {
        'Type': 'text',
        'BaseCharge': 'number'
    }

    context = {
        'model_name': 'Treatment',
        'add_url_name': 'add_treatment',
        'fields': fields,
        'input_types': input_types
    }

    return render(request, 'insert_data/add_data.html', context)


def edit_treatment(request, treatment_id):
    treatment = get_object_or_404(Treatment, TreatmentID=treatment_id)
    fields = [
        ('Type', 'Treatment Type'),
        ('BaseCharge', 'Base Charge')
    ]

    input_types = {
        'Type': 'text',
        'BaseCharge': 'number'
    }

    if request.method == 'POST':
        treatment.Type = request.POST['Type'].strip()
        treatment.BaseCharge = request.POST['BaseCharge']
        treatment.save()

        return redirect('treatment_list')

    context = {
        'model_name': 'Treatment',
        'fields': fields,
        'input_types': input_types,
        'object': treatment,
        'object_model_name': 'treatment_list'
    }

    return render(request, 'edit_data/edit_data.html', context)


def delete_treatment(request, treatment_id):
    treatment = get_object_or_404(Treatment, TreatmentID=treatment_id)
    if request.method == 'POST':
        treatment.delete()
        return redirect('treatment_list')


class MedicineListView(generic.ListView):
    model = Medicine
    template_name = 'medicine_list.html'
    context_object_name = 'medicines'


def add_medicine(request):
    if request.method == 'POST':
        name = request.POST.get('Name').strip()
        brand = request.POST.get('Brand').strip()
        instructions = request.POST.get('Instructions').strip()
        default_dosage = request.POST.get('DefaultDosage').strip()
        price = request.POST.get('Price')

        medicine = Medicine(
            Name=name,
            Brand=brand,
            Instructions=instructions,
            DefaultDosage=default_dosage,
            Price=price
        )
        medicine.save()

        return redirect('medicine_list')

    fields = [
        ('Name', 'Name'),
        ('Brand', 'Brand'),
        ('Instructions', 'Instructions'),
        ('DefaultDosage', 'Default Dosage'),
        ('Price', 'Price')
    ]
    input_types = {
        'Name': 'text',
        'Brand': 'text',
        'Instructions': 'text',
        'DefaultDosage': 'text',
        'Price': 'number'
    }

    context = {
        'model_name': 'Medicine',
        'add_url_name': 'add_medicine',
        'fields': fields,
        'input_types': input_types
    }

    return render(request, 'insert_data/add_data.html', context)


def delete_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, MedicationID=medicine_id)
    if request.method == 'POST':
        medicine.delete()
        return redirect('medicine_list')


def edit_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, MedicationID=medicine_id)

    fields = [
        ('Name', 'Name'),
        ('Brand', 'Brand'),
        ('Instructions', 'Instructions'),
        ('DefaultDosage', 'Default Dosage'),
        ('Price', 'Price')
    ]

    input_types = {
        'Name': 'text',
        'Brand': 'text',
        'Instructions': 'text',
        'DefaultDosage': 'text',
        'Price': 'number'
    }

    if request.method == 'POST':
        medicine.Name = request.POST['Name'].strip()
        medicine.Brand = request.POST['Brand'].strip()
        medicine.Instructions = request.POST['Instructions'].strip()
        medicine.DefaultDosage = request.POST['DefaultDosage'].strip()
        medicine.Price = request.POST['Price']
        medicine.save()
        return redirect('medicine_list')

    context = {
        'model_name': 'Medicine',
        'fields': fields,
        'input_types': input_types,
        'object': medicine,
        'object_model_name': 'medicine_list'
    }

    return render(request, 'edit_data/edit_data.html', context)


class DosageListView(generic.ListView):
    model = Dosage
    template_name = 'dosage_list.html'
    context_object_name = 'dosages'


def add_dosage(request):
    if request.method == 'POST':
        medication_id = request.POST.get('MedicationID').strip()
        min_weight = request.POST.get('MinWeight')
        max_weight = request.POST.get('MaxWeight')
        min_age = request.POST.get('MinAge')
        max_age = request.POST.get('MaxAge')
        recommend_dosage = request.POST.get('RecommendDosage').strip()
        units = request.POST.get('Units').strip()
        notes = request.POST.get('Notes').strip()

        dosage = Dosage(
            MedicationID_id=medication_id,
            MinWeight=min_weight,
            MaxWeight=max_weight,
            MinAge=min_age,
            MaxAge=max_age,
            RecommendDosage=recommend_dosage,
            Units=units,
            Notes=notes
        )
        dosage.save()

        return redirect('dosage_list')

    fields = [
        ('MedicationID', 'Medication ID'),
        ('MinWeight', 'Min Weight'),
        ('MaxWeight', 'Max Weight'),
        ('MinAge', 'Min Age'),
        ('MaxAge', 'Max Age'),
        ('RecommendDosage', 'Recommended Dosage'),
        ('Units', 'Units'),
        ('Notes', 'Notes')
    ]
    input_types = {
        'MedicationID': 'text',
        'MinWeight': 'number',
        'MaxWeight': 'number',
        'MinAge': 'number',
        'MaxAge': 'number',
        'RecommendDosage': 'text',
        'Units': 'text',
        'Notes': 'text'
    }

    context = {
        'model_name': 'Dosage',
        'add_url_name': 'add_dosage',
        'fields': fields,
        'input_types': input_types
    }

    return render(request, 'insert_data/add_data.html', context)


def delete_dosage(request, dosage_id):
    dosage = get_object_or_404(Dosage, DosageID=dosage_id)
    if request.method == 'POST':
        dosage.delete()
        return redirect('dosage_list')


def edit_dosage(request, dosage_id):
    dosage = get_object_or_404(Dosage, DosageID=dosage_id)

    fields = [
        ('MedicationID', 'Medication ID'),
        ('MinWeight', 'Min Weight'),
        ('MaxWeight', 'Max Weight'),
        ('MinAge', 'Min Age'),
        ('MaxAge', 'Max Age'),
        ('RecommendDosage', 'Recommended Dosage'),
        ('Units', 'Units'),
        ('Notes', 'Notes')
    ]

    input_types = {
        'MedicationID': 'text',
        'MinWeight': 'number',
        'MaxWeight': 'number',
        'MinAge': 'number',
        'MaxAge': 'number',
        'RecommendDosage': 'text',
        'Units': 'text',
        'Notes': 'text'
    }

    if request.method == 'POST':
        dosage.MedicationID = get_object_or_404(Medicine,
                                                MedicationID=request.POST[
                                                    'MedicationID'].strip())
        dosage.MinWeight = request.POST['MinWeight']
        dosage.MaxWeight = request.POST['MaxWeight']
        dosage.MinAge = request.POST['MinAge']
        dosage.MaxAge = request.POST['MaxAge']
        dosage.RecommendDosage = request.POST['RecommendDosage'].strip()
        dosage.Units = request.POST['Units'].strip()
        dosage.Notes = request.POST['Notes'].strip()
        dosage.save()

        return redirect('dosage_list')

    context = {
        'model_name': 'Dosage',
        'fields': fields,
        'input_types': input_types,
        'object': dosage,
        'object_model_name': 'dosage_list'
        # For generating the back button URL
    }

    return render(request, 'edit_data/edit_data.html', context)


class PatientListView(generic.ListView):
    model = Patient
    template_name = 'patient_list.html'
    context_object_name = 'patients'


def add_patient(request):
    if request.method == 'POST':
        name = request.POST.get('Name').strip()
        phone = request.POST.get('Phone').strip()
        email = request.POST.get('Email').strip()
        birthdate = request.POST.get('Birthdate')
        weight = request.POST.get('Weight')
        height = request.POST.get('Height')
        emergency_contact = request.POST.get('EmergencyContact').strip()

        patient = Patient(
            Name=name,
            Phone=phone,
            Email=email,
            Birthdate=birthdate,
            Weight=weight,
            Height=height,
            EmergencyContact=emergency_contact
        )
        patient.save()

        return redirect('patient_list')

    fields = [
        ('Name', 'Name'),
        ('Phone', 'Phone'),
        ('Email', 'Email'),
        ('Birthdate', 'Birthdate'),
        ('Weight', 'Weight'),
        ('Height', 'Height'),
        ('EmergencyContact', 'Emergency Contact')
    ]
    input_types = {
        'Name': 'text',
        'Phone': 'text',
        'Email': 'email',
        'Birthdate': 'date',
        'Weight': 'number',
        'Height': 'number',
        'EmergencyContact': 'text'
    }

    context = {
        'model_name': 'Patient',
        'add_url_name': 'add_patient',
        'fields': fields,
        'input_types': input_types
    }

    return render(request, 'insert_data/add_data.html', context)


def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, PatientID=patient_id)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')


def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, PatientID=patient_id)
    fields = [
        ('Name', 'Name'),
        ('Phone', 'Phone'),
        ('Email', 'Email'),
        ('Birthdate', 'Birthdate'),
        ('Weight', 'Weight'),
        ('Height', 'Height'),
        ('EmergencyContact', 'Emergency Contact')
    ]

    input_types = {
        'Name': 'text',
        'Phone': 'text',
        'Email': 'email',
        'Birthdate': 'date',
        'Weight': 'number',
        'Height': 'number',
        'EmergencyContact': 'text'
    }

    if request.method == 'POST':
        patient.Name = request.POST['Name'].strip()
        patient.Phone = request.POST['Phone'].strip()
        patient.Email = request.POST['Email'].strip()
        patient.Birthdate = request.POST['Birthdate']
        patient.Weight = request.POST['Weight']
        patient.Height = request.POST['Height']
        patient.EmergencyContact = request.POST['EmergencyContact'].strip()
        patient.save()

        return redirect('patient_list')

    context = {
        'model_name': 'Patient',
        'fields': fields,
        'input_types': input_types,
        'object': patient,
        'object_model_name': 'patient_list'
    }

    return render(request, 'edit_data/edit_data.html', context)


class DoctorListView(generic.ListView):
    model = Doctor
    template_name = 'doctor_list.html'
    context_object_name = 'doctors'


def add_doctor(request):
    if request.method == 'POST':
        name = request.POST.get('Name').strip()
        phone = request.POST.get('Phone').strip()
        email = request.POST.get('Email').strip()
        birthdate = request.POST.get('Birthdate')
        specialization = request.POST.get('Specialization').strip()

        doctor = Doctor(
            Name=name,
            Phone=phone,
            Email=email,
            Birthdate=birthdate,
            Specialization=specialization
        )
        doctor.save()

        return redirect('doctor_list')

    fields = [
        ('Name', 'Name'),
        ('Phone', 'Phone'),
        ('Email', 'Email'),
        ('Birthdate', 'Birthdate'),
        ('Specialization', 'Specialization')
    ]
    input_types = {
        'Name': 'text',
        'Phone': 'text',
        'Email': 'email',
        'Birthdate': 'date',
        'Specialization': 'text'
    }

    context = {
        'model_name': 'Doctor',
        'add_url_name': 'add_doctor',
        'fields': fields,
        'input_types': input_types
    }

    return render(request, 'insert_data/add_data.html', context)


def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, DoctorID=doctor_id)
    if request.method == 'POST':
        doctor.delete()
        return redirect('doctor_list')


def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, DoctorID=doctor_id)

    fields = [
        ('Name', 'Name'),
        ('Phone', 'Phone'),
        ('Email', 'Email'),
        ('Birthdate', 'Birthdate'),
        ('Specialization', 'Specialization')
    ]

    input_types = {
        'Name': 'text',
        'Phone': 'text',
        'Email': 'email',
        'Birthdate': 'date',
        'Specialization': 'text'
    }

    if request.method == 'POST':
        doctor.Name = request.POST['Name'].strip()
        doctor.Phone = request.POST['Phone'].strip()
        doctor.Email = request.POST['Email'].strip()
        doctor.Birthdate = request.POST['Birthdate']
        doctor.Specialization = request.POST['Specialization'].strip()
        doctor.save()

        return redirect('doctor_list')

    context = {
        'model_name': 'Doctor',
        'fields': fields,
        'input_types': input_types,
        'object': doctor,
        'object_model_name': 'doctor_list'
    }

    return render(request, 'edit_data/edit_data.html', context)


class MedicalRecordListView(generic.ListView):
    model = MedicalRecord
    template_name = 'medical_record_list.html'
    context_object_name = 'medical_records'


def add_medical_record(request):
    if request.method == 'POST':
        patient_id = request.POST.get('PatientID').strip()
        doctor_id = request.POST.get('DoctorID').strip()
        disease_id = request.POST.get('DiseaseID').strip()
        visit_reason = request.POST.get('VisitReason').strip()
        summary = request.POST.get('Summary').strip()
        date_visit = request.POST.get('DateVisit')
        status = request.POST.get('Status').strip()

        medical_record = MedicalRecord(
            PatientID_id=patient_id,
            DoctorID_id=doctor_id,
            DiseaseID_id=disease_id,
            VisitReason=visit_reason,
            Summary=summary,
            DateVisit=date_visit,
            Status=status
        )
        medical_record.save()

        return redirect('medical_record_list')

    fields = [
        ('PatientID', 'Patient ID'),
        ('DoctorID', 'Doctor ID'),
        ('DiseaseID', 'Disease ID'),
        ('VisitReason', 'Visit Reason'),
        ('Summary', 'Summary'),
        ('DateVisit', 'Date of Visit'),
        ('Status', 'Status')
    ]
    input_types = {
        'PatientID': 'text',
        'DoctorID': 'text',
        'DiseaseID': 'text',
        'VisitReason': 'text',
        'Summary': 'text',
        'DateVisit': 'date',
        'Status': 'text'
    }

    context = {
        'model_name': 'Medical Record',
        'add_url_name': 'add_medical_record',
        'fields': fields,
        'input_types': input_types
    }

    return render(request, 'insert_data/add_data.html', context)


def delete_medical_record(request, medical_record_id):
    medical_record = get_object_or_404(MedicalRecord,
                                       MedicalRecordID=medical_record_id)
    if request.method == 'POST':
        medical_record.delete()
        return redirect('medical_record_list')


def edit_medical_record(request, medical_record_id):
    medical_record = get_object_or_404(MedicalRecord,
                                       MedicalRecordID=medical_record_id)

    fields = [
        ('PatientID', 'Patient ID'),
        ('DoctorID', 'Doctor ID'),
        ('DiseaseID', 'Disease ID'),
        ('VisitReason', 'Visit Reason'),
        ('Summary', 'Summary'),
        ('DateVisit', 'Date of Visit'),
        ('Status', 'Status')
    ]

    input_types = {
        'PatientID': 'text',
        'DoctorID': 'text',
        'DiseaseID': 'text',
        'VisitReason': 'text',
        'Summary': 'text',
        'DateVisit': 'date',
        'Status': 'text'
    }

    if request.method == 'POST':
        medical_record.PatientID = get_object_or_404(Patient,
                                                     PatientID=request.POST[
                                                         'PatientID'].strip())
        medical_record.DoctorID = get_object_or_404(Doctor,
                                                    DoctorID=request.POST[
                                                        'DoctorID'].strip())
        medical_record.DiseaseID = get_object_or_404(Diseases,
                                                     DiseaseID=request.POST[
                                                         'DiseaseID'].strip())
        medical_record.VisitReason = request.POST['VisitReason'].strip()
        medical_record.Summary = request.POST['Summary'].strip()
        medical_record.DateVisit = request.POST['DateVisit']
        medical_record.Status = request.POST['Status'].strip()
        medical_record.save()

        return redirect('medical_record_list')

    context = {
        'model_name': 'Medical Record',
        'fields': fields,
        'input_types': input_types,
        'object': medical_record,
        'object_model_name': 'medical_record_list'
        # For generating the back button URL
    }

    return render(request, 'edit_data/edit_data.html', context)


class MedicineRecordListView(generic.ListView):
    model = MedicineRecord
    template_name = 'medicine_record_list.html'
    context_object_name = 'medicine_records'


def add_medicine_record(request):
    if request.method == 'POST':
        medical_record_id = request.POST.get('MedicalRecordID').strip()
        medication_id = request.POST.get('MedicationID').strip()
        dosage_id = request.POST.get('DosageID').strip()
        quantity = request.POST.get('Quantity')
        cost = request.POST.get('Cost')

        medicine_record = MedicineRecord(
            MedicalRecordID_id=medical_record_id,
            MedicationID_id=medication_id,
            DosageID_id=dosage_id,
            Quantity=quantity,
            Cost=cost
        )
        medicine_record.save()

        return redirect('medicine_record_list')

    fields = [
        ('MedicalRecordID', 'Medical Record ID'),
        ('MedicationID', 'Medication ID'),
        ('DosageID', 'Dosage ID'),
        ('Quantity', 'Quantity'),
        ('Cost', 'Cost')
    ]
    input_types = {
        'MedicalRecordID': 'text',
        'MedicationID': 'text',
        'DosageID': 'text',
        'Quantity': 'number',
        'Cost': 'number'
    }

    context = {
        'model_name': 'Medicine Record',
        'add_url_name': 'add_medicine_record',
        'fields': fields,
        'input_types': input_types
    }

    return render(request, 'insert_data/add_data.html', context)


def delete_medicine_record(request, medical_record_id):
    medicine_record = get_object_or_404(MedicineRecord,
                                        MedicalRecordID=medical_record_id)
    if request.method == 'POST':
        medicine_record.delete()
        return redirect('medicine_record_list')


def edit_medicine_record(request, medicine_record_id):
    # Retrieve the MedicineRecord object to edit
    medicine_record = get_object_or_404(MedicineRecord,
                                        MedicineRecordID=medicine_record_id)

    fields = [
        ('MedicalRecordID', 'Medical Record ID'),
        ('MedicationID', 'Medication ID'),
        ('DosageID', 'Dosage ID'),
        ('Quantity', 'Quantity'),
        ('Cost', 'Cost')
    ]

    input_types = {
        'MedicalRecordID': 'text',
        'MedicationID': 'text',
        'DosageID': 'text',
        'Quantity': 'number',
        'Cost': 'number'
    }

    if request.method == 'POST':
        medicine_record.MedicalRecordID = get_object_or_404(MedicalRecord,
                                                            MedicalRecordID=
                                                            request.POST[
                                                                'MedicalRecordID'].strip())
        medicine_record.MedicationID = get_object_or_404(Medicine,
                                                         MedicationID=
                                                         request.POST[
                                                             'MedicationID'].strip())
        medicine_record.DosageID = get_object_or_404(Dosage,
                                                     DosageID=request.POST[
                                                         'DosageID'].strip())
        medicine_record.Quantity = request.POST['Quantity']
        medicine_record.Cost = request.POST['Cost']
        medicine_record.save()
        return redirect('medicine_record_list')

    context = {
        'model_name': 'Medicine Record',
        'fields': fields,
        'input_types': input_types,
        'object': medicine_record,
        'object_model_name': 'medicine_record_list'
    }
    return render(request, 'edit_data/edit_data.html', context)


class AppointmentListView(generic.ListView):
    model = Appointment
    template_name = 'appointment_list.html'
    context_object_name = 'appointments'


def add_appointment(request):
    if request.method == 'POST':
        date = request.POST.get('Date')
        start_time = request.POST.get('StartTime')
        end_time = request.POST.get('EndTime')
        patient_id = request.POST.get('PatientID').strip()
        doctor_id = request.POST.get('DoctorID').strip()

        appointment = Appointment(
            Date=date,
            StartTime=start_time,
            EndTime=end_time,
            PatientID_id=patient_id,
            DoctorID_id=doctor_id
        )
        appointment.save()
        return redirect('appointment_list')

    fields = [
        ('Date', 'Date'),
        ('StartTime', 'Start Time'),
        ('EndTime', 'End Time'),
        ('PatientID', 'Patient ID'),
        ('DoctorID', 'Doctor ID')
    ]
    input_types = {
        'Date': 'date',
        'StartTime': 'time',
        'EndTime': 'time',
        'PatientID': 'text',
        'DoctorID': 'text'
    }

    context = {
        'model_name': 'Appointment',
        'add_url_name': 'add_appointment',
        'fields': fields,
        'input_types': input_types
    }

    return render(request, 'insert_data/add_data.html', context)


def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, AppointmentID=appointment_id)
    appointment.delete()
    return redirect('appointment_list')


def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, AppointmentID=appointment_id)

    fields = [
        ('Date', 'Appointment Date'),
        ('StartTime', 'Start Time'),
        ('EndTime', 'End Time'),
        ('PatientID', 'Patient ID'),
        ('DoctorID', 'Doctor ID')
    ]

    input_types = {
        'Date': 'date',
        'StartTime': 'time',
        'EndTime': 'time',
        'PatientID': 'text',
        'DoctorID': 'text'
    }

    if request.method == 'POST':
        appointment.Date = request.POST['Date']
        appointment.StartTime = request.POST['StartTime']
        appointment.EndTime = request.POST['EndTime']
        appointment.PatientID = get_object_or_404(Patient,
                                                  PatientID=request.POST[
                                                      'PatientID'].strip())
        appointment.DoctorID = get_object_or_404(Doctor, DoctorID=request.POST[
            'DoctorID'].strip())
        appointment.save()

        return redirect('appointment_list')

    context = {
        'model_name': 'Appointment',
        'fields': fields,
        'input_types': input_types,
        'object': appointment,
        'object_model_name': 'appointment_list'
    }

    return render(request, 'edit_data/edit_data.html', context)


class AvailabilityListView(generic.ListView):
    model = Availability
    template_name = 'availability_list.html'
    context_object_name = 'availabilities'


def add_availability(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('DoctorID').strip()
        date = request.POST.get('Date')
        start_time = request.POST.get('StartTime')
        end_time = request.POST.get('EndTime')

        availability = Availability(
            DoctorID_id=doctor_id,
            Day=date,
            StartTime=start_time,
            EndTime=end_time
        )
        availability.save()

        return redirect('availability_list')

    fields = [
        ('DoctorID', 'Doctor ID'),
        ('Date', 'Date'),
        ('StartTime', 'Start Time'),
        ('EndTime', 'End Time')
    ]
    input_types = {
        'DoctorID': 'text',
        'Date': 'date',
        'StartTime': 'time',
        'EndTime': 'time'
    }

    context = {
        'model_name': 'Availability',
        'add_url_name': 'add_availability',
        'fields': fields,
        'input_types': input_types
    }

    return render(request, 'insert_data/add_data.html', context)


def delete_availability(request, availability_id):
    availability = get_object_or_404(Availability,
                                     AvailabilityID=availability_id)
    if request.method == 'POST':
        availability.delete()
        return redirect('availability_list')


def edit_availability(request, availability_id):
    availability = get_object_or_404(Availability,
                                     AvailabilityID=availability_id)

    fields = [
        ('DoctorID', 'Doctor ID'),
        ('Date', 'Date'),
        ('StartTime', 'Start Time'),
        ('EndTime', 'End Time')
    ]

    input_types = {
        'DoctorID': 'text',
        'Date': 'date',
        'StartTime': 'time',
        'EndTime': 'time'
    }

    if request.method == 'POST':
        availability.DoctorID = get_object_or_404(Doctor,
                                                  DoctorID=request.POST[
                                                      'DoctorID'].strip())
        availability.Day = request.POST['Date']
        availability.StartTime = request.POST['StartTime']
        availability.EndTime = request.POST['EndTime']
        availability.save()

        return redirect('availability_list')

    context = {
        'model_name': 'Availability',
        'fields': fields,
        'input_types': input_types,
        'object': availability,
        'object_model_name': 'availability_list'
    }

    return render(request, 'edit_data/edit_data.html', context)
