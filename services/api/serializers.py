from rest_framework import serializers
from services.models import BaseService, ProviderService



class BaseServiceSerializer(serializers.ModelSerializer):

    class Meta:

        model = BaseService
        fields = ['id','name','description','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at']


class ProviderServiceSerializer(serializers.ModelSerializer):

    services = BaseServiceSerializer(read_only = True)
    service_id = serializers.PrimaryKeyRelatedField(

                queryset = BaseService.objects.all(),
                source = 'services',
                write_only = True
    )

    class Meta:

        model = ProviderService
        fields = ['id','provider','service_id','services','price','created_at','updated_at']
        read_only_fields = ['id','provider','created_at','updated_at']
    

    def validate_price(self,value):

        if value < 0 or value > 100000:
            raise serializers.ValidationError("Price should be reasonable.")
        
        return value
    
