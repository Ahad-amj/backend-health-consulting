from django.contrib import admin
from .models import Doctor, Medicine, Review, Patient, Prescription

admin.site.site_header = "Central Medical Control System"
admin.site.register(Prescription)
admin.site.register(Doctor)
admin.site.register(Medicine)
admin.site.register(Patient)
admin.site.register(Review)



