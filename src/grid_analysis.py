import auxiliary as aux


def plotLineRatio(line1, line2):
    if isinstance(line1, line) and isinstance(line2, line):
    # proceed
    else:
        aux.Misc().error_msg("One or both lines are not an instance of the Class < line >.")
        return -1


class line():
    entries = []  ## its entries on the grid
    nu = 0.0  ## its rest frequency in GHz
    valid = False

    def __init__(self, nu, grid):
        self.nu = nu
        self.entries = []
        for entry in grid:
            if entry[4] == nu:
                self.entries.append(entry)
        if len(self.entries) == 0:
            aux.Misc().error_msg("Line not found in grid!")
        else:
            self.valid = True
