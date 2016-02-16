## User configurable parameters:
## Dependant on your machine RADEX instalation

moldir = '/Users/desouzav/Radex/moldat'
radex = '/Users/desouzav/Radex/bin/radex'

## Do not mess below if you don't know the leveled flying speed of an african swallow

import Tkinter as tk
import os
import time

import numpy as np

import numlte as nl

softName = "Chyexmachina"
version = 'Prerelease 0.3'
defaultMessage = 'Something went wrong see terminal window for details.'


def writeInfo(fileout, subname):
    """
    Writes first header line on output files
    :param fileout: File for the header line to be written
    :param subname: Subrutine calling the method
    :return: No return
    """
    fileout.write(
        "## Created by " + softName + ":" + subname + " Version: " + version + " on " + time.asctime() + ".\n")


class Misc():
    """
    Class containing miscellaneous tasks regarding window management, error and warning displays,
    Parameter parsing, helper buttons.
    """
    def error_window(self, frame, message):
        """
        Prompts an error window for the user
        :param frame: tk input parameter
        :param message: Message to be displayed in the error window
        :return: No return
        """
        frame.wm_title("ERROR!")
        err = tk.Label(frame, fg='red', text="ERROR: " + message)
        err.pack(side='top', padx=5, pady=5)
        qt = self.ok_button(frame)

    def warn_window(self, frame, message):
        """
        Prompts an warning window for the user
        :param frame: tk input parameter
        :param message: Message to be displayed in the warning window
        :return: No return
        """
        frame.wm_title("Warning")
        warn = tk.Label(frame, fg='purple', text="Warning: " + message)
        warn.pack(side='top', padx=5, pady=5)
        qt = self.ok_button(frame)

    def error_msg(self, message):
        """
        Displays an error message on the terminal, more versatile on how to be called than error window.
        :param message: Message to be displayed
        :return: no return
        """
        print '\n'
        self.draw_attention(40)
        print "ERROR: " + message
        self.draw_attention(40)
        print '\n'

    def warn_msg(self, message):
        """
        Displays a warning message on the terminal, more versatile on how to be called than warning window.
        :param message: Message to be displayed
        :return: no return
        """
        print '\n'
        self.draw_attention(40)
        print "Warning: " + message
        self.draw_attention(40)
        print '\n'

    def draw_attention(self, times):
        """
        Prints a string of #
        :param times: how many # in the string
        :return: No return
        """
        saida = ''
        for i in range(times):
            saida += '#'
        print saida

    def helper(self, frame, par, desc, exam):
        """
        Configures a help window for a parameter
        :param frame: Parent tk frame
        :param par: Name of the parameter for the help
        :param desc: Description of the parameter
        :param exam: example of usage of the parameter
        :return: No return
        """
        frame.wm_title("Help for: " + par)
        frame.config(bg='yellow')
        helping = tk.Message(frame, width=300, bg='yellow',
                             text=par + "\n\nDescription: \n\n" + desc + "\n\n Example:\n\n\t" + exam)
        helping.pack(side='top')
        accept = self.ok_button(frame)

    def ok_button(self, frame):
        """
        Simple ok button
        :param frame: parent tk frame
        :return: the ok button
        """
        return tk.Button(frame, text='Ok', command=frame.destroy).pack(side='bottom')

    def help_button(self, frame, help_com):
        """
        a prototypical help_button.
        :param frame: Parent tk frame for the button
        :param help_com: command to be executed by the help button
        :return: Help button
        """
        return tk.Button(frame, text='Help', command=help_com, fg='orange')

    def get_par_from_sv_werr(self, sv):
        parw = sv.get().split()
        if len(parw) == 1:
            par = float(parw[0])
            epar = 0.0
            status = 1
        elif len(parw) == 2:
            par = float(parw[0])
            epar = float(parw[1])
            status = 1
        elif len(parw) > 2:
            par = float(parw[0])
            epar = float(parw[1])
            status = 0
            self.warn_msg("More than 2 parameters given...")
        else:
            par = None
            epar = None
            status = -1
            self.error_msg("No parameters given")
        return par, epar, status

    def get_par_from_sv_nerr(self, sv):
        parw = sv.get().split()
        if len(parw) == 1:
            par = float(parw[0])
            status = 1
        elif len(parw) > 1:
            par = float(parw[0])
            status = 0
            self.warn_msg("More than 1 parameter given...")
        else:
            par = None
            status = -1
            self.error_msg("No parameters given")
        return par, status

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


class LTE:
    class tex:
        parnames = ["Opacity: ", 'Intensity [K] :', 'Frequency [GHz] :']
        pardesc = ['Total opacity of the line',
                   'Main beam scale line intensity in Kelvins',
                   'Rest frequency of the line']
        parexam = ['4.7 ## No uncertainty\n\t4.7 1.0 ## Uncertainty of 1.0',
                   '2.5 ## No uncertainty\n\t2.5 0.1 ## Uncertainty of 0.1',
                   '340 ## No uncertainty']

        def calculate_Tex(self, result_sv, *args):
            tau, etau, status1 = Misc().get_par_from_sv_werr(args[0])
            tr, etr, status2 = Misc().get_par_from_sv_werr(args[1])
            nu, status3 = Misc().get_par_from_sv_nerr(args[2])
            status = [status1, status2, status3]
            if -1 in status:
                result_sv.set("ERROR!")
            else:
                tex, etex = nl.calc_tex(tau, etau, tr, etr, 1e9 * nu)
                result_sv.set("{0:.2f} +- {1:.2f}".format(tex, etex))

    class col:
        parnames = ["Frequency [GHz]",
                    "Einsteins Coefficient [s^{-1}]",
                    "Upper level Degeneracy",
                    "Upper level Energy [K]",
                    "Lower level Quantum number",
                    "Partition Function at given Tex []",
                    "Excitation Temperature [K]",
                    "Excitation Temperature error [k]",
                    "Opacity/Integrated Intensity [n/a]/[K*km/s]",
                    "Opacity/Integrated Intensity error [n/a]/[K*km/s]",
                    "Line width [km*s^{-1}]",
                    "Line width error [km*s^{-1}]]"]
        pardesc = ['Total opacity of the line',
                   'Main beam scale line intensity in Kelvins',
                   'Rest frequency of the line']
        parexam = ['4.7 ## No uncertainty\n\t4.7 1.0 ## Uncertainty of 1.0',
                   '2.5 ## No uncertainty\n\t2.5 0.1 ## Uncertainty of 0.1',
                   '340 ## No uncertainty']

        def save_mol_pars(self):
            return 1


    class bb:
        bnuNames = ["Temperature [K]", "Frequency [GHz]", "Flux [Jy]"]
        jnuNames = ["Temperature [K]", "Frequency [GHz]", "Intensity [K]"]
        emergNames = ["Excitation Temperature[K]", "Opacity", "Frequency [GHz]", "Intensity [K]"]

        helpbnu = ["Bnu/Ibnu", "calculate Bnu ibnu", "example"]
        helpjnu = ["jnu/Ijnu", "calculate jnu ijnu", "example"]
        helpemerg = ["", "", ""]

        def decide_bnu_ibnu(self, pars):
            temp = pars[0].get()
            nu = pars[1].get()
            flux = pars[2].get()
            if temp == "" and (nu != "") and (flux != ""):
                nuf = 1.0e9 * float(nu)
                fluxf = float(flux)
                tempf = nl.ibnu(fluxf, nuf)
                pars[0].set("{0:.3f}".format(tempf))
                return 1
            elif flux == "" and (nu != "") and (temp != ""):
                nuf = 1.0e9 * float(nu)
                tempf = float(temp)
                fluxf = nl.bnu(tempf, nuf) / nl.jy2erg
                pars[2].set("{0:.3e}".format(fluxf))
                return 1
            elif (flux != "") and (nu != "") and (temp != ""):
                Misc().warn_msg("All parameters Filled.")
                return 0
            elif (flux == "") and (nu == "") and (temp == ""):
                Misc().warn_msg("No parameters Filled.")
                return 0
            elif flux != "" and (nu == "") and (temp != ""):
                Misc().error_msg("You have to type in the Frequency.")
                return -1
            else:
                Misc().error_msg("Something went really wrong, contact developer.")
                return -1

        def decide_jnu_ijnu(self, pars):
            """
            ***NEEDS PARAMETERS RENAMING!!! but it works!
            :param pars:
            :return:
            """
            temp = pars[0].get()
            nu = pars[1].get()
            flux = pars[2].get()
            if temp == "" and (nu != "") and (flux != ""):
                nuf = 1.0e9 * float(nu)
                fluxf = float(flux)
                tempf = nl.ijnu(fluxf, nuf)
                pars[0].set("{0:.3f}".format(tempf))
                return 1
            elif flux == "" and (nu != "") and (temp != ""):
                nuf = 1.0e9 * float(nu)
                tempf = float(temp)
                fluxf = nl.jnu(tempf, nuf)
                pars[2].set("{0:.3e}".format(fluxf))
                return 1
            elif flux != "" and (nu == "") and (temp != ""):
                Misc().error_msg("You have to type in the Frequency.")
                return -1
            elif (flux != "") and (nu != "") and (temp != ""):
                Misc().warn_msg("All parameters Filled.")
                return 0
            elif (flux == "") and (nu == "") and (temp == ""):
                Misc().warn_msg("No parameters Filled.")
                return 0
            else:
                Misc().error_msg("Something went really wrong, contact developer.")
                return -1

        def calc_emerging(self, pars):
            tex = pars[0].get()
            tau = pars[1].get()
            nu = pars[2].get()
            if tex != '' and tau != '' and nu != '':
                texf = float(tex)
                tauf = float(tau)
                nuf = float(nu)
                dejnu = nl.djnu(texf, nl.tbg, nuf)
                emerg = dejnu * (1 - np.exp(-1.0 * tauf))
                pars[3].set("{0:.2f}".format(emerg))
                return 1
            elif tex == '' and tau == '' and nu == '':
                Misc().warn_msg("No parameters given.")
                return 0
            else:
                Misc().error_msg("All parameters need to be given.")
                return -1

    def manual_input(self, filename):
        return 0

    def write_input(self, filename):
        return 0

    def call_minicol(self, filename):
        return 0


class Chi_Machine():
    def input_grids(self, *gridnames):
        return 0

    def call_chimachine(self, gridnames, obs):
        return 0


class Grid_Analisys():
    plotdev = 0
