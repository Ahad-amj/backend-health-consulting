from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from main_app.models import Doctor, Patient 

User = get_user_model()

class AuthorizationTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('signup')
        self.login_url = reverse('login')
        self.token_refresh_url = reverse('token_refresh')

        self.doctor_data = {
            'username': 'docuser',
            'email': 'doc@example.com',
            'password': 'docpass123',
            'role': 'doctor',
            'name': 'Dr. John',
            'gender': 'M',
            'specialization': 'Cardiology',
            'years_of_experience': 10,
            'hospital_affiliation': 'City Hospital'
        }

        self.patient_data = {
            'username': 'patuser',
            'email': 'pat@example.com',
            'password': 'patpass123',
            'role': 'patient',
            'name': 'Jane Doe',
            'gender': 'F'
        }

    def test_doctor_registration(self):
        response = self.client.post(self.register_url, self.doctor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['role'], 'doctor')
        self.assertTrue(Doctor.objects.filter(user__username='docuser').exists())

    def test_patient_registration(self):
        response = self.client.post(self.register_url, self.patient_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['role'], 'patient')
        self.assertTrue(Patient.objects.filter(user__username='patuser').exists())

    def test_invalid_registration(self):
        response = self.client.post(self.register_url, {'username': 'invalid'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)

    def test_login_doctor(self):
        self.client.post(self.register_url, self.doctor_data, format='json')
        login_data = {'username': 'docuser', 'password': 'docpass123'}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['role'], 'unknown')

    def test_login_patient(self):
        self.client.post(self.register_url, self.patient_data, format='json')
        login_data = {'username': 'patuser', 'password': 'patpass123'}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['role'], 'unknown')
    

    def test_login_invalid_credentials(self):
        response = self.client.post(self.login_url, {'username': 'wrong', 'password': 'wrong'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_token_refresh(self):
        self.client.post(self.register_url, self.patient_data, format='json')
        login_data = {'username': 'patuser', 'password': 'patpass123'}
        login_response = self.client.post(self.login_url, login_data, format='json')

        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        refresh_response = self.client.get(self.token_refresh_url)
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)
        self.assertIn('refresh', refresh_response.data)

    def test_protected_endpoint_requires_authentication(self):
        protected_url = reverse('doctor-index')  
        response = self.client.get(protected_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.post(self.register_url, self.doctor_data, format='json')
        login_response = self.client.post(self.login_url, {'username': 'docuser', 'password': 'docpass123'}, format='json')
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.get(protected_url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_403_FORBIDDEN])  # Adjust based on endpoint

    def tearDown(self):
        self.client.credentials()
