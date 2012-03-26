import pygeoip
from datetime import datetime
from dateutil import tz
import pygame
import math
import sys
from pygame.locals import *

class Accesses:
    def __init__(self):
        self.access_list = []

class Access:
    def __init__(self):
        pass

# Convert a date and time in the format "10/Sep/2011:11:20:54" to a datetime object
def get_datetime_object(datetime_string):
    return datetime.strptime(datetime_string, '%d/%b/%Y:%H:%M:%S')


# Get the latitude (y) of the terminator given the longitude (x) and declination
def getTerminatorLat(long, decl):
    return math.arctan(-math.cos(long) / math.tan(decl))

# Get the declination of the Earth towards the Sun given a date (as a datetime object)
def getDecl(date):
    return
# Get the hour angle (tau) since the Sun last made a transit of the
# Earth's meridian, given a date (as a datetime object)
def getTau(date):
    return

def parse_file(filename):

    # Extract text from file
    infile = open(filename, 'r')
    lines = infile.readlines()
    infile.close()

    accesses = Accesses()

    for line in lines:

        # Make a new Access instance to describe and add to the list
        access_el = Access()

        # Parse IP address out of line
        ip_to_set = line.split()[0]
        access_el.ip = ip_to_set

        # Parse out date, time, and timezone information
        local_datetime = line.split()[3][1:]
        local_timezone = line.split()[4][:-1]
        datetime_object = get_datetime_object(local_datetime)
        # Add timezone to datetime
        timezone_seconds_offset = (int(local_timezone) / 100) * 3600
        datetime_object = datetime_object.replace(tzinfo = tz.tzoffset(None, timezone_seconds_offset))
        # Store datetime as UTC
        access_el.datetime_object = datetime_object.astimezone(tz.tzutc())

        accesses.access_list.append(access_el)

    return accesses

def add_geo_info(accesses):
    # Make GeoIP object for accessing GeoIP database
    gi = pygeoip.GeoIP('./GeoLiteCity.dat', pygeoip.STANDARD)

    # Go through accesses and add GeoIP information about each
    for i in range(len(accesses.access_list)):
        gir = gi.record_by_addr(accesses.access_list[i].ip)
        
        # Add geographical data for access to access object
        accesses.access_list[i].city = gir.get('city', '')
        accesses.access_list[i].region = gir.get('region', '')
        accesses.access_list[i].country = gir.get('country_name', '')
        accesses.access_list[i].lat = gir.get('latitude', '')
        accesses.access_list[i].long = gir.get('longitude', '')
    
    return accesses

# Displays a splash screen
def splash_screen():
    print "This program is copyright 2012 by Nat Guy."
    print "This product includes GeoLite data created by MaxMind, available from http://www.maxmind.com/."

# Opens the log file
def load_and_parse_log(filename):
    print "Loading and parsing log data..."
    accesses = parse_file(filename)
    accesses = add_geo_info(accesses)
    print "Log data parsed."
    return accesses

# Perform pygame graphics initialization
def pygame_init(screen_size):
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Server Log World Visualizer')
    return screen

# Load images from file for map
def load_images():
    # Load images of Earth during the day and night
    day_surface = pygame.image.load('earth_day_1200x600.jpg')
    night_surface = pygame.image.load('earth_night_1200x600.jpg')

    # Convert to pixel format for screen surface
    day_surface = day_surface.convert()
    night_surface = night_surface.convert()

    return day_surface, night_surface

# Debug output for access data
def debug_output(accesses, filename):
    outfile = open(filename, 'w')
    for access_el in accesses.access_list:
        outfile.write("City: " + access_el.city + '\n')
        outfile.write("Region: " + access_el.region + '\n')
        outfile.write("Country: " + access_el.country + '\n')
        outfile.write("Lat: " + str(access_el.lat) + '\n')
        outfile.write("Long: " + str(access_el.long) + '\n')
        outfile.write("Timetuple: " + str(access_el.datetime_object.timetuple()) + '\n========\n')

    outfile.close()

def main():

    filename = 'seahop_oct_2011_(test_log).log'
    accesses = load_and_parse_log(filename)
    debug_output(accesses, 'debug_log.txt')
    sys.exit()

    screen_size = [1200, 600]
    # Box which is moved across the map for daytime display
    day_box_width = 600
    day_box_height = screen_size[1]

    screen = pygame_init(screen_size)
    day_surface, night_surface = load_images()

    # Test -- fade between images by adjusting alphas
    day_alpha = 255
    night_alpha = 0
    darkening = True

    exit_request = False
    day_box_pos = 500
    while not exit_request:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit_request = True
        
        # Move day_box
        day_box_pos += 1
        if day_box_pos >= screen.get_size()[0]:
            day_box_pos = 0
        


        # Blit day to portion of surface covered by day_box
        if (day_box_pos + day_box_width) >= screen.get_size()[0]:
            day_box_width_to_draw = screen.get_size()[0] - (day_box_pos + day_box_width)
        else:
            day_box_width_to_draw = day_box_width


        screen.blit(day_surface, (day_box_pos, 0), pygame.rect.Rect(day_box_pos, 0, day_box_width, day_box_height))

        # Blit night portion of surface not covered by day_box
        night_box_width0 = day_box_pos
        if (day_box_pos + day_box_width) <= screen.get_size()[0]:
            night_box_width1 = screen.get_size()[0] - (day_box_pos + day_box_width)
        else:
            night_box_width1 = 0
        
        screen.blit(night_surface, (0, 0), pygame.rect.Rect(0, 0, night_box_width0, day_box_height))
        screen.blit(night_surface, ((day_box_pos + day_box_width_to_draw), 0), pygame.rect.Rect((day_box_pos + day_box_width_to_draw), 0, night_box_width1, day_box_height))

        pygame.display.flip()


    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        if darkening:
            day_alpha -= 1
            night_alpha += 1
            if (day_alpha == 0):
                darkening = False
        else:
            day_alpha += 1
            night_alpha -= 1
            if (day_alpha == 255):
                darkening = True

        day_surface.set_alpha(day_alpha)
        night_surface.set_alpha(night_alpha)
        screen.blit(day_surface, (0, 0))
        screen.blit(night_surface, (0, 0))
        pygame.display.flip()

    splash_screen()
    


if __name__ == '__main__':
    main()