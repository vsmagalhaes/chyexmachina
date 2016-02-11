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
aux.writeInfo(fileout, "MiniTex")
fileout.write("#Source[1] Molecule[2] Transition[3] Frequency(GHz)[4] Opacity[5] sig(Opacity)[6] Intensity(K)[7] sig(intensity)(K)[8] Exc. Temp.(K)[9] sig(Exc. temp.)(K)[10]")
for i in range(len(values)):
    value = values[i]
    line = fileaslist[i]
    results = nl.calc_tex(value[1],value[2],value[3],value[4],value[0])
    fileout.write(line[:-1] + "\t{0:.4f}\t{1:.4f}\n".format(results[0], results[1]))
fileout.close()
