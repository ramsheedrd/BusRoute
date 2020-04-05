from django.contrib import admin
from .models import BusModel,PlacesModel,TripModel,RouteModel,\
    DistrictModel,NearMeModel, EmergencyNumbersModel, RentBusModel, BookingModel

# Register your models here.
admin.site.register(PlacesModel)
admin.site.register(RouteModel)
admin.site.register(DistrictModel)


@admin.register(BusModel)
class BusAdmin(admin.ModelAdmin):
    list_display = ["name", "reg_no", "category", "permitted", "active"]

@admin.register(TripModel)
class TripAdmin(admin.ModelAdmin):
    list_display = ["bus", "start_time", "end_time", "start_place", "end_place", "active"]

@admin.register(NearMeModel)
class NearMeAdmin(admin.ModelAdmin):
    list_display = ["name", "category"]

@admin.register(EmergencyNumbersModel)
class EmergencyNumbersAdmin(admin.ModelAdmin):
    list_display = ["name", "phone"]

@admin.register(RentBusModel)
class RentBusAdmin(admin.ModelAdmin):
    list_display = ["category", "ac", "capacity", "owner", "phone", "address"]

@admin.register(BookingModel)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["user", "trip", "created_date"]




