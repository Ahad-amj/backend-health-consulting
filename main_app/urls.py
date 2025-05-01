from django.urls import path
from .views import Home, DoctorsIndex, DoctorDetail, MedicineIndex, ReviewListCreateView

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('doctors/', DoctorsIndex.as_view(), name='doctor-index'),
  path('doctors/<int:doctor_id>/', DoctorDetail.as_view(), name='doctor-detail'),
  path('medicines/', MedicineIndex.as_view(), name='medicine-index'),
  path('doctors/<int:doctor_id>/reviews/', ReviewListCreateView.as_view(), name='doctor-reviews'),
]