#!/usr/bin/env python3
import urllib.request
import json
import webbrowser
import pprint

## Define APOD 
neourl = 'https://api.nasa.gov/neo/rest/v1/feed?'
startdate = 'start_date=2018-06-01'
enddate = '&end_date=END_DATE'
mykey = '&api_key=yJ0JEFG0aP47UlJBw5s5V6iQ8YHnVzyPNbVEOS1Z'    ## your key goes in place of DEMO_KEY

prompt = input("Input start date as YYYY-MM-DD: ")
if prompt:
    startdate = 'start_date=' + prompt
prompt = input("Input end date as YYYY-MM-DD: ")
if prompt:
    enddate = '&end_date=' + prompt
    startdate = startdate + enddate

neourl = neourl + startdate + mykey

## Call the webservice
neourlobj = urllib.request.urlopen(neourl)

## read the file-like object
neoread = neourlobj.read()

## decode json to python data structure
decodeneo = json.loads(neoread.decode('utf-8'))

## display our pythonic data
print("\n\nConverted python data")
pprint.pprint(decodeneo)
with open("output.txt","w") as neo_out:
    neo_out.write(pprint.pformat(decodeneo))

neos = decodeneo.get('near_earth_objects')

def convert_to_moonlen(miss_distance):
    return float(miss_distance)/238900

total_neo=0
for date, date_list in neos.items():
    print("Date: {}".format(date))
    for item in date_list:
        miss_distance = item.get('close_approach_data',[dict()])[0].get('miss_distance',dict()).get('miles',0)
        total_neo+=1
        print("Object name: {} miss_distance(miles): {} (in moon length): {}".format(item.get('name'),
              miss_distance, convert_to_moonlen(miss_distance)))
print("Total NEO:",total_neo)
