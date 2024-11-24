from django.db import models


# Create your models here.
class CoveragePolicy(models.Model):
    PolicyID = models.CharField(max_length=30, primary_key=True)
    InsuranceID = models.ForeignKey('Insurance', on_delete=models.CASCADE, db_column='InsuranceID')
    TreatmentID = models.ForeignKey('Treatment', on_delete=models.CASCADE, db_column='TreatmentID')
    CoveragePercentage = models.PositiveIntegerField()
    MaxCoverageAmount = models.PositiveIntegerField()

    def __str__(self):
        return self.PolicyID


class Insurance(models.Model):
    InsuranceID = models.CharField(max_length=30, primary_key=True)
    PatientID = models.ForeignKey('Patient', on_delete=models.CASCADE, db_column='PatientID')
    Provider = models.CharField(max_length=100)
    CoverageAmount = models.PositiveIntegerField()
    ExpireDate = models.DateField()
    Type = models.CharField(max_length=50)

    def __str__(self):
        return self.InsuranceID


class Payment(models.Model):
    PaymentID = models.CharField(max_length=30, primary_key=True)
    MedicalRecordID = models.ForeignKey('MedicalRecord', on_delete=models.CASCADE, db_column='MedicalRecordID')
    InsuranceID = models.ForeignKey('Insurance', on_delete=models.SET_NULL, null=True, blank=True,
                                    db_column='InsuranceID')
    BaseCharge = models.PositiveIntegerField()
    MedicineCost = models.PositiveIntegerField()
    InsuranceDiscount = models.PositiveIntegerField()
    TotalCost = models.PositiveIntegerField()
    DatePaid = models.DateField(null=True, blank=True)
    Status = models.CharField(max_length=50)

    def __str__(self):
        return self.PaymentID


class Diseases(models.Model):
    DiseaseID = models.CharField(max_length=30, primary_key=True)
    Name = models.CharField(max_length=100)
    Description = models.TextField()
    TreatmentID = models.ForeignKey('Treatment', on_delete=models.CASCADE, db_column='TreatmentID')

    def __str__(self):
        return self.Name


class Treatment(models.Model):
    TreatmentID = models.CharField(max_length=30, primary_key=True)
    Type = models.CharField(max_length=100)
    BaseCharge = models.PositiveIntegerField()

    def __str__(self):
        return self.Type


class Medicine(models.Model):
    MedicationID = models.CharField(max_length=30, primary_key=True)
    Name = models.CharField(max_length=100)
    Brand = models.CharField(max_length=100)
    Instructions = models.TextField()
    DefaultDosage = models.CharField(max_length=50)
    Price = models.PositiveIntegerField()

    def __str__(self):
        return self.Name


class Dosage(models.Model):
    DosageID = models.CharField(max_length=30, primary_key=True)
    MedicationID = models.ForeignKey(Medicine, on_delete=models.CASCADE, db_column='MedicationID')
    MinWeight = models.CharField(max_length=50)
    MaxWeight = models.CharField(max_length=50)
    MinAge = models.PositiveIntegerField()
    MaxAge = models.PositiveIntegerField()
    RecommendDosage = models.CharField(max_length=100)
    Units = models.CharField(max_length=50)
    Notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.DosageID


class Patient(models.Model):
    PatientID = models.CharField(max_length=30, primary_key=True)
    Name = models.CharField(max_length=100)
    # Phone = models.CharField(max_length=15)
    Email = models.EmailField()
    Birthdate = models.DateField()
    EmergencyContact = models.CharField(max_length=100)
    Weight = models.CharField(max_length=50)
    Height = models.CharField(max_length=50)

    def __str__(self):
        return self.Name


class MedicalRecord(models.Model):
    MedicalRecordID = models.CharField(max_length=30, primary_key=True)
    PatientID = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='PatientID')
    DoctorID = models.ForeignKey('Doctor', on_delete=models.CASCADE, db_column='DoctorID')
    DiseaseID = models.ForeignKey(Diseases, on_delete=models.CASCADE, db_column='DiseaseID')
    VisitReason = models.CharField(max_length=200)
    Summary = models.TextField()
    DateVisit = models.DateField()
    Status = models.CharField(max_length=50)

    def __str__(self):
        return self.MedicalRecordID


class MedicineRecord(models.Model):
    MedicineRecordID = models.CharField(max_length=30, primary_key=True)
    MedicalRecordID = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, db_column='MedicalRecordID')
    MedicationID = models.ForeignKey(Medicine, on_delete=models.CASCADE, db_column='MedicationID')
    DosageID = models.ForeignKey(Dosage, on_delete=models.CASCADE, db_column='DosageID')
    Quantity = models.PositiveIntegerField()
    Cost = models.PositiveIntegerField()

    def __str__(self):
        return self.MedicineRecordID


class Doctor(models.Model):
    DoctorID = models.CharField(max_length=30, primary_key=True)
    Name = models.CharField(max_length=100)
    Phone = models.CharField(max_length=15)
    Email = models.EmailField()
    Birthdate = models.DateField()
    Specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.Name


class Appointment(models.Model):
    AppointmentID = models.CharField(max_length=30, primary_key=True)
    Date = models.DateField()
    StartTime = models.TimeField()
    EndTime = models.TimeField()
    PatientID = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='PatientID')
    DoctorID = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='DoctorID')

    def __str__(self):
        return self.AppointmentID


class Availability(models.Model):
    AvailabilityID = models.CharField(max_length=30, primary_key=True)
    DoctorID = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="availabilities")
    Day = models.CharField(max_length=15)
    StartTime = models.TimeField()
    EndTime = models.TimeField()

    def __str__(self):
        return f"{self.DoctorID} - {self.Day} ({self.StartTime} to {self.EndTime})"
