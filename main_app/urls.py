from django.urls import path
from .views import Home, Doctors

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('doctors/', Doctors.as_view(), name='doctor-index'),
]