from rest_framework import serializers
from users.models import CustomerProfile, ProviderProfile
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomerRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only = True)
    password2 = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ['username','email','password','password2']
    
    def validate_username(self, value):

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        
        if len(value) <= 4:
            raise serializers.ValidationError("Username should contain more than 4 words.")
        
        return value
    

    def validate_email(self,value):

        if User.objects.filter(email__iexact = value).exists():
            raise serializers.ValidationError("Email already exists.")
        
        return value
    
    def validate(self, attrs):

        password = attrs.get('password')
        password2 = attrs.get('password2')

        if len(password2) < 8:
            raise serializers.ValidationError("Password must be more than 8 characters.")
        
        if password != password2:
            raise serializers.ValidationError("Password didn't match.")


        return attrs
    
    def create(self, validated_data):
        
        username = validated_data.get('username')
        password = validated_data.get('password')
        email = validated_data.get('email')
        validated_data.pop('password2')

        user = User.objects.create(

                    username=username,
                    email =email,
                    )
        user.set_password(password)
        user.save()


        return user
        

class ProviderRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only = True)
    password2 = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ['username','email','password','password2']
    
    def validate_username(self, value):

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        
        if len(value) <= 4:
            raise serializers.ValidationError("Username should contain more than 4 words.")
        
        return value
    

    def validate_email(self,value):

        if User.objects.filter(email__iexact = value).exists():
            raise serializers.ValidationError("Email already exists.")
        
        return value
    
    def validate(self, attrs):

        password = attrs.get('password')
        password2 = attrs.get('password2')

        if len(password2) < 8:
            raise serializers.ValidationError("Password must be more than 8 characters.")
        
        if password != password2:
            raise serializers.ValidationError("Password didn't match.")


        return attrs
    
    def create(self, validated_data):
        
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        validated_data.pop('password2')


        user = User.objects.create(username=username, email=email, role = 'p')
        user.set_password(password)
        user.save()


        return user


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(required= True)
    password = serializers.CharField(write_only = True, required=True)


    def validate_email(self, value):

        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email not found.")

        return value
    
    def validate_password(self,value):

        if len(value) < 8:
            raise serializers.ValidationError("Password should be more than 8 characters.")

        return value

class ChangePasswordSerializer(serializers.Serializer):

    current_password = serializers.CharField(write_only = True, required = True)
    new_password = serializers.CharField(write_only = True, required = True)
    confirm_password = serializers.CharField(write_only = True, required = True)
    
    def validate(self, attrs):

        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError("Password didn't match.")
        
        if len(confirm_password) < 8:
            raise serializers.ValidationError("Password should be more than 8 characters.")
        
        return attrs

'''class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField(required = True)


    def validate(self, attrs):

        email = attrs.get('email')

        try:
            User.objects.get(email=email)
        
        except User.DoesNotExist:
            raise serializers.ValidationError("Email doesnot exists.")
        
        return attrs

class ResetPasswordSerializer(serializers.Serializer):

    new_password = serializers.CharField(write_only = True, required = True)

    def validate(self, attrs):

        new_password = attrs.get('new_password')

        if len(new_password) < 8:
            raise serializers.ValidationError("Password should be more than 8 characters.")

        return attrs'''

            

class CustomerProfileSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(validators =[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png'])])

    class Meta:
        model = CustomerProfile
        fields = ['id','image','first_name','middle_name','last_name','address']
        read_only_fields = ['user','created_at','updated_at']

    
    def validate_image(self, value):

        MAX_SIZE = 6*1024*1024

        if value.size > MAX_SIZE:
            raise serializers.ValidationError("Image size should be less than 6MB.")

        return value
    
    def create(self, validated_data):

        user = self.context['request'].user
        profile = CustomerProfile.objects.create(user=user,**validated_data, is_profile_complete = True)

        return profile
    
    def update(self, instance, validated_data):

        image = validated_data.get('image',None)

        if image:
            instance.image = image

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.address = validated_data.get('address', instance.address)

        instance.save()

        return instance

class ProviderProfileSerializer(serializers.ModelSerializer):

    image = serializers.ImageField( validators = [FileExtensionValidator (allowed_extensions= ['jpg','jpeg','png'])])

    class Meta:
        model = ProviderProfile
        fields = ['id','full_name','image','phone','service_area','hourly_rate','gender',
                  'experience_years','address','availability']
        
        read_only_fields = ['user','created_at','updated_at']
        
    
    def validate_image(self, value):

        MAX_SIZE = 6*1024*1024

        if value.size > MAX_SIZE:
            raise serializers.ValidationError("Image should be less than 50MB.")

        return value
    
    def validate_experience_years(self, value):

        if  value < 0 or value > 50:
            raise serializers.ValidationError("Add proper experiences.")
        

        return value
    

    def create(self, validated_data):

        user = self.context['request'].user
        profile = ProviderProfile.objects.create(user=user, **validated_data, is_profile_complete = True)
        
        return profile
    
    def update(self, instance, validated_data):

        image = validated_data.get('image', None)

        if image:
            instance.image = image

        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.service_area = validated_data.get('service_area', instance.service_area)
        instance.hourly_rate = validated_data.get('hourly_rate', instance.hourly_rate)
        instance.address = validated_data.get('address', instance.address)
        instance.experience_years = validated_data.get('experience_years', instance.experience_years)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.availability = validated_data.get('availability', instance.availability)
 
        instance.save()

        return instance