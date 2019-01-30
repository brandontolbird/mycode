#!/usr/bin/env python3
#
import urllib.request
import json
import webbrowser
from pprint import pprint as pp # part of the standard libray

## define some constants
NASAAPI = 'https://api.nasa.gov/planetary/apod?' # this is our api to call
MYKEY = 'api_key=DEMO_KEY' ## this is our api key

## pretty print json
def main():
    """ask user for date"""
    input_str = input("Enter date to pull APOD in YYYY-MM-DD [today]: ")
    if input_str and input_str == "today":
        DATE = None
    else:
        DATE = "&date=" + input_str
    """run-time code"""
    if DATE:
        nasaapiobj = urllib.request.urlopen(NASAAPI + MYKEY + DATE) # call the webservice
    else:
        nasaapiobj = urllib.request.urlopen(NASAAPI + MYKEY)
    nasaread = nasaapiobj.read() # parse the JSON blob returned
    convertedjson = json.loads(nasaread.decode('utf-8')) # convert json

    # Show converted json
    # print(convertedjson) # show convereted JSON without pprint
    # input('\nThis is converted json. Press ENTER to continue.') # pause for enter

    # Show Pretty Print json
    # pp(convertedjson) # this is pretty print in action
    # pprint.pprint(convertedjson) # if you do a simple import pprint, the result is a long usage
    # input('\nThis is pretty printed JSON. Press ENTER to continue.') # pause for ENTER

    # Print the description of the photo we are about to view
    print("Title: " + convertedjson['title'])
    print("Date: " + convertedjson['date'])
    print("Explanation: " + convertedjson['explanation']) # display the value for the key explanation
    prompt = input('Input "save", "view", or "exit" to \nsave the image, open it in the '
                   'browser or exit, respectively: ') # pause for ENTER
    if prompt == "save":
         img_data = urllib.request.urlopen(convertedjson['hdurl'])
         filename = convertedjson['hdurl'].split('/')[-1]
         with open(filename,'wb') as img_fh:
             img_fh.write(img_data.read())
    elif prompt == "view":
        webbrowser.open(convertedjson['hdurl']) # open in the webbrowser

main()


