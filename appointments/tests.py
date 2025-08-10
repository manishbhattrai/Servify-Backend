from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from .models import Appointments
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from rest_framework import status

# Create your tests here.

User = get_user_model()


class AppointmentTestCase(APITestCase):


    def setUp(self):
        
        self.customer_user = User.objects.create(

            username = 'test',
            email = 'test@gmail.com',
            password = 'test@12345',
            role = 'c'
        )

        self.customer_user_2 = User.objects.create(

            username = 'test3',
            email = 'test3@gmail.com',
            password = 'test@12345',
            role = 'c'
        )

        self.provider_user = User.objects.create(

            username = 'test1',
            email = 'test1@gmail.com',
            password = 'test123456',
            role = 'p'
        )

        self.provider_user_2 = User.objects.create(

            username = 'test2',
            email = 'test2@gmail.com',
            password = 'test123456',
            role = 'p'
        )

        self.customer_appointments = Appointments.objects.create(

            customer = self.customer_user,
            provider = self.provider_user,
            status = 'pending',
            payment_method = 'cash',
            extra_notes = 'hi hi hi',
            appointment_date = '2025-08-15T14:30:00Z'
        )

        self.customer_appointments_2 = Appointments.objects.create(

            customer = self.customer_user_2,
            provider = self.provider_user,
            status = 'pending',
            payment_method = 'cash',
            extra_notes = 'hi hi hi',
            appointment_date = '2025-08-15T14:30:00Z'
        )

        self.client = APIClient()
    
    def authenticate(self,user):

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION = f" Bearer {access_token}")
    

    def test_create_appointments(self):

        self.authenticate(self.customer_user)

        url = reverse('create-appointment')

        data = {

            "provider":self.provider_user.id,
            "payment_method":"cash",
            "appointment_date":"2025-08-15T14:30:00Z"
        }

        response = self.client.post(url, data, format='json')
        print(response.status_code)


        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['payment_method'],"cash")
    
    def test_only_customer_can_create_appointments(self):

        self.authenticate(self.provider_user)

        url = reverse('create-appointment')

        data = {

            "provider":self.provider_user_2.id,
            "payment_method":"cash",
            "appointment_date":"2025-08-15T14:30:00Z"
        }

        response = self.client.post(url, data, format='json')


        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    
    def test_get_own_appointments(self):

        self.authenticate(self.customer_user)

        url = reverse('get-appointments')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['payment_method'], 'cash')
        self.assertEqual(len(response.data), 1)
    
    def test_cancel_appointment(self):

        self.authenticate(self.customer_user_2)

        
        
        url = reverse('update-appointments', kwargs={'id':self.customer_appointments_2.id})

        data = {

            'status':'cancelled'
        }

        response = self.client.patch(url,data,format='json')

        print(response.status_code)
        

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_can_only_update_own_appointment_status(self):

        self.authenticate(self.customer_user)

        
        
        url = reverse('update-appointments', kwargs={'id':self.customer_appointments_2.id})

        data = {

            'status':'cancelled'
        }

        response = self.client.patch(url,data,format='json')

        print(response.status_code)
        

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class ProviderAppointmentTestCase(APITestCase):

    def setUp(self):

        self.customer_user = User.objects.create(

            username = 'provider3',
            email = 'provider3@gmail.com',
            password = 'provider12345',
            role = 'c'
        )
        
        self.provider_user = User.objects.create(

            username = 'provider',
            email = 'provider@gmail.com',
            password = 'provider12345',
            role = 'p'
        )

        self.provider_user_1 = User.objects.create(

            username = 'provider1',
            email = 'provider1@gmail.com',
            password = 'provider123456',
            role = 'p'
        )

        self.appointment_1 = Appointments.objects.create(

            customer = self.customer_user,
            provider = self.provider_user,
            status = 'pending',
            payment_method = 'cash',
            extra_notes = 'hi hi hi',
            appointment_date = '2025-08-15T14:30:00Z'
        )

        self.appointment_2 = Appointments.objects.create(

            customer = self.customer_user,
            provider = self.provider_user_1,
            status = 'pending',
            payment_method = 'cash',
            extra_notes = 'hi hi hi',
            appointment_date = '2025-08-15T14:30:00Z'
        )

        self.client = APIClient()
    
    def authenticate(self,user):

        refresh = RefreshToken.for_user(user)
        access_token  = refresh.access_token

        self.client.credentials(HTTP_AUTHORIZATION = f" Bearer {access_token}")
    
    def test_get_list_of_appointments(self):

        self.authenticate(self.provider_user)

        url = reverse('provider-appointment-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['payment_method'],"cash")
    
    def test_retrieve_single_appointments(self):

        self.authenticate(self.provider_user)
        url = reverse('provider-appointment-details', kwargs={'id':self.appointment_1.id})

        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['payment_method'], "cash")
    
    def test_update_appointment_status(self):

        self.authenticate(self.provider_user)
        url = reverse('provider-appointment-details', kwargs={'id':self.appointment_1.id})

        data = {
            "status":"approved"
        }

        response = self.client.patch(url, data, format='json')

        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_provider_cannot_update_non_pending_appointments(self):

        self.authenticate(self.provider_user)

        self.appointment_1.status = 'approved'
        self.appointment_1.save()

        url = reverse('provider-appointment-details', kwargs={'id':self.appointment_1.id})
        data = {
            "status":"rejected"
        }

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_provider_cannot_set_invalid_status(self):

        self.authenticate(self.provider_user)

        url = reverse('provider-appointment-details', kwargs={'id':self.appointment_1.id})
        data = {
            "status":"completed"
        }

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
