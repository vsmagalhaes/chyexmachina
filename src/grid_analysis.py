import auxiliary as aux


def plotLineRatio(line1, line2):
    if isinstance(line1, line) and isinstance(line2, line):
    # proceed
    if True  ## equal grid points
    # proceed
    else:

        return -1
    else:
        aux.Misc().error_msg("One or both lines are not an instance of the Class < line >.")
        return -1


class line():
    ncol = []
    dens = []
    tex = []
    trad = []
    intInt = []
    tau = []
    temp = []
    nu = 0.0  ## its rest frequency in GHz
    grd_ncol = []
    grd_dens = []
    grd_temp = []
    valid = False

    def __init__(self, nu, grid, grid_type):
        self.nu = nu
        if grid_type == 'RADEX':
            for entry in grid:  # initialize grid points in ncol ndens
                if entry[4] == nu:
                    self.temp.append(entry[0])
                    self.dens.append(entry[1])
                    self.ncol.append(entry[2])
                    self.trad.append(entry[8])
                    self.tex.append(entry[6])
                    self.intInt.append(entry[11])
                    self.tau.append(entry[7])
                    if not (entry[0] in self.grd_temp):
                        self.grd_temp.append(entry[0])
                    if not (entry[1] in self.grd_dens):
                        self.grd_dens.append(entry[1])
                    if not (entry[2] in self.grd_ncol):
                        self.grd_ncol.append(entry[2])
        if len(self.temp) == 0:
            aux.Misc().error_msg("Line not found in grid!")
        else:
            self.valid = True

    def plot_line(self, xaxis, yaxis, selection):
        return 1
