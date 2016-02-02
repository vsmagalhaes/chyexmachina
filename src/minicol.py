#!/usr/bin/python

import argparse

import numlte as nl
import pyfi as fh

# When calculating from integrated intensity remenber!
# the is a DeltaJnu factor!!! (jnu(tex)-jnu(tbg))
# This will be dealt by the code, no need for the user to do this...


parser = argparse.ArgumentParser(
    description="Calculates Column Densities from one input file with molecular and brightness information")
parser.add_argument("infile", type=str, help="Input file")
parser.add_argument("outfile", type=str, help="Output file")
args = parser.parse_args()

filein = open(args.infile, "r")  # real option
# filein = open("../resources/teste_minicol_in.dat",'r') #test option
fileaslist = fh.strip_off_comm(filein, "#")
filein.close()

values = fh.float_file(fileaslist, skip=[0, 1, 2])

# fh.print_list_inlines(values)
# fh.print_list_inlines(identifiers)


fileout = open(args.outfile, 'w')  # real option
# fileout = open('../resources/teste_minicol_out.dat','w') #test option
fileout.write("#Source[1] Molecule[2] Transition[3] Frequency[4] Einstein Coef.[5] En. Upper j[6] Lower j[7]")
fileout.write(
    " Partition Func Q[8] Exc. Temp.[9] sig(Exc. temp.)[9] Opacity/Integ. int.[10] sig(Opacity/Integ. int.)[11]")
fileout.write(" Line width[12] sig(Line width)[13]\n")
for i in range(len(values)):
    value = values[i]
    line = fileaslist[i]
    results = nl.coldens(*value)
    fileout.write(line[:-1] + "\t{0:.4e}\t{1:.4e}\n".format(results[0], results[1]))
fileout.close()
