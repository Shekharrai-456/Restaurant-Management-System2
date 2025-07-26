
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from bookings.models import Booking
from bookings.serializers import BookingSerializer
from users.models import CustomUser
from users.serializer import CustomUserSerializer  # Make sure this exists
from django.contrib.auth import authenticate


# --- EVENT TEST ENDPOINT ---
@api_view(['GET'])
def api_event_list(request):
    return Response({"message": "Event list API works!"})


# --- GET ALL BOOKINGS BY USER ID ---
@api_view(['GET'])
def api_user_bookings(request, user_id):
    bookings = Booking.objects.filter(user__id=user_id)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)


# --- CREATE A NEW BOOKING ---
@api_view(['POST'])
def api_create_booking(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# --- USER REGISTRATION ---
@api_view(['POST'])
def api_register_user(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def api_login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        return Response({"message": "Login successful", "user_id": user.id}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)