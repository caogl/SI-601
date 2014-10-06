import matplotlib.pyplot as plt
import sqlite3, urllib2

import json, re, os
import sys

from math import sin, cos, sqrt, atan2, radians

############## Utility functions for finding distances via Google Geocode API ##############
# get_lat_long:  Fetch the latitude and longitude of a place name string using the Google geocode API
#
# Input:  name string, e.g. "Ann Arbor, MI"
# Output: a floating-point tuple containing the latitude and longitude, or [None, None] if not found
#
def get_lat_long(place):
    place = re.sub('\s','+', place)
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + place
    content = urllib2.urlopen(url).read()

    obj = json.loads(content)
    results = obj['results']

    lat = long = None
    if len(results) > 0:
        loc = results[0]['geometry']['location']
        lat = float(loc['lat'])
        long = float(loc['lng'])

    return [lat, long]

# Great circle distance between two points using the haversine formula
#
# pass the first point's latitude and longitude (in degrees) as a 2-tuple
# pass the second point's latitude and longitude (in degrees) as a 2-tuple
# returns -1 if either input point is invalid, i.e. negative degree values
def great_circle_distance(pt1, pt2):
    R = 6371.0   # mean radius of the Earth in km

    if (pt1[0] < 0 or pt2[0] < 0):
        return -1

    lat1_r = radians(pt1[0])
    lon1_r = radians(pt1[1])
    lat2_r = radians(pt2[0])
    lon2_r = radians(pt2[1])

    dlon = lon2_r - lon1_r
    dlat = lat2_r - lat1_r

    a = (sin(dlat/2))**2 + cos(lat1_r) * cos(lat2_r) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c

    return distance

def main():
	conn=sqlite3.connect(r'si-601-hw4_caogl.db')
	c=conn.cursor()
	
	sql='''
		SELECT e.school_name, p.hometown_name, CASE WHEN e.school_type = 'Graduate School' then 3
					    		    WHEN e.school_type='College' then 2
					   		    WHEN e.school_type='High School' then 1
						       END
		FROM FRIEND_PROFILE p, FRIEND_EDUCATION e
		WHERE p.friend_id=e.friend_id AND p.hometown_name!='NULL' 
	    '''
	c.execute(sql)
	result=c.fetchall()
	
	distanceList=[]
	school_level_list=[]
	for item in result:
		tp1=get_lat_long(item[0])
		tp2=get_lat_long(item[1])
		distance=great_circle_distance(tp1, tp2)
		if distance>=0:
			distanceList.append(distance)
			school_level_list.append(item[2])
	plt.scatter(school_level_list, distanceList)
	plt.xticks([1, 2, 3], ['High School', 'College', 'Graduate School'])
	plt.ylabel('Distance between school and hometown')
	plt.xlabel('Education level')
	plt.savefig('p4_graph_caogl.png')
main()
