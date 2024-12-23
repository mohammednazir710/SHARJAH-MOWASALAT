from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from main.models import BusStop, BusSchedule, History, Route, RouteStop
# import csv, json
# from datetime import time
from django.db.models import Q
from datetime import datetime, timedelta
import math
# Create your views here.

def index(request):
    return render(request, 'index.html')

def route(request):
    history = History.objects.filter(key=request.session.session_key)
    return render(request, 'route.html', {'history': history})

def sayer(request):
    return render(request, 'sayer.html')

def career(request):
    return render(request, 'career.html')

def mission_and_vision(request):
    return render(request, 'mission_and_vision.html')

def schadule(request):
    starting_points = BusStop.objects.all().order_by('name')
    return render(request, 'schadule.html', {'starting_points': starting_points})

# def test(request):
#     return render(request, 'test.html')

def delete_history(request):
    if request.session.session_key:
        History.objects.filter(key=request.session.session_key).delete()
    return redirect(request.META.get('HTTP_REFERER', '/fallback-url'))


def get_end_points(request, start_id):
    # Find the starting bus stop
    start_stop = BusStop.objects.filter(id=start_id).first()
    if not start_stop:
        return JsonResponse([], safe=False)

    # Get all routes where the start stop exists
    routes_with_start = RouteStop.objects.filter(stop=start_stop).values_list('route_id', flat=True)

    # Get all stops in those routes except the start stop itself
    end_stops = RouteStop.objects.filter(
        route_id__in=routes_with_start
    ).exclude(stop=start_stop)

    # Eliminate duplicate stops and prepare the response data
    unique_stops = end_stops.values('stop__id', 'stop__name').distinct().order_by('stop__name')
    data = [
        {"id": stop['stop__id'], "name": stop['stop__name']}
        for stop in unique_stops
    ]

    return JsonResponse(data, safe=False)


def get_schedules(request, start_point_id, end_point_id):
    
    start_routes = RouteStop.objects.filter(stop_id=start_point_id).values_list('route_id', flat=True)
    end_routes = RouteStop.objects.filter(stop_id=end_point_id).values_list('route_id', flat=True)
    common_route = Route.objects.filter(id__in=set(start_routes).intersection(end_routes)).first()
    start_point_order = RouteStop.objects.get(stop_id=start_point_id, route=common_route).order
    end_point_order = RouteStop.objects.get(stop_id=end_point_id, route=common_route).order
    print(start_point_order, end_point_order, common_route.total_stops())
    reverse = False if start_point_order < end_point_order else True
    total_time = common_route.schedules.filter(reverse=reverse).first().travel_duration()
    print(total_time)
    total_stops = common_route.total_stops()
    timeaddition = total_time/(total_stops-1)
    if start_point_order==1 and end_point_order==total_stops:
        timeaddition = 0
    if reverse:
        add_with_dispatch = math.ceil(timeaddition*(total_stops-start_point_order)) if timeaddition != 0 else 0
        minus_from_arraival = math.floor(timeaddition*(end_point_order-1)) if timeaddition != 0 else 0
    else:    
        add_with_dispatch = math.ceil(timeaddition*(start_point_order-1)) if timeaddition != 0 else 0
        minus_from_arraival = math.floor(timeaddition*(total_stops-end_point_order)) if timeaddition != 0 else 0
    schedules = BusSchedule.objects.filter(
        route=common_route,
        reverse=reverse
        )
    print("Timeaddition: ",timeaddition)
    print("Add with dispatch: ", add_with_dispatch)
    print("Minus with dispatch: ", minus_from_arraival)
    data = [
        {
            "route": common_route.name,
            "dispatch": (datetime.combine(datetime.today(), schedule.dispatch_time) + timedelta(minutes=add_with_dispatch)).time().strftime('%I:%M %p'),
            "arrival": (datetime.combine(datetime.today(), schedule.arrival_time) - timedelta(minutes=minus_from_arraival)).time().strftime('%I:%M %p'),
            "fare": "AED 6.00 - 8.00",  # Adjust fare logic if needed
        }
        for schedule in schedules
    ]

    return JsonResponse(data, safe=False)

def get_bus_stops(request):
    # Fetch all bus stops from the database and sort them alphabetically by name
    bus_stops = BusStop.objects.all().values('name', 'latitude', 'longitude').order_by('name')
    
    # Convert the QuerySet to a list and return as JSON response
    return JsonResponse(list(bus_stops), safe=False)


# from math import radians, sin, cos, sqrt, atan2

# def haversine(lat1, lon1, lat2, lon2):
#     # Convert latitude and longitude from degrees to radians
#     lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

#     # Haversine formula
#     dlat = lat2 - lat1
#     dlon = lon2 - lon1
#     a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
#     c = 2 * atan2(sqrt(a), sqrt(1 - a))
#     R = 6371  # Earth's radius in kilometers
#     return R * c

# def find_nearest_bus_stop(lat, lng):
#     bus_stops = BusStop.objects.all()
#     nearest_stop = None
#     min_distance = float('inf')

#     for stop in bus_stops:
#         distance = haversine(lat, lng, float(stop.lat), float(stop.lng))
#         if distance < min_distance:
#             min_distance = distance
#             nearest_stop = stop

#     return nearest_stop

# def temp_route(request):
#     if request.method == "POST":
#         start_lat = float(request.POST.get('startLat'))
#         start_lng = float(request.POST.get('startLng'))
#         end_lat = float(request.POST.get('endLat'))
#         end_lng = float(request.POST.get('endLng'))

#         start_loc_name = request.POST.get('startLocName')
#         end_loc_name = request.POST.get('endLocName')

#         # Find nearest bus stops
        
#         start_bus_stop = find_nearest_bus_stop(start_lat, start_lng)
#         end_bus_stop = find_nearest_bus_stop(end_lat, end_lng)

#         start_loc = f'{start_lat},{start_lng}'
#         end_loc = f'{end_lat},{end_lng}'
#         start_bus_loc = f'{start_bus_stop.lat},{start_bus_stop.lng}'
#         end_bus_loc = f'{end_bus_stop.lat},{end_bus_stop.lng}'

#         # Get the current session key
#         session_key = request.session.session_key
        
#         # If session hasn't been created yet, force it to create
#         if not session_key:
#             request.session.create()
#             session_key = request.session.session_key
#         distance = haversine(start_lat, start_lng, end_lat, end_lng)
#         History.objects.create(
#             key=session_key,
#             start=start_loc,
#             end=end_loc,
#             start_loc_name=start_loc_name,
#             end_loc_name=end_loc_name,
#             distance=distance
#         )


#         con = {
#             'route_view': True,
#             'start_loc': start_loc,
#             'end_loc': end_loc,
#             'start_bus_loc':start_bus_loc,
#             'end_bus_loc':end_bus_loc

#         }
#         print(con.values())
#     context = con if con else {}
#     return render(request, 'index.html', context)



# ---------------------------------------------------------------------
# ------------------------------ Load Data ----------------------------
# ---------------------------------------------------------------------
import csv
def load_data(request):
    
    with open('data.csv', 'r') as file:
        reader = csv.reader(file)
        fields = next(reader)
        route_ = Route.objects.get(name="88")
        for stop in reader:
            BusSchedule.objects.create(
                route=route_,
                reverse=True,
                dispatch_time=stop[0],
                arrival_time=stop[1]
            )
    return HttpResponse("Data loaded successful")

