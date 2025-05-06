from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
]

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=GENDER_CHOICES[0][0])  
    specialization = models.TextField(max_length=250)
    years_of_experience = models.IntegerField()
    hospital_affiliation = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
    
class Medicine(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(max_length=250)
    photo = models.TextField()

    def __str__(self):
        return self.name
    
    
class Patient(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=GENDER_CHOICES[0][0])
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='patients')
    medicines = models.ManyToManyField(Medicine, related_name='patients', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Review(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    message = models.TextField(max_length=500)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    reply = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.doctor.name} - Rating: {self.rating}"
    

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='prescriptions')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='prescriptions')
    date_prescribed = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} - {self.medicine.name} by {self.doctor.name}"


# INSERT INTO main_app_doctor 
# VALUES
# (DEFAULT,'Dr. Ahmed Al-Qahtani', 'M', 'Cardiology', 10, 'King Faisal Specialist Hospital', 1),
# (DEFAULT,'Dr. Nora Al-Shehri', 'F', 'Dermatology', 8, 'King Khalid University Hospital', 2),
# (DEFAULT,'Dr. Faisal Al-Dosari', 'M', 'Neurology', 12, 'Riyadh Military Hospital', 3),
# (DEFAULT,'Dr. Amani Al-Harbi', 'F', 'Pediatrics', 7, 'King Fahd Medical City', 4),
# (DEFAULT,'Dr. Saleh Al-Zahrani', 'M', 'Orthopedics', 15, 'King Saud Medical City', 5),
# (DEFAULT,'Dr. Reem Al-Otaibi', 'F', 'Gynecology', 11, 'King Khalid Hospital', 6),
# (DEFAULT,'Dr. Majed Al-Mutairi', 'M', 'Psychiatry', 9, 'Security Forces Hospital', 7),
# (DEFAULT,'Dr. Huda Al-Juhani', 'F', 'Ophthalmology', 6, 'National Guard Hospital', 8),
# (DEFAULT,'Dr. Turki Al-Fahad', 'M', 'General Surgery', 13, 'Al-Mouwasat Hospital', 9),
# (DEFAULT,'Dr. Lama Al-Saleh', 'F', 'Endocrinology', 10, 'Dr. Sulaiman Al Habib Hospital', 10),
# (DEFAULT,'Dr. Khaled Al-Shammari', 'M', 'Urology', 14, 'King Abdullah Medical City', 11),
# (DEFAULT,'Dr. Sarah Al-Qahtani', 'F', 'Internal Medicine', 9, 'Dallah Hospital', 12),
# (DEFAULT,'Dr. Badr Al-Anazi', 'M', 'ENT', 8, 'King Saud University Medical City', 13),
# (DEFAULT,'Dr. Muna Al-Hazza', 'F', 'Family Medicine', 7, 'International Medical Center', 14),
# (DEFAULT,'Dr. Nasser Al-Otaibi', 'M', 'Oncology', 16, 'Saudi German Hospital', 15),
# (DEFAULT,'Dr. Dana Al-Amri', 'F', 'Radiology', 5, 'Al Hammadi Hospital', 16),
# (DEFAULT,'Dr. Mishal Al-Rashid', 'M', 'Gastroenterology', 12, 'King Fahad Armed Forces Hospital', 17),
# (DEFAULT,'Dr. Wafa Al-Faraj', 'F', 'Nephrology', 10, 'Prince Sultan Military Medical City', 18),
# (DEFAULT,'Dr. Sami Al-Ghamdi', 'M', 'Pulmonology', 11, 'King Salman Hospital', 19),
# (DEFAULT,'Dr. Rania Al-Dossary', 'F', 'Rheumatology', 6, 'Riyadh Care Hospital', 20);
