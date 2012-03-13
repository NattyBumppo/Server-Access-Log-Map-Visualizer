import pygeoip
import datetime

class Accesses:
    def __init__(self):
        self.access_list = []

class Access:
    def __init__(self):
        pass

# Convert a date and time in the format "10/Sep/2011:11:20:54" to a datetime object
def get_datetime_object(datetime_string):
    return datetime.datetime.strptime(datetime_string, '%d/%b/%Y:%H:%M:%S')


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
        datetime_string = line.split()[3][1:]
        datetime_object = get_datetime_object(datetime_string)
        access_el.datetime_object = datetime_object

        accesses.access_list.append(access_el)

    return accesses

def parse_accesses(accesses):
    # Make GeoIP object for accessing GeoIP database
    gi = pygeoip.GeoIP('./GeoLiteCity.dat', pygeoip.STANDARD)

    # Go through accesses and add GeoIP information about each
    for i in range(len(accesses.access_list)):

        gir = gi.record_by_addr(accesses.access_list[i])

        # Add geographical data for access to access object
        accesses.access_list[i].city = gir['city']
        accesses.access_list[i].region = gir['region']
        accesses.access_list[i].country = gir['country_name']
        accesses.access_list[i].lat = gir['latitude']
        accesses.access_list[i].long = gir['longitude']
    
    return accesses

# Displays a splash screen
def splash_screen:
    print "This program is copyright 2012 by Nat Guy."
    print "This product includes GeoLite data created by MaxMind, available from http://www.maxmind.com/."

# Opens the log file, 
def load_and_parse(filename):
    filename = 'seahop_oct_2011_(test_log).log'
    print "Loading and parsing log data..."
    accesses = parse_file(filename)
    accesses = parse_accesses(accesses)
    print "Log data parsed."
    return accesses

def main():
    splash_screen()
    accesses = load_and_parse_log(filename)
    


if __name__ == '__main__':
    main()