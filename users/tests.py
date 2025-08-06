from django.test import TestCase
from rest_framework.test import APIClient,APITestCase
from users.models import CustomerProfile, ProviderProfile
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework_simplejwt.tokens import RefreshToken 
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse

User = get_user_model()
# Create your tests here.

class CustomerProfileAPITest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="profile_owner",
            email="owner@test.com",
            password="testpassword123"
        )
        self.other_user = User.objects.create_user(
            username="other_user",
            email="other@test.com",
            password="testpassword123"
        )

        self.profile = CustomerProfile.objects.create(
            user=self.user,
            first_name="Jane",
            last_name="Doe",
            address="123 Main St"
        )

        self.client = APIClient()

    def authenticate(self,user):

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION = F'Bearer {access_token}')


    def test_create_customer_profile(self):
       
        self.authenticate(self.other_user)
        
        url = reverse('customer-profile')
        
        image = SimpleUploadedFile("test_pic.jpg",
                                    b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\xff\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b", 
                                    content_type="image/jpeg")
        data = {
            "first_name": "John",
            "last_name": "Smith",
            "address": "456 Oak Ave, Anytown",
            "image": image,
        }

        response = self.client.post(url, data, format='multipart')

        print("Response status:", response.status_code)
        print("Response data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertTrue(CustomerProfile.objects.filter(user=self.other_user).exists())
        new_profile = CustomerProfile.objects.get(user=self.other_user)
        self.assertEqual(new_profile.first_name, "John")
        self.assertEqual(response.data['address'], "456 Oak Ave, Anytown")
    
    def test_cannot_create_profile_if_one_exitst(self):

        self.authenticate(self.user)

        url = reverse('customer-profile')

        data = {
            "first_name":"manish",
            "middle_name":"bhattarai",
            "address":"birtamode"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_retireve_own_profile(self):

        self.authenticate(self.user)

        url = reverse('customer-profile')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "Jane")
        self.assertEqual(response.data['last_name'], "Doe") 
    
    def test_retireve_others_profile(self):

        self.authenticate(self.other_user)

        url = reverse('customer-profile-get', kwargs={"id":self.profile.id})

        response  = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "Jane")
        self.assertEqual(response.data['last_name'], "Doe")
    

    def test_update_own_profile(self):

        self.authenticate(self.user)

        data = {

            "first_name": "manish",
            "last_name": "bhattarai"
        }

        url = reverse('customer-profile')

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "manish")
        self.assertEqual(response.data['last_name'], "bhattarai")
    
    def test_update_others_profile(self):

        self.authenticate(self.other_user)

        data ={
            "first_name":"ram",
            "last_name":"shyam"
        }

        url = reverse('customer-profile')

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class ProviderProfileAPITest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="owner",
            email="Powner@test.com",
            password="testpassword123"
        )
        self.other_user = User.objects.create_user(
            username="other_owner",
            email="otherO@test.com",
            password="testpassword123"
        )

        self.profile = ProviderProfile.objects.create(

            user=self.user,
            first_name="manish",
            last_name="bhattarai",
            address="charpane",
            bio = "i am new here",
            experience_years = 1,
            service_category="plumber"
        )

        self.client = APIClient()

    def authenticate(self,user):

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION = F'Bearer {access_token}')


    def test_create_provider_profile(self):
       
        self.authenticate(self.other_user)
        
        url = reverse('provider-profile')
        
        image = SimpleUploadedFile("test_pics.jpg",
                                    b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\xff\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b", 
                                    content_type="image/jpeg")
        data = {
            "first_name": "tyson",
            "last_name": "Smith",
            "address": "456 Oak Ave, Anytown",
            "image": image,
            "bio": "I am new here",
            "experience_years": 1,
            "service_category": "electrician"
        }

        response = self.client.post(url, data, format='multipart')

        print("Response status:", response.status_code)
        print("Response data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertTrue(ProviderProfile.objects.filter(user=self.other_user).exists())
        new_profile = ProviderProfile.objects.get(user=self.other_user)
        self.assertEqual(new_profile.first_name, "tyson")
        self.assertEqual(response.data['address'], "456 Oak Ave, Anytown")
    
    def test_cannot_create_profile_if_already_exitst(self):

        self.authenticate(self.user)

        url = reverse('provider-profile')

        data = {
            "first_name":"manisha",
            "middle_name":"bhattaraii",
            "address":"birtamode-02",
            "bio": "I am new here",
            "experience_years": 2,
            "service_category": "electrician"

        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_retireve_self_profile(self):

        self.authenticate(self.user)

        url = reverse('provider-profile')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "manish")
        self.assertEqual(response.data['last_name'], "bhattarai") 
    
    def test_retireve_other_profile(self):

        self.authenticate(self.other_user)

        url = reverse('provider-profile-get', kwargs={"id":self.profile.id})

        response  = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "manish")
        self.assertEqual(response.data['last_name'], "bhattarai")
    

    def test_update_self_profile(self):

        self.authenticate(self.user)

        data = {

            "first_name": "anish",
            "last_name": "hattarai"
        }

        url = reverse('provider-profile')

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "anish")
        self.assertEqual(response.data['last_name'], "hattarai")
    
    def test_update_other_profile(self):

        self.authenticate(self.other_user)

        data ={
            "first_name":"ram",
            "last_name":"shyam"
        }

        url = reverse('provider-profile')

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 


class ProfileInreactionAPITest(APITestCase):

    def setUp(self):
        
        self.customer_user = User.objects.create(

            username="customer_user",
            email = "customer@gmail.com",
            password = "customeruser"
        )

        self.customer_profile = CustomerProfile.objects.create(

            user=self.customer_user,
            first_name = "customer",
            last_name = "user",
            address = "birtamode-02, jhapa, nepal"
        )

        self.provider_user = User.objects.create(

            username = "Provider_user",
            email = "provider@gmail.com",
            password = "provideruser"
        )

        self.provider_profile = ProviderProfile.objects.create(

            user=self.provider_user,
            first_name="Pat",
            last_name="Provider",
            address="456 Provider Plaza",
            service_category="plumber",
            experience_years = 2
        )
    
    def authenticate(self, user):

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION= f'Bearer {access_token}')
    

    def test_customer_can_view_provider_profile(self):

        self.authenticate(self.customer_user)

        url = reverse('provider-profile-get', kwargs={"id":self.provider_profile.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "Pat")
        self.assertEqual(response.data['service_category'], "plumber")
    

    def test_provider_can_view_customer_profile(self):

        self.authenticate(self.provider_user)

        url = reverse('customer-profile-get', kwargs={"id": self.customer_profile.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "customer")
        self.assertEqual(response.data['last_name'], "user")