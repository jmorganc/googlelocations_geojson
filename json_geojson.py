#!/usr/bin/python

import json
import sys
from collections import defaultdict

"""
{
    "type":"FeatureCollection",
    "features":[
        {
            "type":"Feature",
            "geometry":{
                "type":"LineString",
                "coordinates":[
                    [-96.7459,32.95282,191],
                    [-96.74588,32.952847,182],
                    [-96.7447,32.952896,192]
                ]
             },
             "properties":{
                 "name":"Track",
                 "styleUrl":"#style_204",
                 "styleHash":-1702365,
	 "description":"<p>
                     Start: May 5, 2014 4:41:42 PM 
                     End: May 5, 2014 5:10:52 PM 
                     Duration: 29'10\" 
                     Elements: 852 
                     Length: 3.03mi 
                     Avg Speed: 6.24mph 
                     Max Speed: 7.83mph 
                     Low: 551ft 
                     High: 673ft 
                     Gain: 1936ft
                 </p>"
             }
        }
    ]
}
"""

def main():
    geojson = defaultdict(tuple)
    sorted_keys = list()

    with open('LocationHistory.json', 'r') as history_file:
        google_history = json.loads(history_file.read())
        for data in google_history['locations']:
            geojson[data['timestampMs']] = convert_lonlat(data['longitudeE7'], data['latitudeE7'])

        sorted_keys = sorted(geojson)
        max_timestamp = max(sorted_keys)

        with open('output.geojson', 'w') as output_file:
            output_file.write('{\n\t"type":"FeatureCollection",\n\t"features":[\n\t\t{\n\t\t\t"type":"Feature",\n\t\t\t"geometry":{\n\t\t\t\t"type":"LineString",\n\t\t\t\t"coordinates":[\n\t\t\t\t\t')
            for timestamp in sorted_keys:
                if timestamp == max_timestamp:
                    output_file.write('[{lon},{lat}]\n'.format(lon=geojson[timestamp][0], lat=geojson[timestamp][1]))
                else:
                    output_file.write('[{lon},{lat}],\n\t\t\t\t\t'.format(lon=geojson[timestamp][0], lat=geojson[timestamp][1]))
                del geojson[timestamp]
            output_file.write('\t\t\t\t]\n\t\t\t},\n\t\t\t"properties":{\n\t\t\t\t"name":"Track"\n\t\t\t}\n\t\t}\n\t]\n}')


def convert_lonlat(lon, lat):
    length_lon = len(str(abs(lon)))
    length_lat = len(str(abs(lat)))
    new_lon = lon
    new_lat = lat
    
    if length_lon < 9:
        for i in range(0, 9%length_lon):
            new_lon = new_lon * 10
    if length_lat < 9:
        for i in range(0, 9%length_lat):
            new_lat = new_lat * 10

    return (new_lon*10**-7, new_lat*10**-7)


def count_sizes(lon, lat):
    length_lon = len(str(abs(data['longitudeE7'])))
    if length_lon in test:
        test[length_lon] = test[length_lon] + 1
    else:
        test[length_lon] = 0
    length_lat = len(str(abs(data['latitudeE7'])))
    if length_lat in test:
        test[length_lat] = test[length_lat] + 1
    else:
        test[length_lat] = 0
    
    print test


if __name__ == '__main__':
    sys.exit(main())

