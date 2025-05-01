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
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Medicine(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(max_length=250)
    photo = models.TextField()

    def __str__(self):
        return self.name
    
    
# class Patient(models.Model):
#     name = models.CharField(max_length=100)
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=GENDER_CHOICES[0][0])
#     doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='patients')
#     medicines = models.ManyToManyField(Medicine, related_name='patients', blank=True)
#     prescription = models.TextField(blank=True)

#     def __str__(self):
#         return self.name
    
class Review(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='reviews')
    # patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='reviews')
    message = models.TextField(max_length=500)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    reply = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.doctor.name} - Rating: {self.rating}"
    

# class Prescription(models.Model):
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='prescriptions')
#     medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='prescriptions')
#     date_prescribed = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.patient.name} - {self.medicine.name} by {self.doctor.name}"