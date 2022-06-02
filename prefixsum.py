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
import math
import ipaddress
import netaddr

POWER_OF_TW0 = [1, 2, 4, 8, 16, 32, 64, 128]


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
    return True if (iptoint(cidr_1)>>prefixbitcount(cidr_1))+1 == iptoint(cidr_2)>>prefixbitcount(cidr_1) else False

#def is_continuous(cidr_1, cidr_2):
#    return True if iptoint(cidr_1) + prefixtoint(cidr_1) == iptoint(cidr_2) else False

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

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


def check_affinity(cidr_a, cidr_b):
    ip_a = get_octets(cidr_a)
    ip_b = get_octets(cidr_b)

    if cidr_a.prefixlen >= 16 and cidr_a.prefixlen <= 24 and \
            cidr_b.prefixlen >= 16 and cidr_b.prefixlen <= 24:


        if ip_a[2] == ip_b[2]-1 and cidr_a.prefixlen == cidr_b.prefixlen:
            cidr_a.prefixlen = cidr_a.prefixlen-1
            return cidr_a
    return cidr_b


def summarization(cidr_list):
    for bits in range(25, 16, -1):
        index = 1
        print('-------------------------------')
        for cidr in cidr_list:
            print(f'{cidrtostr(cidr)} \t\t IP(HEX): {hex(iptoint(cidr))} BROADCAST(HEX): {hex(iptoint(cidr) + prefixtoint(cidr)-1)} - SHIFT(HEX): {hex(iptoint(cidr)>>prefixbitcount(cidr))}')
            if cidr.prefixlen == bits:
                if ipbitshift(cidr)%2 == 0 and index < len(cidr_list) and is_continuous(cidr, cidr_list[index]):
                    print(f'\tRemoving {cidrtostr(cidr_list[index])}')
                    cidr_list.pop(index)
                    cidr.prefixlen -=1
                    print(f'{cidrtostr(cidr)} is summarised')
            index+=1
    return cidr_list


# my own cidr summarization function 
def cidr_summarization(cidr_list):
    sum_cidr_list = []
    n = 0
    for i in range(len(cidr_list)):
        cidr = cidr_list[i]
        if i == len(cidr_list) - 1:
            sum_cidr_list.append(cidr)
            print(f'{cidrtostr(cidr)} the last record')
        else:
            if not is_continuous(cidr, cidr_list[i+1]):
                sum_cidr_list.append(cidr)
                print(f'{cidrtostr(cidr)} is not continuous')
            elif ipbitshift(cidr)%2 != 0:
                sum_cidr_list.append(cidr)
                print(f'{cidrtostr(cidr)} is not even')
            else:
                print(f'{cidrtostr(cidr)} is continuous, includes:')   
                x = i+1
                n = 0
                while x < len(cidr_list)-1 and is_continuous(cidr, cidr_list[x]):
                    print(f'\t{cidrtostr(cidr_list[x])}')                   
                    x+=1                    
                    n+=1
                    i+=1
#        print(f'{str(cidr.network)}/{str(cidr.prefixlen)} \t\t IP(HEX): {hex(iptoint(cidr))} BROADCAST(HEX): {hex(iptoint(cidr) + #prefixtoint(cidr)-1)} - SHIFT(HEX): {hex(iptoint(cidr)>>prefixbitcount(cidr))}')

#                n = count_continuous(cidr_list[i:])

#        x = i
#        n = 0 
#        while x < len(cidr_list)-1 and is_continuous(cidr_list[x], cidr_list[x+1]):
#            x+=1
#            n+=1
#        if n > 1:
#            print(f'n = {n}, i = {i}, x = {x}')
#           prefix_incr = POWER_OF_TW0.index(n)
#           if prefix_incr >= 0:
#                cidr.prefixlen += prefix_incr
#                print(f'Óptimization: increment {prefix_incr}, new network: {str(cidr.network)}/{str(cidr.prefixlen)}')
#                i += n
#            else:
#                prefix_incr = find_lowest_prefix(cidr_list[i, x])
#                print(f'Óptimization: increment {prefix_incr}, new network: {str(cidr.network)}/{str(cidr.prefixlen)}')

#        for x in range(i, len(cidr_list), 1):
#            is_continuous(cird,)
#        if i < len(cidr_list) - 1:
#            if ch
#            iprange = netaddr.IPSet(cidr, cidr_list)
#            if iprange.iscontiguous():
#                print(f'{cidr.network}/{cidr.prefixlen-1} summarization')
#            else:
#                print(str(cidr.network) + '/' + str(cidr.prefixlen))
#        else:
#            print(str(cidr.network) + '/' + str(cidr.prefixlen))
#        print(f'{str(cidr.network)}/{str(cidr.prefixlen)} - IP (HEX): {hex(iptoint(cidr))} - BROADCAST (HEX) {hex(iptoint(cidr) + #prefixtoint(cidr)-1)} - MASK (HEX): {hex(prefixtoint(cidr))} - {is_continuous(cidr, cidr_2)}')
#        print(f'{str(cidr.network)}/{str(cidr.prefixlen)} \t\t IP(HEX): {hex(iptoint(cidr))} BROADCAST(HEX): {hex(iptoint(cidr) + #prefixtoint(cidr)-1)} - SHIFT(HEX): {hex(iptoint(cidr)>>prefixbitcount(cidr))}')

#        if n == 0:
#            sum_cidr_list.append(cidr)
#        else:
#            if sum_cidr_list[n].network == cidr.network:
        
        
def print_cidr_list(cidr_list):
    for cidr in cidr_list:
        print(cidrtostr(cidr))




def main():
    if len(sys.argv) > 1:
        print('Open source prefix file:', sys.argv[1])
        cidr_list = load_prefix_file(sys.argv[1])
        print(f'\t{len(cidr_list)} found in the list')
#        print_ip_list(cidr_list)
        cidr_list.sort()
 
        if len(sys.argv) == 3:
            write_ip_list(sys.argv[2], cidr_list)

        summarized_cidr_list = netaddr.cidr_merge(cidr_list)
#        write_ip_list('output.txt', summarized_cidr_list)
#        print_ip_list(summarized_cidr_list)
#        print('-------------------------')
#        print(f'\t{len(summarized_cidr_list)} summarized list')

#        cidr_summarization(cidr_list)
        summarized_cidr_list = summarization(cidr_list)
        print(f'Summarization complete. New list has {len(summarized_cidr_list)} records.')
        print_cidr_list(summarized_cidr_list)
#        write_ip_list('my_summarization.txt', summarized_cidr_list)      

    else: 
        print('python3 prefixsum.py <input_source_prefix_list> <output_summarized_prefix_list>')

    return 0


if __name__ == '__main__':
    main()