from django.urls import path
from .views import Home, DoctorsIndex, DoctorDetail, MedicineIndex, ReviewListCreateView, CreateUserView, LoginView, VerifyUserView, ReviewReplyView, PrescribeMedicineView

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('doctors/', DoctorsIndex.as_view(), name='doctor-index'),
  path('doctors/<int:doctor_id>/', DoctorDetail.as_view(), name='doctor-detail'),
  path('medicines/', MedicineIndex.as_view(), name='medicine-index'),
  path('doctors/<int:doctor_id>/reviews/', ReviewListCreateView.as_view(), name='doctor-reviews'),
  path('reviews/<int:review_id>/reply/', ReviewReplyView.as_view(), name='review-reply'),
  path('patients/<int:patient_id>/medicines/<int:medicine_id>/prescribe/', PrescribeMedicineView.as_view(), name='prescribe-medicine'),
  path('prescriptions/<int:pk>/', PrescribeMedicineView.as_view(), name='update-delete-prescription'),
  path('users/signup/', CreateUserView.as_view(), name='signup'),
  path('users/login/', LoginView.as_view(), name='login'),
  path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
]