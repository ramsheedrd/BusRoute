from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

bus_category = (
    ("ksrtc","KSRTC"),
    ("private","Private")
)

ksrtc_buses = (
    ("ORD","Ordinary"),
    ("LS","Limited Stop"),
    ("TT","Town to Town"),
    ("FS","Fast Passenger"),
    ("SF","Super Fast"),
    ("PP","Point to Point"),
    ("LF","Low Floor"),
    ("ALF","A/C Low Floor")
)

hospital_types = (
    ("general", "General Hospital"),
    ("government", "Government Hospital"),
    ("private", "Private Hospital")
)

near_me_types = (
    ("police", "Police"),
    ("hospital", "Hospital"),
    ("workshop", "Workshop")
)

rent_bus_type = (
    ("minibus", "Mini bus"),
    ("delux", "Delux bus"),
    ("non-delux", "Non-Delux bus")
)

class BusModel(BaseModel):
    owner = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    reg_no = models.CharField(max_length=30)
    active = models.BooleanField(default=False)
    permitted = models.BooleanField(default=False)
    # leave_day = models.CharField(max_length=15,choices=week_day,null=True,blank=True)
    category = models.CharField(max_length=15,choices=bus_category,default='private')
    ksrtc_category = models.CharField(max_length=15,choices=ksrtc_buses,null=True,blank=True)
    capacity = models.IntegerField(default=0)
    booking = models.BooleanField(default=False)
    minimum_rate = models.IntegerField(null=True,blank=True)
    rate_hour = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.name

class TripModel(BaseModel):
    bus = models.ForeignKey(BusModel,on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_place = models.CharField(max_length=30)
    end_place = models.CharField(max_length=30)
    active = models.BooleanField(default=False)
    stand_delay = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.bus.name +" ( "+self.start_place.capitalize()+"-"+self.end_place.capitalize()+" )"

class DistrictModel(BaseModel):
    district = models.CharField(max_length=50)

    def __str__(self):
        return self.district

class PlacesModel(BaseModel):
    place_name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.place_name

class RouteModel(BaseModel):
    trip = models.ForeignKey(TripModel,on_delete=models.CASCADE)
    stop = models.ForeignKey(PlacesModel,on_delete=models.CASCADE)
    time = models.TimeField()
    forward = models.BooleanField(default=True)

    def __str__(self):
        return str(self.time)+" - "+self.stop.place_name

class NearMeModel(models.Model):
    category = models.CharField(max_length=20,choices=near_me_types,default='hospital')
    name = models.CharField(max_length=100)
    hospital_category = models.CharField(max_length=20,choices=hospital_types,null=True,blank=True)
    address = models.TextField(null=True)
    phone = models.CharField(max_length=20,null=True)
    latitude = models.CharField(max_length=100,null=True)
    longitude = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name

class EmergencyNumbersModel(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class RentBusModel(BaseModel):
    owner = models.CharField(max_length=60)
    reg_no = models.CharField(max_length=30)
    category = models.CharField(max_length=20,choices=rent_bus_type,null=True,blank=True)
    ac = models.BooleanField(default=False)
    capacity = models.IntegerField(null=True,blank=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(null=True)

    def __str__(self):
        return self.reg_no

class BookingModel(BaseModel):
    user = models.ForeignKey(get_user_model(),on_delete= models.CASCADE)
    trip = models.ForeignKey(TripModel, on_delete=models.CASCADE)
    booking_date = models.DateField()
    start = models.ForeignKey(RouteModel, on_delete=models.CASCADE, related_name="tripstart")
    end = models.ForeignKey(RouteModel, on_delete=models.CASCADE, related_name="tripend")
    fare = models.IntegerField()







