from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from .models import Doctor, Medicine, Review
from .serializers import DoctorSerializer, MedicineSerializer, ReviewSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the healthconsulting api home route!'}
    return Response(content)

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
        reviews = Review.objects.filter(doctor_id=doctor_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, doctor_id):
        print("DATA RECEIVED:", request.data)
        data = request.data.copy()
        data['doctor'] = doctor_id
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("ERRORS:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LoginView(APIView):

  def post(self, request):
    try:
      username = request.data.get('username')
      password = request.data.get('password')
      user = authenticate(username=username, password=password)
      if user:
        refresh = RefreshToken.for_user(user)
        content = {'refresh': str(refresh), 'access': str(refresh.access_token),'user': UserSerializer(user).data}
        return Response(content, status=status.HTTP_200_OK)
      return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as err:
      return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    try:
      response = super().create(request, *args, **kwargs)
      user = User.objects.get(username=response.data['username'])
      refresh = RefreshToken.for_user(user)
      content = {'refresh': str(refresh), 'access': str(refresh.access_token), 'user': response.data }
      return Response(content, status=status.HTTP_201_CREATED)
    except Exception as err:
      return Response({ 'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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