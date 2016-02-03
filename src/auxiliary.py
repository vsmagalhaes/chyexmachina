## User configurable parameters:
## Dependant on your machine RADEX instalation

moldir = '/Users/desouzav/Radex/moldat'
radex = '/Users/desouzav/Radex/bin/radex'

## Do not mess below if you don't know the leveled flying speed of an african swallow

import Tkinter as tk
import os
import time

softName = "Chyexmachina"
version = 'Prerelease 0.1'
defaultMessage = 'Something went wrong see terminal window for details.'


def writeInfo(fileout, subname):
    fileout.write(
        "## Created by " + softName + ":" + subname + " Version: " + version + " on " + time.asctime() + ".\n")


class Misc():
    def error_window(self, frame, message):
        frame.wm_title("ERROR!")
        err = tk.Label(frame, fg='red', text="ERROR: " + message)
        err.pack(side='top', padx=5, pady=5)
        qt = self.ok_button(frame)

    def warn_window(self, frame, message):
        frame.wm_title("Warning")
        warn = tk.Label(frame, fg='purple', text="Warning: " + message)
        warn.pack(side='top', padx=5, pady=5)
        qt = self.ok_button(frame)

    def error_msg(self, message):
        print '\n'
        self.draw_attention(40)
        print "ERROR: " + message
        self.draw_attention(40)
        print '\n'

    def warn_msg(self, message):
        print '\n'
        self.draw_attention(40)
        print "Warning: " + message
        self.draw_attention(40)
        print '\n'

    def draw_attention(self, times):
        saida = ''
        for i in range(times):
            saida += '#'
        print saida

    def helper(self, frame, par, desc, exam):
        frame.wm_title("Help for: " + par)
        frame.config(bg='yellow')
        helping = tk.Message(frame, width=300, bg='yellow',
                             text=par + "\n\nDescription: \n\n" + desc + "\n\n Example:\n\n\t" + exam)
        helping.pack(side='top')
        accept = self.ok_button(frame)

    def ok_button(self, frame):
        return tk.Button(frame, text='Ok', command=frame.destroy).pack(side='bottom')

    def help_button(self, frame, help_com):
        return tk.Button(frame, text='Help', command=help_com, fg='orange')


class Gridder():
    molecule = ''
    gridInFile = ''
    gridOutFile = ''
    pars = []
    gridfolder = '../resources/grids/'
    if not os.path.exists(gridfolder):
        os.system("mkdir " + gridfolder)
    parnames = ['## Column density [cm^{-2}]: min, max, n\n', \
                '## Frequencies [GHz]: min, max\n', \
                '## Number densitiy [cm^{-3}]: min, max, n\n', \
                '## Temperatures [K]:\n', \
                '## Line Width [km/s]:\n', ]
    pardescriptions = ['Molecular file for RADEX calculations as in ' + moldir + '.', \
                       'Column densities for the RADEX grid, minimum value, maximum value, number of values.', \
                       'Number densities for the RADEX grid, minimum value, maximum value, number of values.', \
                       'Minimum and maximum frequencies for RADEX spectral features selection.', \
                       'Temperatures for the RADEX grid as space separated values.', \
                       'Line width for the RADEX grid, 1 is expected for most cases, specially if a Chi Square is intended to be done later.']
    names = ['Molecule: ', \
             'Column densities [cm^{-2}] : ', \
             'Number densities [cm^{-3}] : ', \
             'Frequencies [GHz] : ', \
             'Temperatures [K] : ', \
             'Line width [km/s] : ']

    examples = ['cn-h2-hfs', \
                '1e10 1e14 5', \
                '1e3 1e5 5', \
                '330 350', \
                '5 8 10 12', \
                '1']

    def __init__(self, *gridpars):
        if gridpars:
            self.molecule = gridpars[0].get()
            self.pars = []
            for i in range(1, len(gridpars)):
                self.pars.append(gridpars[i].get())
            self.gridInFile = self.gridfolder + self.molecule
            timenow = time.localtime()
            for i in range(6):
                self.gridInFile += "-" + str(timenow[i])
            self.gridInFile += '.grd'
        else:  # empty instanciation
            print "Initiating Grid parameters"

    def write_grid_file(self):
        if os.path.isfile(moldir + "/" + self.molecule + ".dat"):
            output = open(self.gridInFile, 'w')
            writeInfo(output, "Gridder:write_grid")
            output.write("## Molecule: \n")
            output.write(self.molecule + '\n')
            for i in range(len(self.pars)):
                output.write(self.parnames[i])
                output.write(self.pars[i] + '\n')
            output.close()
            return 1
        else:
            Misc().error_msg("LAMDA file for " + self.molecule + " does not exist in:\n" + moldir)
            return -1

    def call_gridder(self):
        self.gridOutFile = self.gridInFile[:-4]
        self.gridOutFile += '.rdx'

        if os.path.isfile(self.gridInFile) and not os.path.isfile(self.gridOutFile):
            print "Starting to run Grid..."
            os.system("python gridder.py " + self.gridInFile + " " + self.gridOutFile)
            return 1
        elif os.path.isfile(self.gridOutFile):
            Misc().warn_msg("Grid " + self.gridOutFile + " already run.")
            return 0
        else:
            Misc().error_msg("GRID could not be run, check file permissions.")
            return -1


class LTE():
    def manual_input(self, filename):
        return 0

    def write_input(self, filename):
        return 0

    def call_minicol(self, filename):
        return 0


class ChiMachine():
    def input_grids(self, *gridnames):
        return 0

    def call_chimachine(self, gridnames, obs):
        return 0
