#!/usr/bin/env python2
# purpose: split a multi-sequence fasta file round-robin between the specified number of files
# usage: cat sequence.fa | python fasta-split.py prefix number_of_files
#  n.b. only works for fasta with one sequence per line

import sys

if len(sys.argv) != 3:
	print '\npurpose: split a multi-sequence fasta file round-robin between the specified number of files'
	print 'usage: cat sequence.fa | fasta-split.py prefix number_of_files'
	print ' n.b. only works for fasta with one sequence per line\n'
	quit()

pref = sys.argv[1]
numf = int(sys.argv[2])

curf = 0 # current file number
curline = 0 # counter for lines output to a given file

for line in sys.stdin:

#	if curf == numf - 1:
#		curf = 0

	curfilename = str(pref) + "." + str(curf).zfill(len(str(numf))) # pad with zeroes

	if curline == 0:
		with open(curfilename,"a") as current:
			current.write(line)
		curline = 1

	elif curline == 1:
		with open(curfilename,"a") as current:
			current.write(line)
		curline = 0
		curf += 1

		if curf == numf: # e.g. for 48 files, they will be numbered 0-47
			curf = 0

### EOF ###
