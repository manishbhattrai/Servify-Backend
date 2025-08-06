from django.test import TestCase
from rest_framework.test import APIClient,APITestCase
from .models import BaseService, ProviderService
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
##from .api.serializers import BaseServiceSerializer

# Create your tests here.

User = get_user_model()



class ProviderServiceTest(APITestCase):


    def setUp(self):
        
        self.customer_user = User.objects.create(

            username = 'test',
            email = 'test@gmail.com',
            password = 'testme@1234',
            role = 'c'
        )

        self.provider_user = User.objects.create(

            username = 'provider',
            email = 'provider@gmail.com',
            password = 'provider@123',
            role = 'p'
        )

        self.provider_user_2 = User.objects.create(

            username = 'provider2',
            email = 'provider2@gmail.com',
            password = 'provider@123',
            role = 'p'
        )


        self.service = BaseService.objects.create(

            name = 'plumber',
            description = 'fixes pump'
        )

        self.provider_service = ProviderService.objects.create(
            
            provider=self.provider_user,
            services=self.service,
            price=200
        )

        self.provider_service_2 = ProviderService.objects.create(
            
            provider=self.provider_user_2,
            services=self.service,
            price=500
        )


        self.client = APIClient()
    
    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    
    def test_create_provider_service(self):
        

        self.authenticate(self.provider_user)

        url = reverse('provider-services-list')


        data = {
            "service_id":self.service.id,
            "price":200
        }

        response = self.client.post(url, data, format='json')

        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['services']['name'], "plumber")
    
    def test_customer_cannot_create_provider_service(self):

        self.authenticate(self.customer_user)

        url = reverse('provider-services-list')

        data = {
            "service_id":self.service.id,
            "price":200
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_own_services(self):

        self.authenticate(self.provider_user)

        url = reverse('provider-services-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['services']['name'], 'plumber')
        self.assertEqual(response.data[0]['price'], "200.00") 
    
    def test_can_update_own_service(self):

        self.authenticate(self.provider_user)

        url = reverse('provider-services-detail', args=[self.provider_service.id])

        data = {

            "price":400
        }

        response = self.client.patch(url, data, format='json')
        
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_cannot_update_others_service(self):

        self.authenticate(self.provider_user_2)

        url = reverse('provider-services-detail', args=[self.provider_service.id])

        data = {
        
            "price": 400
        }

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_own_service(self):

        self.authenticate(self.provider_user_2)

        url = reverse('provider-services-detail', args=[self.provider_service_2.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_cannot_delete_other_service(self):

        self.authenticate(self.provider_user_2)

        url = reverse('provider-services-detail', args=[self.provider_service.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class BaseServiceTest(APITestCase):

    def setUp(self):
        
        self.superuser = User.objects.create_superuser(

            username = 'admin',
            email='admin@gmail.com',
            password='password12345'
        )

        self.user = User.objects.create(

            username = 'admin1',
            email='admin1@gmail.com',
            password='password12345',
            role = 'c'
        )

        self.base_service = BaseService.objects.create(

            name = 'plumber',
            description = 'this is a plumber'
        )

        self.base_service_2 = BaseService.objects.create(

            name = 'driver',
            description = 'this is a driver'
        )

        self.client = APIClient()
    
    def authenticate(self, user):

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION = f" Bearer {access_token}")
    

    def test_admin_can_create(self):

        self.authenticate(self.superuser)

        url = reverse('base-services-list')

        data = {

            "name":"plumber",
            "description":"this is plumber"
        }

        response = self.client.post(url,data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'],"plumber")
    
    def test_only_admin_can_create(self):

        self.authenticate(self.user)

        url = reverse('base-services-list')

        data = {

            "name":"plumber",
            "description":"this is plumber"
        }

        response = self.client.post(url,data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_only_admin_can_get_services(self):

        self.authenticate(self.user)

        url = reverse('base-services-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_only_admin_can_update_services(self):

        self.authenticate(self.user)

        url = reverse('base-services-detail', args=[self.base_service.id])

        data = {

            "name":"driver",
            
        }

        response = self.client.patch(url,data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_only_admin_can_delete_services(self):

        self.authenticate(self.user)

        url = reverse('base-services-detail',args=[self.base_service_2.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
