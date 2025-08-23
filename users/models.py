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
    


class skill(models.Model):

    SKILL_CHOICES = [
    ('Plumbing', 'Plumbing'),
    ('Electrical Work', 'Electrical Work'),
    ('Carpentry', 'Carpentry'),
    ('Painting', 'Painting'),
    ('Cleaning', 'Cleaning'),
    ('Gardening', 'Gardening'),
    ('AC Repair', 'AC Repair'),
    ('Appliance Repair', 'Appliance Repair'),
    ('Tutoring', 'Tutoring'),
    ('Web Development', 'Web Development'),
    ('Graphic Design', 'Graphic Design'),
    ('Photography', 'Photography'),
    ('Catering', 'Catering'),
    ('Beauty Services', 'Beauty Services'),
    ('Massage Therapy', 'Massage Therapy'),
    ('Pet Care', 'Pet Care'),
    ('House Sitting', 'House Sitting'),
    ('Moving Services', 'Moving Services'),
    ('Car Wash', 'Car Wash'),
    ('Laundry Services', 'Laundry Services'),
    ]

    name = models.CharField(choices=SKILL_CHOICES, max_length=59)

    def __str__(self):
        return self.name
    
class ProviderProfile(models.Model):

    GENDER_CHOICES = [

        ('m','Male'),
        ('f', 'Female'),
        ('o','Others'),
    ]

    WORKING_HOUR_CHOICES = [
    ('24/7 Availability', '24/7 Availability'),
    ('Morning (6 AM - 12 PM)', 'Morning (6 AM - 12 PM)'),
    ('Afternoon (12 PM - 6 PM)', 'Afternoon (12 PM - 6 PM)'),
    ('Evening (6 PM - 10 PM)', 'Evening (6 PM - 10 PM)'),
    ('Night (10 PM - 6 AM)', 'Night (10 PM - 6 AM)'),
    ('Flexible Hours', 'Flexible Hours'),
    ]

    SERVICE_AREA_CHOICES = [
    ('Kathmandu', 'Kathmandu'),
    ('Lalitpur', 'Lalitpur'),
    ('Bhaktapur', 'Bhaktapur'),
    ('Birtamode', 'Birtamode'),
    ('Bhadrapur', 'Bhadrapur'),
    ('Biratnagar', 'Biratnagar'),
    ('Pokhara', 'Pokhara'),
    ('Nepalgunj', 'Nepalgunj'),
    ('Butwal', 'Butwal'),
    ('Hetauda', 'Hetauda'),
    
    ]

    AVAILABILITY_CHOICES = [
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time'),
    ('Weekends Only', 'Weekends Only'),
    ('Flexible', 'Flexible'),
    ]


    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to= 'provider/')
    ##first_name = models.CharField(max_length=200)
    ##middle_name = models.CharField(max_length=200, null=True, blank=True)
    full_name = models.CharField(max_length=220)
    ##last_name = models.CharField(max_length=200)
    ##bio = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15)
    service_area = models.CharField(max_length=50, choices=SERVICE_AREA_CHOICES)
    hourly_rate = models.DecimalField(decimal_places=2, max_digits=5)
    gender = models.CharField(choices=GENDER_CHOICES, default='m', max_length=12)
    experience_years = models.IntegerField(default=0)
    address = models.TextField()
    ##service_category = models.CharField(max_length=100)
    working_hours = models.CharField(max_length=50, choices= WORKING_HOUR_CHOICES, default='Flexible')
    availability = models.CharField(max_length=50,choices=AVAILABILITY_CHOICES ,null=True, blank=True)
    available_skills = models.ManyToManyField(skill)
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
