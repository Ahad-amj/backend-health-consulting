from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from .models import Doctor, Medicine, Review, Patient, Prescription
from .serializers import DoctorSerializer, MedicineSerializer, ReviewSerializer, UserSerializer, PatientSerializer,PrescriptionSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the healthconsulting api home route!'}
    return Response(content)

class LoginView(APIView):
  def post(self, request):
    try:
      username = request.data.get('username')
      password = request.data.get('password')
      user = authenticate(username=username, password=password)

      if user:
        role = 'unknown'
        if hasattr(user, 'doctor'):
          role = 'doctor'
        elif hasattr(user, 'patient'):
          role = 'patient'

        refresh = RefreshToken.for_user(user)
        content = {
          'refresh': str(refresh),
          'access': str(refresh.access_token),
          'user': UserSerializer(user).data,
          'role': role
        }
        return Response(content, status=status.HTTP_200_OK)

      return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as err:
      return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    try:
      role = request.data.get('role')  
      response = super().create(request, *args, **kwargs)
      user = User.objects.get(username=response.data['username'])

      if role == 'doctor':
        Doctor.objects.create(
          user=user,
          name=request.data.get('name'),
          gender=request.data.get('gender'),
          specialization=request.data.get('specialization'),
          years_of_experience=request.data.get('years_of_experience'),
          hospital_affiliation=request.data.get('hospital_affiliation')
        )
      elif role == 'patient':
        Patient.objects.create(
          user=user,
          name=request.data.get('name'),
          gender=request.data.get('gender')
        )

      refresh = RefreshToken.for_user(user)
      content = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': response.data,
        'role': role
      }
      return Response(content, status=status.HTTP_201_CREATED)
    except Exception as err:
      return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    try:
      user = User.objects.get(username=request.user.username)
      try:
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh),'access': str(refresh.access_token),'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
      except Exception as token_error:
        return Response({"detail": "Failed to generate token.", "error": str(token_error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as err:
      return Response({"detail": "Unexpected error occurred.", "error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class DoctorProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            doctor = Doctor.objects.get(user=request.user)
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
class PatientProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
            serializer = PatientSerializer(patient)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response({'error': 'Doctor profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
class DoctorsIndex(APIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = DoctorSerializer

  def get(self, request):
    try:
      queryset = Doctor.objects.all()
      serializer = self.serializer_class(queryset, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as err:
      return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
class DoctorDetail(APIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = DoctorSerializer
  lookup_field = 'id'

  def get(self, request, doctor_id):
    try:
        queryset = Doctor.objects.get(id=doctor_id)
        doctor = DoctorSerializer(queryset)
        return Response(doctor.data, status=status.HTTP_200_OK)
    except Exception as err:
        return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MedicineIndex(generics.ListCreateAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = MedicineSerializer
  queryset = Medicine.objects.all()


class ReviewListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, doctor_id):
        reviews = Review.objects.filter(doctor=doctor_id)
        print(reviews)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, doctor_id):
        data = request.data.copy()
        print(data)
        data['doctor'] = doctor_id
        patient = getattr(request.user, 'patient', None)
        print(patient)
        data['patient'] = patient
        # if not patient:
        #     return Response({'error': 'Only patients can leave reviews'}, status=status.HTTP_403_FORBIDDEN)
        # data['patient'] = patient.id
    
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, doctor_id):
        review_id = request.data.get("id")
        # if not review_id:
        #     return Response({'error': 'Review ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        review = get_object_or_404(Review, id=review_id, doctor=doctor_id)
        # review = Review.objects.get(doctor=doctor_id)

        # print(review.patient.user, request.user)
        # if review.patient.user != request.user:
        #     return Response({'error': 'You are not authorized to edit this review'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, doctor_id):
        review_id = request.data.get("id")
        # if not review_id:
        #     return Response({'error': 'Review ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        review = get_object_or_404(Review, id=review_id, doctor=doctor_id)
        # review = Review.objects.get(doctor=doctor_id)

        # if review.patient.user != request.user:
        #     return Response({'error': 'You are not authorized to delete this review'}, status=status.HTTP_403_FORBIDDEN)

        review.delete()
        return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
  

        
    
class ReviewReplyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, doctor_id):
        reviews = Review.objects.filter(doctor=doctor_id)
        print(reviews)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
    
        if not hasattr(request.user, 'doctor') or review.doctor.user != request.user:
            return Response({'error': 'You are not authorized to reply to this review'}, status=status.HTTP_403_FORBIDDEN)
    
        reply = request.data.get('reply')
        if not reply:
            return Response({'error': 'Reply content is required'}, status=status.HTTP_400_BAD_REQUEST)
    
        review.reply = reply
        review.save()
    
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)

        if not hasattr(request.user, 'doctor') or review.doctor.user != request.user:
            return Response({'error': 'You are not authorized to reply to this review'}, status=status.HTTP_403_FORBIDDEN)

        reply = request.data.get('reply')
        if reply is None:
            return Response({'error': 'Reply content is required'}, status=status.HTTP_400_BAD_REQUEST)

        review.reply = reply
        review.save()
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)

        if not hasattr(request.user, 'doctor') or review.doctor.user != request.user:
            return Response({'error': 'You are not authorized to delete this reply'}, status=status.HTTP_403_FORBIDDEN)

        review.reply = ''
        review.save()
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)



class PrescribeMedicineView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, doctor_id):
        prescriptions = Prescription.objects.filter(doctor=doctor_id)
        serializer = PrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data)

    def post(self, request, patient_id, medicine_id):
        try:
            patient = Patient.objects.get(pk=patient_id)
            medicine = Medicine.objects.get(pk=medicine_id)
            doctor = patient.doctor

            prescription = Prescription.objects.create(patient=patient, doctor=doctor, medicine=medicine )
            serializer = PrescriptionSerializer(prescription)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            prescription = Prescription.objects.get(pk=pk)
            medicine_id = request.data.get('medicine_id')
            if medicine_id:
                medicine = Medicine.objects.get(pk=medicine_id)
                prescription.medicine = medicine
                prescription.save()

            serializer = PrescriptionSerializer(prescription)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            prescription = Prescription.objects.get(pk=pk)
            prescription.delete()
            return Response({"message": "Prescription deleted."}, status=status.HTTP_204_NO_CONTENT)

        except Prescription.DoesNotExist:
            return Response({"error": "Prescription not found."}, status=status.HTTP_404_NOT_FOUND)