# Generated by Django 5.1 on 2024-11-25 16:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Diseases',
            fields=[
                ('DiseaseID', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=100)),
                ('Description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('DoctorID', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=100)),
                ('Phone', models.CharField(max_length=15)),
                ('Email', models.EmailField(max_length=254)),
                ('Birthdate', models.DateField()),
                ('Specialization', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('MedicationID', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=100)),
                ('Brand', models.CharField(max_length=100)),
                ('Instructions', models.TextField()),
                ('DefaultDosage', models.CharField(max_length=50)),
                ('Price', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('PatientID', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=100)),
                ('Phone', models.CharField(max_length=15)),
                ('Email', models.EmailField(max_length=254)),
                ('Birthdate', models.DateField()),
                ('EmergencyContact', models.CharField(max_length=100)),
                ('Weight', models.CharField(max_length=50)),
                ('Height', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('TreatmentID', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('Type', models.CharField(max_length=100)),
                ('BaseCharge', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('AvailabilityID', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('Day', models.CharField(max_length=15)),
                ('StartTime', models.TimeField()),
                ('EndTime', models.TimeField()),
                ('DoctorID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availabilities', to='clinic_management.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('MedicalRecordID', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('VisitReason', models.CharField(max_length=200)),
                ('Summary', models.TextField()),
                ('DateVisit', models.DateField()),
                ('Status', models.CharField(max_length=50)),
                ('DiseaseID', models.ForeignKey(db_column='DiseaseID', on_delete=django.db.models.deletion.CASCADE, to='clinic_management.diseases')),
                ('DoctorID', models.ForeignKey(db_column='DoctorID', on_delete=django.db.models.deletion.CASCADE, to='clinic_management.doctor')),
                ('PatientID', models.ForeignKey(db_column='PatientID', on_delete=django.db.models.deletion.CASCADE, to='clinic_management.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Dosage',
            fields=[
                ('DosageID', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('MinWeight', models.CharField(max_length=50)),
                ('MaxWeight', models.CharField(max_length=50)),
                ('MinAge', models.PositiveIntegerField()),
                ('MaxAge', models.PositiveIntegerField()),
                ('RecommendDosage', models.CharField(max_length=100)),
                ('Units', models.CharField(max_length=50)),
                ('Notes', models.TextField(blank=True, null=True)),
                ('MedicationID', models.ForeignKey(db_column='MedicationID', on_delete=django.db.models.deletion.CASCADE, to='clinic_management.medicine')),
            ],
        ),
        migrations.CreateModel(
            name='MedicineRecord',
            fields=[
                ('MedicineRecordID', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('Quantity', models.PositiveIntegerField()),
                ('Cost', models.PositiveIntegerField()),
                ('DosageID', models.ForeignKey(db_column='DosageID', on_delete=django.db.models.deletion.CASCADE, to='clinic_management.dosage')),
                ('MedicalRecordID', models.ForeignKey(db_column='MedicalRecordID', on_delete=django.db.models.deletion.CASCADE, to='clinic_management.medicalrecord')),
                ('MedicationID', models.ForeignKey(db_column='MedicationID', on_delete=django.db.models.deletion.CASCADE, to='clinic_management.medicine')),
            ],
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('InsuranceID', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('Provider', models.CharField(max_length=100)),
                ('CoverageAmount', models.PositiveIntegerField()),
                ('ExpireDate', models.DateField()),
                ('Type', models.CharField(max_length=50)),
                ('PatientID', models.ForeignKey(db_column='PatientID', on_delete=django.db.models.deletion.CASCADE, to='clinic_management.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('AppointmentID', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('Date', models.DateField()),
                ('StartTime', models.TimeField()),
                ('EndTime', models.TimeField()),
                ('DoctorID', models.ForeignKey(db_column='DoctorID', on_delete=django.db.models.deletion.CASCADE, to='clinic_management.doctor')),
                ('PatientID', models.ForeignKey(db_column='PatientID', on_delete=django.db.models.deletion.CASCADE, to='clinic_management.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('PaymentID', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('BaseCharge', models.PositiveIntegerField()),
                ('MedicineCost', models.PositiveIntegerField()),
                ('InsuranceDiscount', models.PositiveIntegerField()),
                ('TotalCost', models.PositiveIntegerField()),
                ('DatePaid', models.DateField(blank=True, null=True)),
                ('Status', models.CharField(max_length=50)),
                ('InsuranceID', models.ForeignKey(blank=True, db_column='InsuranceID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinic_management.insurance')),
                ('MedicalRecordID', models.ForeignKey(db_column='MedicalRecordID', on_delete=django.db.models.deletion.CASCADE, to='clinic_management.medicalrecord')),
            ],
        ),
        migrations.AddField(
            model_name='diseases',
            name='TreatmentID',
            field=models.ForeignKey(db_column='TreatmentID', on_delete=django.db.models.deletion.CASCADE, to='clinic_management.treatment'),
        ),
        migrations.CreateModel(
            name='CoveragePolicy',
            fields=[
                ('PolicyID', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('CoveragePercentage', models.PositiveIntegerField()),
                ('MaxCoverageAmount', models.PositiveIntegerField()),
                ('InsuranceID', models.ForeignKey(db_column='InsuranceID', on_delete=django.db.models.deletion.CASCADE, to='clinic_management.insurance')),
                ('TreatmentID', models.ForeignKey(db_column='TreatmentID', on_delete=django.db.models.deletion.CASCADE, to='clinic_management.treatment')),
            ],
        ),
    ]