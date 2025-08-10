from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema


from .serializers import ( CustomerRegistrationSerializer, ProviderRegistrationSerializer,
                                    CustomerProfileSerializer, ProviderProfileSerializer, LoginSerializer,
                                    ChangePasswordSerializer
                                    )

from users.models import ProviderProfile, CustomerProfile
from .permissions import IsOwnerorUser


User = get_user_model()

@extend_schema(tags=['Customer Registration'])
class UserRegistrationView(APIView):

    permission_classes = [AllowAny]
    serializer_class = CustomerRegistrationSerializer 

    def post(self, request):

        data = request.data
        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

@extend_schema(tags=['Provider Registration'])
class ProviderRegistrationView(APIView):

    permission_classes = [AllowAny]
    serializer_class = ProviderRegistrationSerializer 

    def post(self, request):

        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

@extend_schema(tags=['Login'])
class LoginView(APIView):

    permission_classes = [AllowAny]

    serializer_class = LoginSerializer 

    def post(self, request):

        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():

            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, username = email, password=password)

            user_data = {

                    'username':user.username,
                    'email': user.email,
                    'role': user.role,
                }

            if user is not None:


                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

               


                return Response({

                        'message':'Login sucessfull',
                        'user_data':user_data,
                        'access_token': access_token,
                        'refresh_token': str(refresh)
                }, status=status.HTTP_200_OK)
            
        else:
                return Response({
                    "message":"Invalid Credentials."
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Customer Profile'])
class CustomerProfileView(APIView):


    permission_classes = [IsAuthenticated, IsOwnerorUser]
    serializer_class = CustomerProfileSerializer

    def post(self,request):

        data = request.data
        serializer = self.serializer_class(data=data, context = {'request': request})
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self,request):

        user = request.user
        profile = get_object_or_404(CustomerProfile, user=user)

        data = request.data
        serializer = self.serializer_class(profile, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):

        user = request.user
        profile = get_object_or_404(CustomerProfile, user=user)
        serializer = self.serializer_class(profile)

        return Response(
            serializer.data,
         status=status.HTTP_200_OK)

@extend_schema(tags=['Get Customer Profile Publicly'])
class PublicCustomerProfileView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = CustomerProfileSerializer

    def get(self,request, id):

        profile = get_object_or_404(CustomerProfile, id=id)
        serializer = self.serializer_class(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=['Provider Profile'])
class ProviderProfileView(APIView):

    permission_classes = [IsAuthenticated, IsOwnerorUser]
    serializer_class = ProviderProfileSerializer 

    def post(self, request):

        data = request.data
        serializer = self.serializer_class(data=data, context = {'request': request})
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self,request):

        user = request.user

        profile = get_object_or_404(ProviderProfile, user=user)

        data = request.data

        serializer = self.serializer_class(profile, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):

        user = request.user
        profile = get_object_or_404(ProviderProfile, user=user)
        
        serializer = self.serializer_class(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=['Get Provider Profile Publicly'])
class ProviderPublicProfileView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ProviderProfileSerializer

    def get(self,request, id):

        profile = get_object_or_404(ProviderProfile, id=id)
        serializer = self.serializer_class(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(request=None, responses=None, tags=['Get Customer Profile'])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_profile(request):

    user = request.user

    if user.role == 'c':

        customer_profile = CustomerProfile.objects.get(user=user)

        if customer_profile and not customer_profile.is_profile_complete:
            return Response({"message":"Incomplete profile.", "needs_profile_update": True}, status=status.HTTP_200_OK)
    
    elif user.role == 'p':

        provider_profile = ProviderProfile.objects.get(user=user)

        if provider_profile and not provider_profile.is_profile_complete:
            return Response({"message":"Incomplete profile.", "needs_profile_update": True}, status=status.HTTP_200_OK)
    
    else:
        return Response({"message":"Profile complete.","needs_profile_update": False}, status=status.HTTP_200_OK)

@extend_schema(tags=['Change Password'])
class ChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):

        user = request.user

        data = request.data
        serializer = self.serializer_class(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        current_password = serializer.validated_data['current_password']
        new_password = serializer.validated_data['new_password']

        if not user.check_password(current_password):
            return Response({"message":"Incorrect password."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()

        return Response({"message":"Password changed sucessfully."}, status=status.HTTP_200_OK)

@extend_schema(tags=['Logout'])
class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request):

        try:
            refresh_token = request.data.get('refresh_token')

            if refresh_token is None:

                return Response({"message":"Refresh_token is required."},status=status.HTTP_400_BAD_REQUEST)



            token = RefreshToken(refresh_token)

            token.blacklist()
            
            return Response({"message":"User logged out sucessfully."}, status=status.HTTP_205_RESET_CONTENT)
        
        except TokenError:
            return Response({"message":"Invalid Token."}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    