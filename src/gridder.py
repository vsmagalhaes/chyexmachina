#! /usr/bin/python


import argparse
import os
import time

import auxiliary as aux
import numlte as nl
import pyfi as fh

parser = argparse.ArgumentParser(description="Crunches a grid from Radex in a more treatable file")
parser.add_argument("infile", type=str, help="Grid input File")
parser.add_argument("output", type=str, help="Name of the Radex output file")
args = parser.parse_args()


filein = open(args.infile, 'r')
fileAsList = fh.strip_off_comm(filein)
filein.close()

molecule = fileAsList[0]
fileAsList = fh.float_file(fileAsList[1:])

colmin = fileAsList[0][0]
colmax = fileAsList[0][1]
ncoldens = int(fileAsList[0][2])
freqrange = [fileAsList[1][0], fileAsList[1][1]]
nmin = fileAsList[2][0]
nmax = fileAsList[2][1]
ndens = int(fileAsList[2][2])
temps = []
for temp in fileAsList[3]:
    temps.append(temp)
deltav = fileAsList[4][0]

tbg = nl.tbg


def write_input(infile, tkin, nh2, coldens, linewidth):
    infile.write(molecule[:-1] + '.dat\n')
    infile.write('/tmp/radex.out\n')
    infile.write("{0:.2f} {1:.2f}\n".format(freqrange[0], freqrange[1]))
    infile.write(str(tkin) + '\n')
    infile.write('1\n')
    infile.write('H2\n')
    infile.write(str(nh2) + '\n')
    infile.write(str(tbg) + '\n')
    infile.write(str(coldens) + '\n')
    infile.write(str(linewidth) + '\n')


start = time.time()

infile = open('/tmp/radex.inp', 'w')
i = 0
for temp in temps:
    for idens in range(ndens + 1):
        for icol in range(ncoldens + 1):

            dens = nmin * ((nmax / nmin) ** (float(idens) / ndens))
            colden = colmin * ((colmax / colmin) ** (float(icol) / ncoldens))
            dv = deltav
            write_input(infile, temp, dens, colden, dv)
            i += 1
            if (i == (len(temps) * (ndens + 1) * (ncoldens + 1))):
                infile.write('0\n')
                infile.close()
            else:
                infile.write('1\n')

os.system(aux.radex + ' < /tmp/radex.inp > /dev/null')

stop = time.time()
dure = stop - start
print "Run time = ", dure, "seconds"
os.system('mv radex.log /tmp/')
output = open(args.output, 'w')
aux.writeInfo(output, "Gridder")
output.write(
    "#   Tkin     Density       Cdens     Eup        Freq       Wavel        Tex        Tau         TR        Pop        Pop       flux       flux     Jup  Jlow\n")
output.write(
    "#      K        cm-3        cm-2       K         GHz        micr          K          -          K         Up        Low     K km/s  erg/cm2/s\n")
output.write(
    "#Col   1           2           3       4           5           6          7          8          9         10         11         12         13      14    15\n")
output.close()
os.system('grep -v \'!\' /tmp/radex.out >> ' + args.output)
