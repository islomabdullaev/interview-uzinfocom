from datetime import datetime, time
from uuid import UUID
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from django.db.models import Q
from booking.models import Playground, PlaygroundBooking
from booking.serializers import (
    CreatePlaygroundSerializer, PlaygroundBookingCreateSerializer,
    PlaygroundBookingSerializer, PlaygroundResponseSerializer, UpdatePlaygroundSerializer)
from config.permissions import IsAdminOrClient, IsAdminOrOwner
from users.choices import UserRoleType
from rest_framework.decorators import permission_classes

# Create your views here.

class PlaygroundView(APIView):

    def post(self, request: Request):
        data = request.data

        serializer = CreatePlaygroundSerializer(data=data)

        if serializer.is_valid():
            owner = request.user

            # here I'm checking whether objects is created in one session without any problem
            created = serializer.save(owner=owner)
            if not created:
                return Response(data={"message": "Something went wrong !"},
                                status=status.HTTP_400_BAD_REQUEST)

            return Response(data={"message": "Created Successfully !"},
                            status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request: Request):
        # Couldnt do order by distance part as never worked with locations)
        query = request.query_params
        for_date = query.get("for_date")
        start_time = query.get("start_time")
        end_time = query.get("end_time")

        converted_start_time = datetime.strptime(start_time, "%H:%M:%S")
        converted_end_time = datetime.strptime(end_time, "%H:%M:%S")
        
        # here goes the process of search with given argumens
        if query:
            playgrounds = Playground.objects.exclude(
                bookings__for_date=for_date,
                bookings__start_time__lte=converted_start_time,
                bookings__end_time__gte=converted_end_time
            )
        else:
            playgrounds = Playground.objects.all()
        serializer = PlaygroundResponseSerializer(playgrounds, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def get_permissions(self):
        permissions = super().get_permissions()

        if self.request.method.lower() == 'post':
            permissions.append(IsAdminOrOwner())

        if self.request.method.lower() == 'get':
            permissions.append(IsAdminOrClient())


class PlaygroundDetailView(APIView):
    
    def get(self, request: Request, id: UUID):
        try:
            playground = Playground.objects.get(id=id)
        except Playground.DoesNotExist:
            return Response(data={"message": "Playground not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PlaygroundResponseSerializer(playground, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request: Request, id: UUID):
        data = request.data
        try:
            playground = Playground.objects.get(id=id)
        except Playground.DoesNotExist:
            return Response(data={"message": "Playground not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UpdatePlaygroundSerializer(playground, data=data)

        if serializer.is_valid():
            print("validation passed !")
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_permissions(self):
        permissions = super().get_permissions()

        if self.request.method.lower() == 'put':
            permissions.append(IsAdminOrOwner())

        return permissions


class PlaygroundBookingView(APIView):

    def post(self, request: Request):
        serializer = PlaygroundBookingCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            playground = Playground.objects.get(id=serializer.validated_data["playground"])
            serializer.save(user=user, playground=playground)
            return Response(data={"message": "Booking created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def get(self, request: Request):
        user = request.user
        if user.role == UserRoleType.admin.value:
            bookings = PlaygroundBooking.objects.all()
        else:
            bookings = PlaygroundBooking.objects.filter(Q(user=user) | Q(playground__owner=user))
        serializer = PlaygroundBookingSerializer(bookings, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def get_permissions(self):
        permissions = super().get_permissions()

        if self.request.method.lower() == 'post':
            permissions.append(IsAdminOrClient())
            print(permissions)

        if self.request.method.lower() == 'get':
            permissions.append(IsAdminOrOwner())

        return permissions


class PlaygroundBookingDetailView(APIView):

    permission_classes = [IsAdminOrOwner]

    def get(self, request: Request, id: UUID):
        try:
            booking = PlaygroundBooking.objects.get(id=id)
        except PlaygroundBooking.DoesNotExist:
            return Response(data={"message": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlaygroundBookingSerializer(booking, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PlaygroundBookingDeleteView(APIView):

    permission_classes = [IsAdminOrOwner]

    def delete(self, request: Request, id: UUID):
        try:
            booking = PlaygroundBooking.objects.get(id=id)
        except PlaygroundBooking.DoesNotExist:
            return Response(data={"message": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if booking.playground.owner != request.user:
            return Response(data={"message": "You are not allowed to delete this booking"}, status=status.HTTP_403_FORBIDDEN)
        booking.delete()
        return Response(data={"message": "Booking deleted successfully"}, status=status.HTTP_200_OK)