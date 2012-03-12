import pygeoip

class Accesses:
    def __init__(self):
        self.access_list = []

class Access:
    def __init__(self):
        self.ip = ''
        self.date = ''
        self.time = ''
        self.timezone = ''

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
        date_time_to_set = line.split()[3][1:]
        date_to_set, time_to_set = date_time_to_set.split(':', 1)
        access_el.date = date_to_set
        access_el.time = time_to_set

        timezone_to_set = line.split()[4][:-1]
        access_el.timezone = timezone_to_set

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
            outfile.write("\nDate: " + access_el.date)
            outfile.write("\nTime: " + access_el.time)
            outfile.write("\nTimezone: " + access_el.timezone)
            outfile.write("\n\n")


def main():
    print "This product includes GeoLite data created by MaxMind, available from http://www.maxmind.com/."
    filename = 'seahop_oct_2011_(test_log).log'
    accesses = parse_file(filename)
    parse_accesses(accesses)


if __name__ == '__main__':
    main()