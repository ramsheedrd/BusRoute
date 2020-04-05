import datetime
from .models import BusModel, PlacesModel, RouteModel, TripModel
from django.db.models import Q


def js_to_py_time(arg):
    return datetime.time(int(arg.split(":")[0]), int(arg.split(":")[1]), 00) 

def start_js_to_py_time(arg):
    return (datetime.datetime.combine(datetime.date(1,1,1),js_to_py_time(arg)) - datetime.timedelta(minutes = 1)).time() 

def match_bus(from_stop, to_stop, start_time, end_time, category="all"):
    matched_buses = []
    if start_time == "" and end_time == "":
        now = datetime.datetime.now().time()
        now_10 = (datetime.datetime.now() + datetime.timedelta(minutes = 30)).time()
    else:
        now = start_js_to_py_time(start_time)
        # now_10 = (datetime.datetime.combine(datetime.date(1,1,1),now) + datetime.timedelta(minutes = 30)).time()
        now_10 = js_to_py_time(end_time)
    try:
        place_obj = PlacesModel.objects.get(place_name = from_stop)
        to_obj = PlacesModel.objects.get(place_name = to_stop)
        matched_trips = RouteModel.objects.filter(Q(stop=place_obj,time__gt = now) & Q(stop=place_obj,time__lt = now_10))
    except:
        pass
    
    for trip_obj in matched_trips:
        # print(trip_obj.trip,trip_obj.forward)
        try:
            print(trip_obj.time)
            trip_obj2 = RouteModel.objects.get(trip=trip_obj.trip,stop=to_obj,time__gt = trip_obj.time,forward=trip_obj.forward)
            if (category == "all" or trip_obj2.trip.bus.category == category) and \
                (trip_obj2.trip.bus.active and trip_obj2.trip.bus.permitted and trip_obj2.trip.active):
                matched_buses.append({"bus":trip_obj2.trip.bus,"from":trip_obj,"to":trip_obj2,"trip":trip_obj2.trip})
        except:
            print("no match")
    return matched_buses