import pygeoip

class Accesses:
    def __init__(self):
        self.ips = []
        self.dates = []
        self.timezones = []

def parse_file(filename):


    # Extract text from file
    infile = open(filename, 'r')
    lines = infile.readlines()
    infile.close()

    accesses = Accesses()

    for line in lines:
        # Parse IP address out of line
        accesses.ips.append(line.split()[0])


    return accesses

def parse_accesses(accesses):
    # Make GeoIP object for accessing GeoIP database
    gi = pygeoip.GeoIP('./GeoLiteCity.dat', pygeoip.STANDARD)

    outfile = open('geoip_output.txt', 'w')

    for ip in accesses.ips:
        # Get and output city
        record = gi.record_by_addr(ip)
        city = record['city']
        outfile.write(ip + ': ' + city + '\n')
    


def main():
    filename = 'seahop_oct_2011_(test_log).log'
    accesses = parse_file(filename)
    parse_accesses(accesses)


if __name__ == '__main__':
    main()