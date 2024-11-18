from main.models import BusStop
import csv
with open('address_with_code.csv', 'r') as file:
    reader = csv.reader(file)
    fields = next(reader)
    for stop in reader:
        BusStop.objects.create(
            name = stop[1],
            code = stop[0]
        )
        
