#!/usr/bin/python

import argparse

import auxiliary as aux
import numlte as nl
import pyfi as fh

### Fix description
parser = argparse.ArgumentParser(
    description="Calculates Column Densities from one input file with molecular and brightness information")
parser.add_argument("infile", type=str, help="Input file")
parser.add_argument("outfile", type=str, help="Output file")
args = parser.parse_args()

filein = open(args.infile, "r")

fileaslist = fh.strip_off_comm(filein, "#")
filein.close()

values = fh.float_file(fileaslist, skip=[0, 1, 2])
fileout = open(args.outfile, 'w')  # real option
aux.writeInfo(fileout,"MiniCol")
fileout.write("#Source[1] Molecule[2] Transition[3] Frequency (GHz)[4] Einstein Coef.(s^{-1})[5] En. Upper j(K)[6] Lower j[7]")
fileout.write(
    " Partition Func Q[8] Exc. Temp.(K)[9] sig(Exc. temp.)(K)[10] Opacity/Integ. int.(0|K*km/s)[11] sig(Opacity/Integ. int.)(0|K*km/s)[12]")
fileout.write(
    " Line width(km/s)[13] sig(Line width)(km/s)[14] Column dens.(cm^{-2})[15] sig(Column dens.(cm^{-2}))[16]\n")
for i in range(len(values)):
    value = values[i]
    line = fileaslist[i]
    results = nl.coldens(*value)
    fileout.write(line[:-1] + "\t{0:.4e}\t{1:.4e}\n".format(results[0], results[1]))
fileout.close()
