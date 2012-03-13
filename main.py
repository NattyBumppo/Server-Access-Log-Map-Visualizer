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

    outfile = open('geoip_output.txt', 'w')

    for access_el in accesses.access_list:

        gir = gi.record_by_addr(access_el.ip)

        if gir['city'] == '':
            outfile.write("Not found: " + repr(gir) + "\n\n")
        else:
            # Print data about access
            outfile.write("IP: " + access_el.ip)
            outfile.write("\nCity: " + gir['city'])
            outfile.write("\nDate: \n")
            string = ''
            for it in access_el.datetime_object.timetuple():
                string += str(it) + ' '
            string += '\n\n'
            outfile.write(string)

def main():
    print "This product includes GeoLite data created by MaxMind, available from http://www.maxmind.com/."
    filename = 'seahop_oct_2011_(test_log).log'
    accesses = parse_file(filename)
    parse_accesses(accesses)


if __name__ == '__main__':
    main()