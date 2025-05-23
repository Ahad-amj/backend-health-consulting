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
            prescriptions = Prescription.objects.filter(doctor=doctor.id)
            return Response({
                   "doctor": serializer.data,
                   "prescriptions": PrescriptionSerializer(prescriptions, many=True).data,
               }, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
class PatientProfileView(APIView):
   
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, doctor_id):
      try:
        doctor = Doctor.objects.get(id=doctor_id)
        patients = Patient.objects.filter(doctor=doctor)
        serializer = PatientSerializer(patients, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

      except Doctor.DoesNotExist:
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
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
        patientQuery = Patient.objects.filter(doctor=doctor_id)
        patientSerial = PatientSerializer(patientQuery, many=True)
        print(patientSerial.data, "test patient data")
        return Response({"doctor": doctor.data, "patients": patientSerial.data}, status=status.HTTP_200_OK)
    except Exception as err:
        return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MedicineIndex(generics.ListCreateAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = MedicineSerializer
  queryset = Medicine.objects.all()


class ReviewListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, doctor_id):
        try:
            reviews = Review.objects.filter(doctor=doctor_id)
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, doctor_id):
        try:
            data = request.data.copy()
            data['doctor'] = doctor_id
            patient = getattr(request.user, 'patient', None)
            data['patient'] = patient
            serializer = ReviewSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReviewDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, review_id):
      try:
        review = Review.objects.get(id=review_id)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_200_OK)
      except Exception as e:
        print(str(e), "check error")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
            review.delete()
            return Response({'message': 'review deleted successfully'}, status=204)
        except Review.DoesNotExist:
            return Response({'error': 'review not found'}, status=404)

    
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

    def put(self, request, prescription_id):
        try:
            prescription = Prescription.objects.get(prescription=prescription_id)
            medicine_id = request.data.get('medicine_id')
            if medicine_id:
                medicine = Medicine.objects.get(prescription=medicine_id)
                prescription.medicine = medicine
                prescription.save()

            serializer = PrescriptionSerializer(prescription)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, prescription_id):
        try:
            prescription = Prescription.objects.get(prescription_id=prescription_id)
            prescription.delete()
            return Response({"message": "Prescription deleted."}, status=status.HTTP_204_NO_CONTENT)

        except Prescription.DoesNotExist:
            return Response({"error": "Prescription not found."}, status=status.HTTP_404_NOT_FOUND)
        
  
class PrescriptionDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, prescription_id):
        try:
            prescription = Prescription.objects.get(id=prescription_id)
            serializer = PrescriptionSerializer(prescription)
            return Response(serializer.data)
        except Prescription.DoesNotExist:
            return Response({'error': 'Prescription not found'}, status=404)

    def put(self, request, prescription_id):
        try:
            prescription = Prescription.objects.get(id=prescription_id)
            medicine = Medicine.objects.get(id=request.data["medicine"])
            serializer = PrescriptionSerializer(prescription, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(medicine=medicine)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_200_OK)
        except Prescription.DoesNotExist:
            return Response({'error': 'Prescription not found'}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, prescription_id):
        try:
            prescription = Prescription.objects.get(id=prescription_id)
            prescription.delete()
            return Response({'message': 'Prescription deleted successfully'}, status=204)
        except Prescription.DoesNotExist:
            return Response({'error': 'Prescription not found'}, status=404)

        
class PatientsPrescriptionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, patient_id):
        prescriptions = Prescription.objects.filter(patient=patient_id)
        serializer = PrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data)
       