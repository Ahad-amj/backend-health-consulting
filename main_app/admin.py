from django.contrib import admin
from .models import Doctor, Medicine, Review, Patient

admin.site.register(Doctor)
admin.site.register(Medicine)
admin.site.register(Patient)
admin.site.register(Review)