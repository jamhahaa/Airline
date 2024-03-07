from rest_framework import serializers
from .models import Flight, City, Reservation, Passenger, Admin
from django.contrib.auth.models import User



class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name', 'airport_name', 'airport_code', 'status']


class FlightSerializer(serializers.ModelSerializer):
    origin = CitySerializer(read_only=True)
    destination = CitySerializer(read_only=True)

    class Meta:
        model = Flight
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    flight = FlightSerializer()

    class Meta:
        model = Reservation
        fields = ['id', 'flight', 'first_name', 'middle_name', 'last_name', 'email', 'contact_number', 'seat_type', 'status']

    def create(self, validated_data):
        flight_data = validated_data.pop('flight')
        flight = Flight.objects.get(pk=flight_data['id'])

        user = self.context['request'].user

        reservation = Reservation.objects.create(flight=flight, **validated_data)
        return reservation


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.CharField()
    contact_number = serializers.CharField()

    class Meta:
        model = Passenger
        fields = ['username','first_name', 'last_name', 'password', 'email', 'contact_number', 'gender', 'address']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name = validated_data['first_name'],
            last_name= validated_data['last_name'],
            password=validated_data['password'],
            email=validated_data['email'],
        )
        passenger = Passenger.objects.create(
            user=user,
            contact_number=validated_data['contact_number'],
            gender=validated_data['gender'],
            address=validated_data['address']
        )
        return passenger



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','email','password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class AdminRegistrationSerializer(serializers.Serializer):
    admin_codes = serializers.ListField(child=serializers.CharField(max_length=20))
    user = UserSerializer()

    def validate_admin_codes(self, values):
       
        valid_codes = ['admin111', 'admin222']  
        for code in values:
            if code not in valid_codes:
                raise serializers.ValidationError('Invalid admin code: {}'.format(code))
        return values

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        admin_codes = validated_data.pop('admin_codes')
        admins = []
        for code in admin_codes:
            admin = Admin.objects.create(user=user, admin_code=code, **validated_data)
            admins.append(admin)
        return admins



class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

