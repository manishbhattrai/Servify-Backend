from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class BaseService(models.Model):

    name = models.CharField(max_length=220)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProviderService(models.Model):

    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='provider_services', limit_choices_to={'role':'provider'})
    services = models.ForeignKey(BaseService, on_delete = models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:

        unique_together = ('provider', 'services')
    

    def __str__(self):
        return f"{self.services} used by {self.provider.username}."
    
