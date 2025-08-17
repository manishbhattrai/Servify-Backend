from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):

    email = models.EmailField(unique=True)

    ROLE_CHOICES = [

        ('c','Customer'),
        ('p','provider'),
    ]

    role = models.CharField(choices=ROLE_CHOICES, max_length=20, default='c')
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class CustomerProfile(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='customer/')
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200)
    address = models.TextField()
    is_profile_complete = models.BooleanField(default= False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    '''def is_complete(self):

        required_fields = [

            self.image,
            self.first_name,
            self.last_name,
            self.address,
        ]

        return all(required_fields)'''


    def __str__(self):
        return f"{self.user.username}'s profile."
    

class ProviderProfile(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to= 'provider/')
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200)
    bio = models.TextField(null=True, blank=True)
    experience_years = models.IntegerField(default=0)
    address = models.TextField()
    service_category = models.CharField(max_length=100)
    is_profile_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    '''def is_complete(self):

        required_fields = [

            self.image,
            self.first_name,
            self.last_name,
            self.experience_years,
            self.address,
            self.service_category,
        ]

        return all(required_fields) '''
    
    def __str__(self):
        
        return f"{self.user.username}'s profile."
