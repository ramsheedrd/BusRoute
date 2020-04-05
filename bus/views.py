from django.contrib.auth.decorators import login_required,permission_required
from django.contrib import messages
from django.core import serializers
from django.db.models import Q
from django.shortcuts import HttpResponse,render,redirect
from django.utils import timezone,dateparse

from .extras import js_to_py_time, match_bus
from .forms import CreateBusForm
from .models import BusModel, PlacesModel, RouteModel,\
     TripModel ,NearMeModel, EmergencyNumbersModel, RentBusModel, BookingModel
from accounts.models import UserAccounts 
from geopy.distance import geodesic

import datetime
import json

# Create your views here.
USER_URL = "/accounts/user/login/"
OWNER_URL = "/accounts/owner/login/"

USER_PERM = 'accounts.user_rights'
OWNER_PERM = 'accounts.owner_rights'

@login_required(login_url=USER_URL)
@permission_required(USER_PERM,login_url = USER_URL)
def user_main_view(request):
    context = {}
    if request.method == "POST":
        from_stop = request.POST["from"]
        to_stop = request.POST["to"]
        start_time = request.POST["start_time"]
        end_time = request.POST["end_time"]
        category = request.POST.get("category","all")
        context = {
            "matched":match_bus(from_stop, to_stop, start_time, end_time, category)
        }
        if not context["matched"]:
            messages.info(request, 'No Result Found')

    return render(request, 'bus/search.html',context)

@login_required(login_url=OWNER_URL)
@permission_required(OWNER_PERM,login_url = OWNER_URL)
def owner_main_view(request):
    bus_list = BusModel.objects.filter(owner=request.user)
    if request.method == "POST":
        form = CreateBusForm(request.POST)
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.owner = request.user
            tmp.save()
            messages.info(request, 'Bus Added Successfully!')
            return redirect('/bus/owner/main/')
        else:
            context = {
                "buses" : bus_list,
                "form" : form
            }
            return render(request, 'bus/buses.html',context)
    else:
        form = CreateBusForm()
        context = {
            "buses" : bus_list,
            "form" : form
        }
        return render(request, "bus/buses.html", context)

@login_required(login_url=USER_URL)
def near_view(request,category):
    if category == 'all':
        locations = NearMeModel.objects.all()
    else:
        locations = NearMeModel.objects.filter(category=category)
    
    if request.session.has_key("time"):
            latitude = request.session['latitude']
            longitude = request.session['longitude'] 
            locations = list(locations)
            locations.sort(key=lambda i: geodesic((float(latitude),float(longitude)), (float(i.latitude),float(i.longitude))))
    
    return render(request, "bus/find_nearest.html",{"locations":locations})

@login_required(login_url=USER_URL)
def emergency_view(request):
    emergency_numbers = EmergencyNumbersModel.objects.all()
    return render(request, "bus/emergency.html",{"emrgencies": emergency_numbers})

@permission_required(USER_PERM,login_url = USER_URL)
@login_required(login_url=USER_URL)
def user_mytrip_view(request):
    value_list = BookingModel.objects.values(
    'booking_date','user','trip','start','end'
    ).distinct()
    mytrips = []
    for j in value_list:
        ob = BookingModel.objects.filter(user = request.user,booking_date=j["booking_date"], trip = j['trip'], start = j['start'], end = j['end'])
        mytrips.append(ob)
    
    temp = []
    for k in mytrips:
        temp.append({"booking":k[0],"count":k.count(),"total":k.count()*254})

    # booked = BookingModel.objects.filter(user = request.user, booking_date__gt = timezone.now().date())
    return render(request, "bus/mytrip.html",{"booked": temp})

@login_required(login_url=USER_URL)
def user_booking_view(request, trip_id, from_id, to_id):
    trip = TripModel.objects.get(id=trip_id)
    start = RouteModel.objects.get(id=from_id)
    end = RouteModel.objects.get(id=to_id)
    context = {"trip": trip, "from": start, "to": end}
    booking_date = request.GET.get("book_date")
    # context["booking_date"] = timezone.now().date().strftime("%Y-%m-%d") 
    if booking_date:
        booked = BookingModel.objects.filter(trip = trip, booking_date = booking_date)
    else:
        booked = BookingModel.objects.filter(trip = trip, booking_date = timezone.now().date())

    if not booked.count() >= trip.bus.capacity:
        context["booked_records"] = booked 
        context["booking_date"] = booking_date 
        context["available"] = trip.bus.capacity - booked.count()


    if request.method == "POST":
        no_passengers = request.POST["no_passenger"]
        fare = 254
        if datetime.datetime.strptime(booking_date, '%Y-%m-%d').date()>timezone.now().date():
            for _ in range(int(no_passengers)):
                obj = BookingModel(user=request.user, trip=trip, booking_date = booking_date, start=start, end=end, fare=fare)
                obj.save()
            messages.success(request,"Booking successful")
        else:
            messages.error(request,"Invalid Date")

        return redirect('/bus/user/mytrip/')

    return render(request, "bus/booking.html", context)

@permission_required(OWNER_PERM,login_url = OWNER_URL)
@login_required(login_url=OWNER_URL)
def rent_a_bus_view(request):
    buses = RentBusModel.objects.all()
    return render(request, "bus/rent_a_bus.html",{"buses": buses})

@login_required(login_url=USER_URL)
def main_view(request):
    if request.user.is_bus_owner:
        return redirect('/bus/owner/main/')
    else:
        return redirect('/bus/user/main/')

@login_required(login_url=OWNER_URL)
@permission_required(OWNER_PERM,login_url = OWNER_URL)
def owner_route_view(request,id):
    trip_list = TripModel.objects.filter(bus=id,bus__owner=request.user)
    context = {
        "trips":trip_list,
        "bus_id": id
    }
    return render(request, "bus/routes.html", context)

@login_required(login_url=OWNER_URL)
@permission_required(OWNER_PERM,login_url = OWNER_URL)
def owner_route_add_view(request,id):
    bus = BusModel.objects.get(id=id)
    if request.user.id != bus.owner.id:
        return redirect('/accounts/owner/main/')
    context = {
        "bus": bus
    }
    return render(request, "bus/add_route.html", context)

def places_ajax_view(request):
    if request.is_ajax():
        place = request.GET.get('startsWith', '')
        data = PlacesModel.objects.filter(place_name__startswith = place)
        qs_json = serializers.serialize('json', data)
        return HttpResponse(qs_json, content_type='application/json')
    return render(request, 'index.html', {'user': ''})

@login_required(login_url=OWNER_URL)
@permission_required(OWNER_PERM,login_url = OWNER_URL)
def owner_route_save_view(request,id):
    data = json.loads(request.GET['parameters'])
    bus = BusModel.objects.get(id=id)
    start_time = js_to_py_time(data[0]["time"])
    end_time = js_to_py_time(data[-1]["time"])
    start_place = data[0]["place"]
    end_place = [i for i in data if i["forward"] == False]
    try:
        end_place = end_place[0]["place"]
    except:
        end_place = data[-1]["place"]
    obj = TripModel(bus=bus, start_time=start_time, end_time=end_time, start_place=start_place, end_place=end_place)
    obj.save()
    for i in data:
        tmp_place = PlacesModel.objects.get(place_name = i["place"])
        rout = RouteModel(trip = obj, stop = tmp_place, \
        time = js_to_py_time(i["time"]), forward = i["forward"])
        rout.save()
    return HttpResponse({"success":"true"}, content_type='application/json')

@login_required(login_url=OWNER_URL)
@permission_required(OWNER_PERM,login_url = OWNER_URL)
def owner_bus_status_view(request,id):
    if request.is_ajax():
        obj = BusModel.objects.get(id=id)
        if request.user.id == obj.owner.id:
            obj.active = not obj.active
            obj.save()
    return HttpResponse({"success":"true"}, content_type='application/json')

@login_required(login_url=OWNER_URL)
@permission_required(OWNER_PERM,login_url = OWNER_URL)
def owner_bus_delete_view(request,id):
    bus = BusModel.objects.get(id=id)
    if request.user.id == bus.owner.id:
        bus.delete()
    return redirect('/bus/owner/main/')

@login_required(login_url=OWNER_URL)
@permission_required(OWNER_PERM,login_url = OWNER_URL)
def owner_trip_status_view(request,id,trip):
    bus = BusModel.objects.get(id=id)
    if request.user.id == bus.owner.id:
        print(trip)
        obj = TripModel.objects.get(id=trip)
        obj.active = not obj.active
        obj.save()
    return HttpResponse({"success":"true"}, content_type='application/json')


@login_required(login_url=OWNER_URL)
@permission_required(OWNER_PERM,login_url = OWNER_URL)
def owner_trip_delete_view(request,id,trip):
    bus = BusModel.objects.get(id=id)
    if request.user.id == bus.owner.id:
        obj = TripModel.objects.get(id= trip)
        obj.delete()
    return redirect('/bus/owner/routes/'+str(id)+"/")

@login_required(login_url=USER_URL)
def owner_ajax_bus_view(request,id):
    if request.is_ajax():
        obj = TripModel.objects.get(id=id)
        d = [{"time":str(i.time),"stop":i.stop.place_name,"bus":i.trip.bus.name,"plate":i.trip.bus.reg_no,"owner":i.trip.bus.owner.first_name} for i in obj.routemodel_set.all()]
        qs_json = json.dumps(d)
        return HttpResponse(qs_json, content_type='application/json')

@permission_required("auth.change_user",login_url = '/admin/login/')
def admin_news(request):
    buses = BusModel.objects.filter(permitted=False)
    buses = [i for i in buses if i.tripmodel_set.count() > 0]
    users = UserAccounts.objects.all()[:10:-1]
    all_buses = BusModel.objects.filter(permitted=True)
    return render(request, "admin/news.html", {"buses":buses,"users":users,"all_buses":all_buses})   

@permission_required("auth.change_user",login_url = '/admin/login/')
def grant_permit_admin(request,id):
    bus = BusModel.objects.get(id=id)
    bus.permitted = True
    bus.save()
    return redirect('/admin/news/')  


def set_location(request):
    latitude = request.GET.get("latitude")
    longitude = request.GET.get("longitude")
    if request.session.has_key("time"):
        if datetime.datetime.now().time()>dateparse.parse_time(request.session['time']):            
            if longitude and latitude:
                request.session['latitude']=latitude
                request.session['longitude']=longitude
                request.session['time']=str((datetime.datetime.now() + datetime.timedelta(minutes = 1)).time())
                return HttpResponse(json.dumps({"success":"new"}), content_type='application/json')

    else:
        if longitude and latitude:
                request.session['latitude']=latitude
                request.session['longitude']=longitude
                request.session['time']=str((datetime.datetime.now() + datetime.timedelta(minutes = 1)).time())
    return HttpResponse(json.dumps({"success":"old"}), content_type='application/json')

