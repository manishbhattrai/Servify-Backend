from django.db import models
##from django.contrib.auth import get_user_model

# Create your models here.

'''User = get_user_model()

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
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment_received')
    status = models.CharField(choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(choices=PAYMENT_CHOICES, default='cash')
    extra_notes = models.TextField(null=True)
    appointment_date = models.DateTimeField()
    booked_at = models.DateTimeField(auto_now=True) '''
    