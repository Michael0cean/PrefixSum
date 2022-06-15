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


import sys
import ipaddress as ip

def load_show_ip_bgp(filename):
    header_skipper = True
#    with open(filename, 'r') as file:
#        for line in file:
    line = 'V*   1.0.4.0/22       212.66.96.126                          0 20912 6939 4826 38803 38803 38803 i'
    line = line.strip()
    if len(line) > 0 and header_skipper:
        bgp_keys = str(line[0:4]).strip()
        bgp_cidr = str(line[5:21]).strip()
        bgp_nhop = str(line[22:41]).strip()
        bgp_metric = str(line[42:48]).strip()
        bgp_locpref = str(line[49:55]).strip()
        bgp_weight = str(line[56:62]).strip()
        bgp_aspath = str(line[63:]).split()
        bgp_asn = bgp_aspath[-2] if len(bgp_aspath) > 1 and bgp_aspath[-1] == 'i' else 'Unknown'
        print(f'|{bgp_keys}|{bgp_cidr}|{bgp_nhop}|{bgp_metric}|{bgp_locpref}|{bgp_weight}| - {bgp_aspath} - {bgp_asn}')

                # main parse
#            elif not header_skipper and 'Network' in line and 'Next Hop' in line and 'Metric':



def main():
    load_show_ip_bgp('filename')
    return 0

if __name__ == '__main__':
    main()
