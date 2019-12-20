"""
This module contains functions to import data to the database from a file

NOTE: These functions will likely need to be change or even re-written as the data model changes
"""
import csv
from datetime import datetime
from sortedcontainers import SortedList

from django.contrib.gis.geos import fromstr, LineString, Point

from dashboard.models import Truck, Commune, Street

def load_trucks_csv(csv_path, fieldnames, headers=True):

    print('Reading truck CSV file')

    trucks_dict = {}
    with open(csv_path, newline='') as measurements:
        # fieldnames = [
        #     'req_timestamp', 'id_timestamp', 'id', 'long', 'lat', 'speed', 'direction', 'nationality', 'eurocode', 
        #     'MAM', 'measurement_timestamp', 'measurement_time', 'position', 'commune']
        reader = csv.DictReader(measurements, fieldnames=fieldnames)
        if headers:
            next(reader, None) #Skip first row if it is a header
        for row in reader:
            print(row)
            obu_id = row.get('id')
            measurement_time = datetime.fromisoformat(row.get('measurement_timestamp'))

            pos = row.get('position')
            if pos is None:
                x = float(row.get('long'))
                y = float(row.get('lat'))
                pos = Point(x,y)
            else:
                pos = fromstr(pos)
            vel = float(row['speed'])
            if obu_id not in trucks_dict:
                trucks_dict[obu_id] = {
                    'positions': SortedList([(pos, measurement_time)], key=lambda x: x[1]), #Keeptrack of positions sorted by time
                    'weight_category': int(row['MAM']) if row.get('MAM') is not None else None,
                    'velocities': [vel], #List of velocities to take the average at the end
                    'country_code': row.get('nationality'),
                    'euro_value': int(row['eurocode']) if row.get('eurocode') else None
                }
            else:
                truck = trucks_dict[obu_id]
                truck['positions'].add((pos, measurement_time))
                truck['velocities'].append(vel)
    # print(trucks_dict)

    print('Importing trucks in the database')

    for obu_id, truck_data in trucks_dict.items():
        velocities = truck_data['velocities']
        avg_vel = sum(velocities) / len(velocities)

        positions = truck_data['positions']
        last_pos = positions[-1][0]
        pos_list = []
        time_list = []

        # print(positions)
        for pos, dt in positions:
            pos_list.append(pos)
            time_list.append(dt.time())
        
        # print(pos_list)
        date = positions[0][1].date()
        route = LineString(pos_list) if len(pos_list) > 1 else LineString([])

        tr = Truck.objects.create(
            obu_id=obu_id, measurement_date=date, weight_category=truck_data['weight_category'], average_velocity=avg_vel, 
            country_code=truck_data['country_code'], euro_value=truck_data['euro_value'], last_position=last_pos,
            route=route)
        print(tr)
    
    print('Import done')

def load_roads_shp(data):
    print('Filtering out small roads')
    roads = [r for r in data[0] if r.get('code') > 5110 and r.get('code') < 5135] # Filter out roads that are to small

    print('Filtered out small roads')
    communes = Commune.objects.all()

    for com in communes:
        print('Loading roads for commune ' + com.name)
        com_geom = com.boundaries
        for road in roads:
            road_geom = road.geom.geos
            if road_geom.intersects(com_geom):
                bridge = True if road.get('bridge') == 'T' else False
                tunnel = True if road.get('tunnel') == 'T' else False
                Street.objects.create(name=road.get('name'), speed_limit=road.get('maxspeed'), one_way=road.get('oneway'), bridge=bridge, tunnel=tunnel, category=road.get('fclass'), commune=com, path=road_geom)
        
        print('Finished loading streets for ' + com.name)
