from django.urls import path
from .views import CreateAppointmentView, CustomerGetUpdateappointmentView


urlpatterns = [

    path('create/', CreateAppointmentView.as_view(), name='create-appointment'),
    path('my-appointments/', CustomerGetUpdateappointmentView.as_view(), name='get-appointments'),
    path('update/<int:id>/my-appointments/', CustomerGetUpdateappointmentView.as_view(), name='update-appointments'),
]