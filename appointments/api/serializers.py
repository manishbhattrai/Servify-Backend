from rest_framework import serializers
from appointments.models import Appointments
from users.models import ProviderProfile
from users.api.serializers import CustomerProfileSerializer


class CreateAppointmentSerializer(serializers.ModelSerializer):

    provider_id = serializers.IntegerField(write_only = True)
    appointment_date = serializers.DateField()
    time = serializers.TimeField()

    class Meta:
        model = Appointments
        fields = ['provider_id','payment_method','extra_notes','time','appointment_date']
    
    def validate_provider_id(self,value):

        try:
            provider = ProviderProfile.objects.get(id=value)
        
        except ProviderProfile.DoesNotExist:
            raise serializers.ValidationError("Provider not found.")
        
        return provider
    

    def create(self, validated_data):

        provider = validated_data.pop('provider_id')
        validated_data['provider'] = provider
        return super().create(validated_data)
        

class CustomerGetAppointmentsSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = Appointments
        fields = ['id','provider','payment_method','status','time','extra_notes','appointment_date','booked_at']


class ProviderAppointmentSerializer(serializers.ModelSerializer):

    customer = CustomerProfileSerializer(read_only = True)
    class Meta:

        model = Appointments
        fields = ['id','customer','payment_method','status','time','extra_notes','appointment_date','booked_at']
    
