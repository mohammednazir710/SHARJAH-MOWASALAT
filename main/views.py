from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import BusStop
from main.models import BusStop, EndStop, BusSchedule
import csv, json
from datetime import time

# Create your views here.

def index(request):
    return render(request, 'index.html')

def route(request):
    return render(request, 'route.html')

def schadule(request):
    starting_points = BusStop.objects.filter(start=True)
    return render(request, 'schadule.html', {'starting_points': starting_points})

def test(request):
    return render(request, 'test.html')

def get_end_points(request, start_code):
    # Find the starting bus stop
    start_stop = BusStop.objects.filter(code=start_code).first()
    if not start_stop:
        return JsonResponse([], safe=False)

    # Get all destinations for the selected start stop
    end_stops = EndStop.objects.filter(from_stop=start_stop)
    data = [
        {"code": end_stop.stop.code, "name": end_stop.stop.name}
        for end_stop in end_stops
    ]
    return JsonResponse(data, safe=False)

def get_schedules(request, start_point_code, end_point_code):
    schedules = BusSchedule.objects.filter(
        end_stop__stop__code=end_point_code, 
        end_stop__from_stop__code=start_point_code
        )
    data = [
        {
            "route": schedule.end_stop.stop.code,
            "dispatch": schedule.dispatch.strftime('%I:%M %p'),
            "arrival": schedule.arrival.strftime('%I:%M %p'),
            "fare": "AED 4.50 - 6.00",  # Adjust fare logic if needed
        }
        for schedule in schedules
    ]
    return JsonResponse(data, safe=False)

def get_bus_stops(request):
    # Fetch all bus stops from the database
    bus_stops = BusStop.objects.all().values('name', 'lat', 'lng')
    return JsonResponse(list(bus_stops), safe=False)


def temp_route(request):
    return render(request, 'index.html', {'route_view': True})
def load_data(request):
    
    with open('only_end_loc.csv', 'r') as file:
        reader = csv.reader(file)
        fields = next(reader)
        for stop in reader:
            BusStop.objects.create(
                name = stop[1],
                code = stop[0]
            )
    return HttpResponse("Data loaded successful")

def get_time_obj(time_string):
    hours, minutes = map(int, time_string.split(":"))
    time_obj = time(hour=hours, minute=minutes)
    return time_obj

def load_time_data(request):
    with open('stopFrom_stop_to.csv', 'r') as file:
        reader = csv.reader(file)
        fields = next(reader)
        counter = 1
        for stop in reader:
            start = stop[0]
            if start == "0":
                continue
            end_list = json.loads(stop[1])
            for end in end_list:
                if end == "0":
                    continue
                from_stop = BusStop.objects.get(code=start)
                end_stop = BusStop.objects.get(code=end)
                n = EndStop.objects.create(
                    from_stop=from_stop,
                    stop=end_stop
                )
                n.save()
                try:
                    with open(f'bus_schedule/{start}_to_{end}.csv', 'r') as f:
                        temp_reader = csv.reader(f)
                        temp_fields = next(temp_reader)
                        for row in temp_reader:
                            dispatch = get_time_obj(row[0])
                            arrival = get_time_obj(row[1])
                            BusSchedule.objects.create(
                                end_stop=n,
                                dispatch=dispatch,
                                arrival=arrival
                            )
                except:
                    print(f"Can't load data for {start}>{end}")
                
                            
                print(counter)
                counter+=1
    return HttpResponse("All data loaded successfully")


def starting_config(request):
    with open('address_with_code.csv', 'r') as file:
        reader = csv.reader(file)
        fields = next(reader)
        for row in reader:
            obj = BusStop.objects.get(code=row[0])
            obj.start = True
            obj.save()
    return HttpResponse("Starting points add successfully")

def load_location_data(request):
    with open('location_data.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            code = row[0]
            lat = row[2]
            lng = row[3]
            obj = BusStop.objects.get(code=code)
            obj.lat = lat
            obj.lng = lng
            obj.save()
    return HttpResponse("Location data loaded.")