from django.urls import path
from .views import FlightList, FlightSearchView, SearchResultView, ReservationView, create_reservation
from .views import ReservationListView, user_reservations, get_reservation, edit_reservation, delete_reservation, register, PassengerLoginView, LogoutView, register_admin, AdminLoginView, CityListView, add_city, get_city, edit_city, delete_city, add_flight, get_flight, edit_flight, delete_flight, FlightDetail 
from .views import get_auth_users, staff_status, get_passengers, active_status, UserDataView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('flights/', FlightList.as_view(), name='flightlist'),
    path('search/', FlightSearchView.as_view(), name='searchflight'),
    path('result/', SearchResultView.as_view(), name='searchresult'),

    path('reservation/', ReservationView.as_view(), name='flightreservation'),
    path('createreservation/', create_reservation, name='create_reservation'),
    path('reservationlist/', ReservationListView.as_view(), name='reservationlist'),
    path('user_reservations/', user_reservations, name='user_reservations'),
    path('get_reservation/<int:id>/', get_reservation, name='get_reservation'),
    path('edit_reservation/<int:id>/', edit_reservation, name='edit_reservation'),
    path('delete_reservation/<int:id>/', delete_reservation, name='delete_reservation'),

    path('register/', register, name='register'),
    path('login/', PassengerLoginView.as_view(), name='passengerlogin'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('register/admin/', register_admin, name='admin_registration'),
    path('login/admin/', AdminLoginView.as_view(), name='adminlogin'),

    path('cities/', CityListView.as_view(), name='city-list'),
    path('addcity/', add_city, name='add_city'),
    path('get_city/<int:id>/', get_city, name='get_city'),
    path('edit_city/<int:id>/', edit_city, name='edit_city'),
    path('delete_city/<int:id>/', delete_city, name='delete_city'),

    path('addflight/', add_flight, name='add_flight'),
    path('get_flight/<int:id>/', get_flight, name='get_flight'),
    path('edit_flight/<int:id>/', edit_flight, name='edit_flight'),
    path('delete_flight/<int:id>/', delete_flight, name='delete_flight'),
    path('flights/<int:pk>/', FlightDetail.as_view(), name='flightdetail'),

    path('api/auth_users/', get_auth_users, name='get_auth_users'),
    path('api/passengers/', get_passengers, name='get_passengers'),
    path('api/staff_status/<int:id>/', staff_status, name='staff_status'),
    path('api/active_status/<int:id>/', active_status, name='active_status'),
    path('api/user-data/', UserDataView.as_view(), name='user-data'),
    path('api/token/', obtain_auth_token, name='api_token'),
]

