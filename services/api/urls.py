from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (

    ProviderSerivceViewSet, ProviderServiceListForCustomerView, BaseServiceViewSet
)

router = DefaultRouter()

router.register(r'provider-services', ProviderSerivceViewSet, basename='provider-services')
router.register(r'base-services', BaseServiceViewSet, basename='base-services')


urlpatterns = [

    path('',include(router.urls)),
    path('<int:provider_id>/service-list/', ProviderServiceListForCustomerView.as_view(), name='service-list'),
]

