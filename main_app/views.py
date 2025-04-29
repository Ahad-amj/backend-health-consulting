from rest_framework.views import APIView
from rest_framework.response import Response

# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the healthconsulting api home route!'}
    return Response(content)

class Doctors(APIView):
  def get(self, request):
    print("should be hitting api view")
    content = {'message': "Let's get some doctors!"}
    return Response(content)