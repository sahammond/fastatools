#!/usr/bin/env python3

import sys
import re

embl = sys.argv[1]
BAD_FLAG = 'Fragment;'

class record(object):
    """an embl record"""

    # records are separated by "//"
    # "XX" are empty lines
    # fields of interest are ID DE KW SQ

    def __init__(self):
        self.ID = []; self.DE = []; self.KW = []; self.SQ = []


    def add_line(self,line):
        """add a line of an embl record"""
        if line[:2] != 'XX' and line[:2] != 'CC':
            try:
                rec = line.split("   ") # 3 spaces separate line tag and info
                lab = rec[0]
                con = rec[1]
            except IndexError as e:
                msg = f'\nline that produced error is \n{line}'
                print(e + msg)
                sys.exit(1)
            if lab == 'ID':
                nam = con.split(' ')[0]
                self.ID.append(nam)
            elif lab == 'DE':
                self.DE.append(con)
            elif lab == 'KW':
                self.KW.append(con)
            elif line[:2]  == '  ': # actual sequence lines have no label?
                sqn = line.strip('\n').split(' ')
                sqn = [x for x in sqn if x][:-1] # drop empty, select sequence
                self.SQ.append(sqn)
            else:
                pass # don't care about the rest


    def wrap_lines(self):
        outbuff = [self.ID, ' ', self.DE, self.KW]
        outbuff_wrap = [re.sub('\n',' ',' '.join(x)) for x in outbuff]
        outbuff_wrap.insert(0, '>')
        outbuff_join = ''.join(outbuff_wrap)

        return outbuff_join


    def print_sq(self):
        prebuff = [''.join(x) for x in self.SQ]
        outbuff = ''.join(prebuff)

        return outbuff


def main():
    with open(embl, 'r') as infile:
        rec = record() # initial record
        for line in infile:
            if line[:2] == '//':
                wrap = rec.wrap_lines()
                if BAD_FLAG not in wrap:
#                    print rec.wrap_lines()
                    print(wrap)
                    print(rec.print_sq())
                rec = record()
            else:
                rec.add_line(line)


if __name__ == '__main__':
    main()
