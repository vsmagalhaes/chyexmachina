import Tkinter as tk

import auxiliary as aux


class MainWindow(tk.Frame):
    counter = 0
    string = ''
    radexOn = 0

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        logo = tk.PhotoImage(file='../resources/Chy_ex_machina_logo.gif')
        logo_label = tk.Label(self, image=logo)
        logo_label.image = logo
        logo_label.grid(row=0, column=0, columnspan=5, padx=5, pady=5)

        self.button = tk.Button(self, text="Quit", command=self.quit, fg="red")
        self.button.grid(row=1, column=0, pady=5, padx=5)
        self.button.config(width=10, height=4)

        self.button = tk.Button(self, text="RADEX Grid\nInterface", command=self.radex_grids)
        self.button.grid(row=1, column=1, pady=5, padx=5)
        self.button.config(width=10, height=4)

        self.button = tk.Button(self, text="Analyse RADEX \n grid", command=self.not_implemented)
        self.button.grid(row=1, column=2, pady=5, padx=5)
        self.button.config(width=10, height=4)

        self.button = tk.Button(self, text="Run X^2 on\n RADEX grid", command=self.not_implemented)
        self.button.grid(row=1, column=3, pady=5, padx=5)
        self.button.config(width=10, height=4)

        self.button = tk.Button(self, text="LTE Calculations", command=self.LTE_window)
        self.button.grid(row=1, column=4, pady=5, padx=5)
        self.button.config(width=10, height=4)

    def not_implemented(self):
        frame = tk.Toplevel(self)
        aux.Misc().error_window(frame, "Interface not implemented yet.")

    def LTE_window(self):
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
            aux.Misc().error_window(t, "Another RADEX interface window already open!")
        else:
            self.radexOn += 1
            t.wm_title("RADEX grid Interface")
            toptxt = tk.Label(t, text="RADEX Griding interface")
            toptxt.grid(row=0, column=0, columnspan=2, pady=5)

            gr_name = aux.Gridder()
            name = gr_name.names
            desc = gr_name.pardescriptions
            exam = gr_name.examples
            stringpars = []
            for i in range(len(gr_name.names)):
                par = tk.StringVar()
                text = tk.Label(t, text=gr_name.names[i])
                text.grid(row=i + 1, column=0, pady=5, padx=5, sticky='w')
                field = tk.Entry(t, textvariable=par)
                field.grid(row=i + 1, column=1, pady=5, padx=5)
                stringpars.append(par)

            aux.Misc().help_button(t, lambda: self.call_helper( \
                name[0], desc[0], exam[0])).grid(row=1, column=3, padx=5, pady=5)
            aux.Misc().help_button(t, lambda: self.call_helper( \
                name[1], desc[1], exam[1])).grid(row=2, column=3, padx=5, pady=5)
            aux.Misc().help_button(t, lambda: self.call_helper( \
                name[2], desc[2], exam[2])).grid(row=3, column=3, padx=5, pady=5)
            aux.Misc().help_button(t, lambda: self.call_helper( \
                name[3], desc[3], exam[3])).grid(row=4, column=3, padx=5, pady=5)
            aux.Misc().help_button(t, lambda: self.call_helper( \
                name[4], desc[4], exam[4])).grid(row=5, column=3, padx=5, pady=5)
            aux.Misc().help_button(t, lambda: self.call_helper( \
                name[5], desc[5], exam[5])).grid(row=6, column=3, padx=5, pady=5)


            endbutton = tk.Button(t, fg='blue', text='Accept and Go!', \
                                  command=lambda: self.summon_gridder(t, stringpars[0], stringpars[1], stringpars[3] \
                                                                      , stringpars[2], stringpars[4], stringpars[5]))
            endbutton.grid(row=10, column=1, pady=10)
            cancelbutton = tk.Button(t, fg='red', text='Cancel', command=lambda: self.cancel_gridder(t))
            cancelbutton.grid(row=10, column=0, pady=10)

    def summon_gridder(self, frame, *gridpars):
        newGrid = aux.Gridder(*gridpars)
        if not self.status_check(newGrid.write_grid_file()):
            self.radexOn -= 1
            frame.destroy()
            return
        self.status_check(newGrid.call_gridder())
        self.radexOn -= 1
        frame.destroy()

    def cancel_gridder(self, t):
        self.radexOn -= 1
        t.destroy()

    def call_helper(self, parameter, description, example):
        frame = tk.Toplevel(self)
        aux.Misc().helper(frame, parameter, description, example)

    def status_check(self, status):
        if status == -1:
            t = tk.Toplevel(self)
            aux.Misc().error_window(t, aux.defaultMessage)
            return False
        elif status == 0:
            t = tk.Toplevel(self)
            aux.Misc().warn_window(t, aux.defaultMessage)
            return False
        else:
            return True

root = tk.Tk()
root.title("ChyExMachina Version: " + aux.version)
main = MainWindow(root)
main.pack(side="top", fill="both", expand=True)
root.mainloop()
