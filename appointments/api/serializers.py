from rest_framework import serializers
from appointments.models import Appointments


class CreateAppointmentSerializer(serializers.ModelSerializer):


    class Meta:
        model = Appointments
        fields = ['provider','payment_method','extra_notes','appointment_date']
    
    def validate_provider(self,value):

        if value.role != 'p':
            raise serializers.ValidationError("You cannot book an appointment without a provider.")
        
        return value
    


class CustomerGetAppointmentsSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = Appointments
        fields = ['id','provider','payment_method','status','extra_notes','appointment_date','booked_at']
