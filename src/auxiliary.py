import Tkinter as tk
import os
import time

softName = "Chyexmachina"
version = 'Prerelease'
moldir = '/Users/desouzav/Radex/moldat'
defaultMessage = 'Something went wrong see terminal window for details.'


def writeInfo(fileout, subname):
    fileout.write(
        "## Created by " + softName + ":" + subname + " Version: " + version + " on " + time.asctime() + ".\n")


class Misc():
    def error_window(self, frame, message):
        frame.wm_title("ERROR!")
        warn = tk.Label(frame, fg='red', text="ERROR: " + message)
        warn.pack(side='top', padx=5, pady=5)
        qt = tk.Button(frame, text='Ok', command=frame.destroy)
        qt.pack(side='bottom')

    def warn_window(self, frame, message):
        frame.wm_title("Warning")
        warn = tk.Label(frame, fg='purple', text="Warning: " + message)
        warn.pack(side='top', padx=5, pady=5)
        qt = tk.Button(frame, text='Ok', command=frame.destroy)
        qt.pack(side='bottom')

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
        else:  # manual mode
            print "Manual mode not ready"
            # _manual_grid()

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
        print self.gridOutFile
        self.gridOutFile += '.rdx'
        print self.gridInFile
        print self.gridOutFile
        if os.path.isfile(self.gridInFile) and not os.path.isfile(self.gridOutFile):
            os.system("python gridder.py " + self.gridInFile + " " + self.gridOutFile)
            return 1
        elif os.path.isfile(self.gridOutFile):
            Misc().warn_msg("Grid " + self.gridOutFile + " already run.")
            return 0
        else:
            Misc().error_msg("GRID could not be run, check file permissions.")
            return -1

class Minicol():
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
