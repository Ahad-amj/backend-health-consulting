from django.db import models

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

    def __str__(self):
        return self.name
    
class Medicine(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(max_length=250)
    photo = models.TextField()

    def __str__(self):
        return self.name
    
