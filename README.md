# ClinicManagement
A repository for the Database 2024 project

## Coding Guideline
- Please commit a meaningful message such as 'Add customer query and fix data loading error'.
- Every PR requires a review from one of the team members.
- Have fun doing this project (not much fun due to the time limit).

## Installation Guide
### 1. Clone the repository
- `git clone https://github.com/EggADayKeepTheTeacherAway/ClinicManagement.git`
### 2. Migrate
- `python manage.py migrate`
### 3. Load data
- `python manage.py loaddata data/patient.json data/doctor.json data/treatment.json data/diseases.json data/insurance.json data/coveragepolicy.json data/medicalrecord.json data/medicine.json data/dosage.json data/medicinerecord.json data/appointment.json data/availability.json data/payment.json`
### 4. Start server
- `python manage.py runserver`

![nurse_egg_image](https://github.com/user-attachments/assets/7ffcc7ac-a900-40d7-92d7-20c808de07a2)
