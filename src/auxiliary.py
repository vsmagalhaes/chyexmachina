class Gridder():
    def write_grid_file(self, filename, *gridpars):
        if gridpars:
            print "file: " + filename + " written!"
        else:  # Manual input mode!
            print "Manual mode! not ready..."
        return 0

    def call_gridder(self, gridname, output):
        return 0


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
