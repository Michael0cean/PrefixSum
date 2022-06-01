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

import os
import sys
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
def check_affinity(cidr_1, cidr_2):
    ip = [0,0,0,0]
    
    return

# my own cidr summarization function 
def cidr_summarization(cidr_list):
    sum_cidr_list = []
    n = 0
    for i in range(len(cidr_list)):
        cidr = cidr_list[i]
        if i < len(cidr_list) - 1:
            iprange = netaddr.IPSet(cidr, cidr_list)
            if iprange.iscontiguous():
                print(f'{cidr.network}/{cidr.prefixlen-1} summarization')
            else:
                print(str(cidr.network) + '/' + str(cidr.prefixlen))
        else:
            print(str(cidr.network) + '/' + str(cidr.prefixlen))

#        if n == 0:
#            sum_cidr_list.append(cidr)
#        else:
#            if sum_cidr_list[n].network == cidr.network:
        
        





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
        write_ip_list('output.txt', summarized_cidr_list)
#        print_ip_list(summarized_cidr_list)
#        print('-------------------------')
#        print(f'\t{len(summarized_cidr_list)} summarized list')
#        cidr_summarization(cidr_list)
    else: 
        print('python3 prefixsum.py <input_source_prefix_list> <output_summarized_prefix_list>')

    return 0


if __name__ == '__main__':
    main()