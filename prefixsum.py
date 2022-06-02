"""
Here is a short description of the script:
    execute the scripy:
        python prefixsum.py <filename with prefixes>
    where
        <filename with prefixes> - path + filename of the file with the list of
                                    prefixes to summarise in larger blocks in format
                                    IP network <space> netmask
                                    or
                                    IP network / prefix

"""

__author__ = "Mikhail Okunev"
__author_email__ = "Mikhail.Okunev@gmail.com"

from ipaddress import ip_address

import sys
import ipaddress
import netaddr


# Parsing the line to get an IP address and prefix or netmask
def get_prefix_from_str(line):
    if '/' in line:
        # try to parse xxx.xxx.xxx.xxx/xx
        cidr = netaddr.IPNetwork(line.split('/')[0])      
    else:
        # try to parse or xxx.xxx.xxx.xxx xxx.xxx.xxx.xxx
        splitted = line.split(' ')
        prefix = netaddr.IPAddress(splitted[1]).netmask_bits()
        cidr = netaddr.IPNetwork(splitted[0] + '/' + splitted[1])
    return cidr


# loading the file and creating the list of CIDRs
def load_prefix_file(filename):
    cidr_list = []
    with open(filename, 'r') as reader:
        for line in reader:
            line = line.strip()
            if len(line) > 0:
                cidr_list.append(get_prefix_from_str(line))
    return cidr_list


def print_ip_list(cidr_list):
    for cidr in cidr_list:
        print(cidr)

def write_ip_list(filename, cidr_list):
    with open(filename, 'w') as writer:
        for cidr in cidr_list:
            writer.write(f'{cidr}\n')

# check 
def cidrtostr(cidr):
    return str(cidr.network)+'/'+str(cidr.prefixlen)

def iptoint(cidr):
    return int(ipaddress.IPv4Address(cidr.ip))

def prefixbitcount(cidr):
    return 32-cidr.prefixlen

def prefixtoint(cidr):
    return int(2**(prefixbitcount(cidr)))

def ipbitshift(cidr):
    ip = iptoint(cidr)
    return ip>>prefixbitcount(cidr)

def is_continuous(cidr_1, cidr_2):
    return True if cidr_1.prefixlen == cidr_2.prefixlen and \
            (iptoint(cidr_1)>>prefixbitcount(cidr_1))+1 == iptoint(cidr_2)>>prefixbitcount(cidr_2) else False

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

"""
def get_prefix_incr(n):
    if is_integer(math.sqrt(n)):
        return int(math.sqrt(n))
    for i in range(0, 7):
        if n > 2**i and n < 2**(i+1):
            return i
    return 0

def get_octets(cidr):
    octets = []
    ip_str = str(cidr.network)
    ip_octets = ip_str.split('.')
    for octet in ip_octets:
        octets.append(int(octet))
    return octets
"""

def summarization(cidr_list):
    for bits in range(32, 16, -1):
        index = 1
        for cidr in cidr_list:
            if cidr.prefixlen == bits and ipbitshift(cidr)%2 == 0 and index < len(cidr_list) \
                    and is_continuous(cidr, cidr_list[index]):
                cidr_list.pop(index)
                cidr.prefixlen -=1
            index+=1
    return cidr_list


def main():
    if len(sys.argv) > 1:
        print('Open source prefix file:', sys.argv[1])

        cidr_list = load_prefix_file(sys.argv[1])
        print(f'\t{len(cidr_list)} prefixes found in the list')
        cidr_list.sort()

        # Summarization method 1
#        summarized_cidr_list = netaddr.cidr_merge(cidr_list)
#        print(f'Summarization 1 complete. New list has {len(summarized_cidr_list)} records.')

        # Summarization method 2
        summarized_cidr_list = summarization(cidr_list)
        print(f'Summarization 2 complete. New list has {len(summarized_cidr_list)} records.')

        if len(sys.argv) == 3:
            write_ip_list(sys.argv[2], summarized_cidr_list)

    else: 
        print('python3 prefixsum.py <input_source_prefix_list> <output_summarized_prefix_list>')

    return 0


if __name__ == '__main__':
    main()