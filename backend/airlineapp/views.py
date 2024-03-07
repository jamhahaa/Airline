from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Flight, Reservation, City, Passenger
from .serializers import UserSerializer, FlightSerializer, ReservationSerializer, RegistrationSerializer, AdminRegistrationSerializer, AdminLoginSerializer, CitySerializer
from django.db.models import Q
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.utils import timezone
from dateutil import parser
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import F
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication




@api_view(['POST'])
def register(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        passenger = serializer.save()
        return Response({'message': 'Registration successful'})
    return Response(serializer.errors, status=400)


class PassengerLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)  

            token, created = Token.objects.get_or_create(user=user)

            user_data = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,  
            }

            return Response({'token': token.key, 'user': user_data, 'message': 'Login successful'})

        else:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):

    def post(self, request):
        logout(request)  
        return Response({'detail': 'Logged out successfully'}, status=status.HTTP_200_OK)


class UserDataView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        user_data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
        }

        return Response({'user': user_data})


class FlightList(APIView):
    def get(self, request):
        flights = Flight.objects.all()
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def get_flight(request, id):
    try:
        flight = Flight.objects.get(pk=id)
        serializer = FlightSerializer(flight)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Flight.DoesNotExist:
        return Response({"error": "Flight not found"}, status=status.HTTP_404_NOT_FOUND)



class FlightSearchView(APIView):
    def post(self, request):
        search_criteria = request.data
        print("Received search criteria:", search_criteria)

        trip_choice = request.data.get('trip_choice')
        destination_id = request.data.get('destination_id')
        origin_id = request.data.get('origin_id')
        departure_time_str = request.data.get('departure_time')

        seat_type = request.data.get('seat_type')

        flights = Flight.objects.all()

        if trip_choice:
            flights = flights.filter(trip_choice=trip_choice)
        if destination_id:
            flights = flights.filter(destination_id=destination_id)
        if origin_id:
            flights = flights.filter(origin_id=origin_id)
        if departure_time_str:
            departure_time = parser.parse(departure_time_str)
            departure_time_aware = timezone.make_aware(departure_time)
            flights = flights.filter(departure_time__gte=departure_time_aware)

        if seat_type:
            flights = flights.filter(seat_type=seat_type)

        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)


class SearchResultView(APIView):
    def post(self, request):
        search_results = request.data

        return Response(search_results)

class ReservationView(APIView):

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            reservation = serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reservation(request):
    user = request.user
    flight_id = request.data.get('flight_id')
    first_name = request.data.get('first_name')
    middle_name = request.data.get('middle_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')
    contact_number = request.data.get('contact_number')
    seat_type = request.data.get('seat_type')


    reservation = Reservation.objects.create(
        flight_id=flight_id,
        user=user, 
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        email=email,
        contact_number=contact_number,
        seat_type=seat_type,
        status='pending'  
    )

    return Response({'reservation_id': reservation.id})


class ReservationListView(APIView):
    def get(self, request):
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def user_reservations(request):
    if request.user.is_authenticated:

        reservations = Reservation.objects.filter(user=request.user)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)
    else:        
        return Response({'message': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_reservation(request, id):
    try:
        reservation = Reservation.objects.get(pk=id)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Reservation.DoesNotExist:
        return Response({"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def edit_reservation(request, id):
    try:
        reservation = Reservation.objects.get(pk=id)
    except Reservation.DoesNotExist:
        return Response({"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND)

    reservation_serializer = ReservationSerializer(instance=reservation, data=request.data, partial=True)
    if reservation_serializer.is_valid():
        reservation_serializer.save()
        return Response(reservation_serializer.data, status=status.HTTP_200_OK)

    return Response({"error": reservation_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_reservation(request, id):
    try:
        reservation = Reservation.objects.get(pk=id)
    except Reservation.DoesNotExist:
        return Response({'error': 'Reservation not found'}, status=status.HTTP_404_NOT_FOUND)

    reservation.delete()
    return Response({'message': 'Reservation deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def register_admin(request):
    serializer = AdminRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'message': 'Admin registered successfully'})
    return Response(serializer.errors, status=400)


    
class AdminLoginView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active and user.is_staff:
                login(request, user)
                return Response({'message': 'Login successful'})
            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

class CityListView(APIView):
    def get(self, request):
        cities = City.objects.all()
        data = [{'id': city.id, 'name': city.name, 'airport_name': city.airport_name, 'airport_code': city.airport_code, 'status': city.status} for city in cities]
        return Response(data)
    
@api_view(['GET'])
def get_city(request, id):
    try:
        city = City.objects.get(pk=id)
        serializer = CitySerializer(city)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except City.DoesNotExist:
        return Response({"error": "City not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def add_city(request):
    serializer = CitySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def edit_city(request, id):
    city = City.objects.get(pk=id)
    serializer = CitySerializer(instance=city, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_city(request, id):
    try:
        city = City.objects.get(pk=id)
    except City.DoesNotExist:
        return Response({'error': 'City not found'}, status=status.HTTP_404_NOT_FOUND)

    city.delete()
    return Response({'message': 'City deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def add_flight(request):
    serializer = FlightSerializer(data=request.data)
    if serializer.is_valid():

        origin_id = request.data.get('origin')
        destination_id = request.data.get('destination')

        serializer.validated_data['origin_id'] = origin_id
        serializer.validated_data['destination_id'] = destination_id

        serializer.save()
        return Response({'message': 'Flight added successfully'}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def edit_flight(request, id):
    flight = Flight.objects.get(pk=id)
    serializer = FlightSerializer(instance=flight, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_flight(request, id):
    try:
        flight = Flight.objects.get(pk=id)
    except Flight.DoesNotExist:
        return Response({'error': 'Flight not found'}, status=status.HTTP_404_NOT_FOUND)

    flight.delete()
    return Response({'message': 'Flight deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class FlightDetail(View):
    def get(self, request, pk):
        try:
            flight = Flight.objects.get(pk=pk)
            flight_data = {
                'id': flight.id,
                'flight_number': flight.flight_number,
                'origin': {
                    'id': flight.origin.id,
                    'name': flight.origin.name,
                },
                'destination': {
                    'id': flight.destination.id,
                    'name': flight.destination.name,
                },
                'departure_time': flight.departure_time,
                'arrival_time': flight.arrival_time,
                'return_time': flight.return_time,
                'capacity': flight.capacity,
                'available_seats': flight.available_seats,
                'trip_choice': flight.trip_choice,
                'seat_type': flight.seat_type,
                'economy_class_price': flight.economy_class_price,
                'business_class_price': flight.business_class_price,
            }
            return JsonResponse(flight_data)
        except Flight.DoesNotExist:
            return JsonResponse({'error': 'Flight not found'}, status=404)

def get_auth_users(request):
    users = User.objects.values('id', 'username', 'email', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login')
    return JsonResponse(list(users), safe=False)

def get_passengers(request):
    passengers = Passenger.objects.select_related('user').values(
        'user__id',
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
        'user__is_superuser',
        'user__is_staff',
        'user__is_active',
        'user__date_joined',
        'user__last_login',
        'contact_number',
        'gender',
        'address'
    )
    return JsonResponse(list(passengers), safe=False)

@api_view(['POST'])
def staff_status(request, id):
    user = get_object_or_404(User, pk=id)
    user.is_staff = not user.is_staff
    user.save()
    return JsonResponse({'success': True, 'is_staff': user.is_staff, 'message': 'is_staff status updated successfully'})

@api_view(['POST'])
def active_status(request, id):
    user = get_object_or_404(User, pk=id)
    user.is_active = not user.is_active
    user.save()
    return JsonResponse({'success': True, 'is_active': user.is_active, 'message': 'is_active status updated successfully'})


def is_token_valid(user_id, token_key):
    try:
        user = User.objects.get(id=user_id)
        token = Token.objects.get(user=user, key=token_key)
        return True
    except (User.DoesNotExist, Token.DoesNotExist):
        return False
