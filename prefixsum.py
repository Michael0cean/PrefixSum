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

def main():
    if len(sys.argv) != 1:
        print('python prefixsum.py <filename with prefixes>')
    else: 
        print('Try to open ',sys.argv[0])
    return 0


if __name__ == '__main__':
    main()