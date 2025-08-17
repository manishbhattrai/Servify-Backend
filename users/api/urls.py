from django.urls import path
from .views import (

                ChangePasswordView, UserRegistrationView, ProviderProfileView,
                ProviderRegistrationView, CreateAPIView,CustomerProfileView,LoginView,
                LogoutView, get_profile, ProviderPublicProfileView,
                PublicCustomerProfileView
                    
                    )

urlpatterns = [ 

    path('login/', LoginView.as_view(), name= 'user-login'),
    path('customer/register/', UserRegistrationView.as_view(), name= 'customer-register'),
    path('provider/register/', ProviderRegistrationView.as_view(), name='provider-register'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('customer/profile/create/', CreateAPIView.as_view(), name='create-profile'),
    path('customer/profile/', CustomerProfileView.as_view(), name='customer-profile'),
    path('customer/profile/<int:id>/', PublicCustomerProfileView.as_view(), name='customer-profile-get'),
    path('provider/profile/', ProviderProfileView.as_view(), name='provider-profile'),
    path('provider/profile/<int:id>/', ProviderPublicProfileView.as_view(), name='provider-profile-get'),
    path('check-profile/', get_profile, name='check-profile'),
]