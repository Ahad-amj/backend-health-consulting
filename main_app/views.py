from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Doctor, Medicine
from .serializers import DoctorSerializer, MedicineSerializer

class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the healthconsulting api home route!'}
    return Response(content)

class DoctorsIndex(APIView):
  serializer_class = DoctorSerializer

  def get(self, request):
    try:
      queryset = Doctor.objects.all()
      serializer = self.serializer_class(queryset, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as err:
      return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
class DoctorDetail(APIView):
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
  serializer_class = MedicineSerializer
  queryset = Medicine.objects.all()