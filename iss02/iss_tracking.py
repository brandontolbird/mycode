import urllib.request
import json
import time
import turtle


def screen_setup(screen):
	screen.setup(720, 360) # set the resolution
	screen.setworldcoordinates(-180,-90,180,90)
	screen.bgpic('iss_map.gif')
	screen.register_shape('spriteiss.gif')
	iss = turtle.Turtle()
	iss.shape('spriteiss.gif')
	iss.setheading(90)
	return iss

def set_my_location(yellowlat, yellowlon):
	mylocation = turtle.Turtle()
	mylocation.penup()
	mylocation.color('yellow')
	mylocation.goto(yellowlon, yellowlat)
	mylocation.dot(5)
	mylocation.hideturtle()
	return mylocation

	
def get_iss_pos():
	## Trace the ISS - earth-orbital space station
	eoss = 'http://api.open-notify.org/iss-now.json'

	## Call the webserv
	trackiss = urllib.request.urlopen(eoss)

	## put into file object
	ztrack = trackiss.read()

	## json 2 python data structure
	result = json.loads(ztrack.decode('utf-8'))

	## display our pythonic data
	print("\n\nConverted python data")
	print(result)
	##input('\nISS data retrieved & converted. Press any key to continue')    

	location = result['iss_position']
	lat = location['latitude']
	lon = location['longitude']
	print('\nLatitude: ', lat)
	print('Longitude: ', lon)
	return lat, lon

def move_iss(iss, lat, lon):
	lon = round(float(lon))
	lat = round(float(lat))
	iss.penup()
	iss.goto(lon, lat)


def iss_passover(yellowlat, yellowlon):	
	passiss = 'http://api.open-notify.org/iss-pass.json'
	passiss = passiss + '?lat=' + str(yellowlat) + '&lon=' + str(yellowlon)
	response = urllib.request.urlopen(passiss)
	result = json.loads(response.read().decode('utf-8'))

	print(result) ## uncomment to see the downloaded result
	over = result['response'][1]['risetime']
	return over

def main():
	screen = turtle.Screen() # create a screen object
	iss = screen_setup(screen)
	yellowlat = 32.5165782
	yellowlon = -92.1014263
	mylat = input("Input new latitude: [{}]:".format(yellowlat))
	if mylat:
		yellowlat = mylat
	mylon = input("Input new longitude: [{}]:".format(yellowlon))
	mylocation = set_my_location(yellowlat, yellowlon)
	over = iss_passover(yellowlat, yellowlon)
	style = ('Arial', 6, 'bold')
	mylocation.write(time.ctime(over), font=style)
	while True:
		isslat, isslon = get_iss_pos()	
		move_iss(iss, isslat, isslon)
		time.sleep(5)
	turtle.mainloop()

if __name__ == "__main__":
	main()