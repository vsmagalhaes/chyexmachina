import Tkinter as tk


class MainWindow(tk.Frame):
    counter = 0
    string = ''
    radexOn = 0

    # iotext = tk.StringVar()



    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.button = tk.Button(self, text="Window 1", fg="red", command=self.nicetry)
        self.button.pack(side=tk.LEFT)

        self.button = tk.Button(self, text="Radex Interface", command=self.radex_grids)
        self.button.pack(side="left")

        self.button = tk.Button(self, text="Quit", command=self.quit)
        self.button.pack(side='bottom')

    def nicetry(self):
        t = tk.Toplevel(self)
        t.wm_title("Another window")

        warning = tk.Label(t, text="A small step for a man\nEven smaller for mankind...")
        warning.pack(side="top", padx=100, pady=100)

        iotext = tk.StringVar()
        iotext.set("Type something here")
        inputText = tk.Entry(t, textvariable=iotext)
        inputText.pack(side='top', pady=10)

        finish = tk.Button(t, text="Apply changes and go", fg="blue", command=lambda: self.goshow(iotext, t))
        finish.pack(side='top', pady=10)

    def goshow(self, iotext, t):
        ster = iotext.get()
        if ster == "HCN":
            print "Cyanide!"
            t.destroy()
        else:
            iotext.set("Molecule not found, retry")

    def radex_grids(self):
        t = tk.Toplevel(self)
        if self.radexOn:
            t.wm_title("ERROR!")
            warn = tk.Label(t, text="ERROR: Another RADEX interface window already open!")
            warn.pack(side='top')
            qt = tk.Button(t, text='Ok', command=t.destroy)
            qt.pack(side='bottom')
        else:
            self.radexOn += 1
            t.wm_title("RADEX grid Interface")
            toptxt = tk.Label(t, text="RADEX Griding interface")
            toptxt.grid(row=0)
            # .pack(side="top", fill="both", expand=True, pady=10)
            mole = tk.StringVar()
            cdens = tk.StringVar()
            ndens = tk.StringVar()
            freqs = tk.StringVar()
            temps = tk.StringVar()
            dvel = tk.StringVar()
            text = tk.Label(t, text='Molecule: ')
            text.grid(row=1, column=0, pady=5, padx=5)
            field = tk.Entry(t, textvariable=mole)
            field.grid(row=1, column=1, pady=5, padx=5)
            text = tk.Label(t, text='Column densities [cm^{-2}] : ')
            text.grid(row=2, column=0, pady=5, padx=5)
            field = tk.Entry(t, textvariable=cdens)
            field.grid(row=2, column=1, pady=5, padx=5)
            text = tk.Label(t, text='Number densities [cm^{-3}] : ')
            text.grid(row=3, column=0, pady=5, padx=5)
            field = tk.Entry(t, textvariable=ndens)
            field.grid(row=3, column=1, pady=5, padx=5)
            text = tk.Label(t, text='Frequencies [GHz] : ')
            text.grid(row=4, column=0, pady=5, padx=5)
            field = tk.Entry(t, textvariable=freqs)
            field.grid(row=4, column=1, pady=5, padx=5)
            text = tk.Label(t, text='Temperatures [K] : ')
            text.grid(row=5, column=0, pady=5, padx=5)
            field = tk.Entry(t, textvariable=temps)
            field.grid(row=5, column=1, pady=5, padx=5)
            text = tk.Label(t, text='Thermal+turbulent line width [km/s] : ')
            text.grid(row=6, column=0, pady=5, padx=5)
            field = tk.Entry(t, textvariable=dvel)
            field.grid(row=6, column=1, pady=5, padx=5)

            endbutton = tk.Button(t, text='Accept and Go!', command=lambda: self.summon_gridder(t))
            endbutton.grid(row=10, column=1, pady=10)

    def summon_gridder(self, t):
        self.radexOn -= 1
        # aux.Gridder.write_grid_file()
        # aux.Gridder.call_gridder()
        t.destroy()


root = tk.Tk()
root.title("Empty GUI")
main = MainWindow(root)
main.pack(side="top", fill="both", expand=True, padx=200, pady=200)
root.mainloop()
