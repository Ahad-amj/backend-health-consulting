from django.urls import path
from .views import Home, DoctorsIndex, DoctorDetail, MedicineIndex

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('doctors/', DoctorsIndex.as_view(), name='doctor-index'),
  path('doctors/<int:doctor_id>/', DoctorDetail.as_view(), name='doctor-detail'),
  path('medicines/', MedicineIndex.as_view(), name='medicine-index'),
]