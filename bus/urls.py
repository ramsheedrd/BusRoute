"""busroute URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bus import views

urlpatterns = [
    path('set/location/',views.set_location),
    path('user/booking/<int:trip_id>/<int:from_id>/<int:to_id>/',views.user_booking_view),
    path('user/emergency/',views.emergency_view),
    path('user/main/', views.user_main_view),
    path('user/mytrip/',views.user_mytrip_view),
    path('user/nearest/<category>/',views.near_view),
    path('owner/main/', views.owner_main_view),
    path('owner/rent/',views.rent_a_bus_view),
    path('owner/routes/ajax/get/<int:id>/',views.owner_ajax_bus_view),
    path('owner/routes/<int:id>/', views.owner_route_view),
    path('owner/routes/add/<int:id>/',views.owner_route_add_view),
    path('owner/places/',views.places_ajax_view),
    path('owner/routes/save/<int:id>/',views.owner_route_save_view),
    path('owner/bus/status/<int:id>/',views.owner_bus_status_view),
    path('owner/bus/delete/<int:id>/',views.owner_bus_delete_view),
    path('owner/trip/status/<int:id>/<int:trip>/',views.owner_trip_status_view),
    path('owner/trip/delete/<int:id>/<int:trip>/',views.owner_trip_delete_view),
]
