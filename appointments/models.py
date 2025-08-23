from django.db import models
from django.contrib.auth import get_user_model
from users.models import ProviderProfile

# Create your models here.

User = get_user_model()

class Appointments(models.Model):

    STATUS_CHOICES = [

        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled')
    ]

    PAYMENT_CHOICES = [

        ('cash','Cash'),
        ('online', 'Online')
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment_made')
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name='appointment_received')
    status = models.CharField(max_length=20,choices=STATUS_CHOICES, default='pending')
    time = models.TimeField()
    payment_method = models.CharField(max_length=20,choices=PAYMENT_CHOICES, default='cash')
    extra_notes = models.TextField(null=True, blank=True)
    appointment_date = models.DateField()
    booked_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    