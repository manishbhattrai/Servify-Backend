from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import CreateAppointmentSerializer, CustomerGetAppointmentsSerializer
from appointments.models import Appointments
from .permissions import IsCustomerOnly




class CreateAppointmentView(generics.CreateAPIView):

    queryset = Appointments.objects.all()
    serializer_class = CreateAppointmentSerializer
    permission_classes = [IsCustomerOnly]


    def perform_create(self, serializer):
        
        return serializer.save(customer = self.request.user)

class CustomerGetUpdateappointmentView(APIView):

    serializer_class = CustomerGetAppointmentsSerializer
    permission_classes = [IsCustomerOnly]

    def get(self,request):

        user = request.user
        appointments = Appointments.objects.filter(customer=user)

        serializer = self.serializer_class(appointments, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self,request, id):

        user = request.user

        appointments = get_object_or_404(Appointments, id=id ,customer = user)

        new_status = request.data.get('status')

        if new_status != 'cancelled':
            return Response({"message":"customer has only permission to cancel the appointments."},
                            status=status.HTTP_400_BAD_REQUEST
                            )
        
        if new_status != 'pending':
            return Response({"message":"only pending appointments can be cancelled."},
                            status=status.HTTP_400_BAD_REQUEST
                            )
        
        if not new_status:
            return Response({"message":"status is required."},status=status.HTTP_400_BAD_REQUEST)
        
        appointments.status = new_status
        appointments.save()

        return Response({"message":"Appointment cancelled sucessfully."},status=status.HTTP_200_OK)
