#!/usr/bin/env python2

# identify proteins that are subsumed within a larger one
# uses my custom fasta reader
# https://github.com/sahammond/scripts/tree/master/fastatools

import sys

from fastatools import fasta_iter


class Protein(object):
    """simple class to hold protein sequences"""
    # input is a tuple of seqid, sequence
    def __init__(self, feature):
        self.name = feature[0]
        self.sqn = feature[1]
        self.length = len(self.sqn)
    
    def print_prot(self):
        printable = ''.join(['>', self.name, '\n', self.sqn])
        return printable


def main(fasta, prefix):
    # load data
    prots = {}
    with open(fasta, 'r') as infile:
        for rec in fasta_iter(infile):
            prot = Protein(rec)
            prots[prot.name] = prot

    # look for subsumed sequences
    subsumed = set()
    cnt = 0
    for key, value in prots.items():
        cnt += 1
        if cnt % 100 == 0:
            print '%s proteins checked' % cnt
        qry = value.sqn
        for rec in prots:
            # skip finding itself
            if key == rec:
                continue
            subj = prots[rec].sqn
            if qry in subj:
                subsumed.add(key)
                break

    # write out non-subsumed sequences
    print 'Number of input sequences is %s' % cnt
    print 'Number of sequences subsumed within another is %s' % len(subsumed)
    outname = '-'.join([prefix, 'nonSubsumed.fa'])
    outfile = open(outname, 'w')
    for key, value in prots.items():
        if key not in subsumed:
            print >> outfile, value.print_prot()
    outfile.close()


if __name__ == '__main__':
    fasta = sys.argv[1]
    prefix = sys.argv[2]
    main(fasta, prefix)
