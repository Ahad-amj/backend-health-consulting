from django.urls import path
from .views import Home, DoctorsIndex, DoctorDetail, MedicineIndex, ReviewListCreateView, CreateUserView, LoginView, PatientsPrescriptionsView, VerifyUserView, PrescribeMedicineView, PatientProfileView, PrescriptionDetailView, ReviewDetailView

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('doctors/', DoctorsIndex.as_view(), name='doctor-index'),
  path('doctors/<int:doctor_id>/', DoctorDetail.as_view(), name='doctor-detail'),
  path('doctors/<int:doctor_id>/patients/', PatientProfileView.as_view(), name='patients'),
  path('medicines/', MedicineIndex.as_view(), name='medicine-index'),
  path('doctors/<int:doctor_id>/reviews/', ReviewListCreateView.as_view(), name='doctor-reviews'),
  path('reviews/<int:review_id>/', ReviewDetailView.as_view(), name='review-detail'),
  path('doctors/<int:doctor_id>/prescriptions/', PrescribeMedicineView.as_view(), name='doctor-prescription'),
  path('patients/<int:patient_id>/medicines/<int:medicine_id>/prescribe/', PrescribeMedicineView.as_view(), name='prescribe-medicine'),
  path('prescriptions/<int:prescription_id>/', PrescriptionDetailView.as_view(), name='prescribe-detail'),
  path('prescriptions/patients/<int:patient_id>/', PatientsPrescriptionsView.as_view(), name='patient-prescriptions-detail'),
  path('users/signup/', CreateUserView.as_view(), name='signup'),
  path('users/login/', LoginView.as_view(), name='login'),
  path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
]