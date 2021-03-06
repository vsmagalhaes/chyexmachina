#! /usr/bin/python


import Tkinter as tk

import auxiliary as aux


class MainWindow(tk.Frame):
    counter = 0
    string = ''
    radexOn = 0
    lteOn = 0

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        logo = tk.PhotoImage(file='../resources/Chy_ex_machina_logo.gif')
        logo_label = tk.Label(self, image=logo, text='teste')
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
        if self.lteOn:
            aux.Misc().error_window(t, "Another LTE Calculations window already open!")
        else:
            self.lteOn += 1
            t.wm_title("LTE Calculations window")

            description = tk.Label(t, text="Local Thermodynamical Equilibrium\napproximation calculations")
            description.grid(row=0, column=0, columnspan=3)
            # description.config(fg='blue',bg='red')

            tex_desc = tk.Label(t, text="Calculate\n Excitation temperature")
            tex_desc.grid(row=1, column=0, pady=5)

            tex_button = tk.Button(t, text="Tex", command=self.call_tex)
            tex_button.grid(row=1, column=1, pady=5)

            col_desc = tk.Label(t, text="Calculate\n Column density")
            col_desc.grid(row=2, column=0, pady=5)

            col_button = tk.Button(t, text="NCol", command=self.call_col)
            col_button.grid(row=2, column=1, pady=5)

            bb_desc = tk.Label(t, text="Calculate\n Black Body Quantities")
            bb_desc.grid(row=3, column=0, pady=5)

            bb_button = tk.Button(t, text="BB", command=self.call_bb)
            bb_button.grid(row=3, column=1, pady=5)

            # iotext = tk.StringVar()
            # iotext.set("Type something here")
            # inputText = tk.Entry(t, textvariable=iotext)
            # inputText.grid(row=10,column=0,columnspan=3)

            finish = tk.Button(t, text="Close", fg="blue", command=lambda: self.cancel_LTE(t))
            finish.grid(row=11, column=0, columnspan=3)

    def call_tex(self):
        frame = tk.Toplevel(self)
        self.tex_window(frame)

    def call_col(self):
        frame = tk.Toplevel(self)
        self.col_window(frame)

    def call_bb(self):
        frame = tk.Toplevel(self)
        self.bb_window(frame)

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

    def grid_analysis(self):
        frame = tk.Toplevel(self)



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

    def cancel_LTE(self, t):
        self.lteOn -= 1
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

    def tex_window(self, frame):
        sv_pars = []
        parnames = aux.LTE.tex.parnames
        parsdesc = aux.LTE.tex.pardesc
        parexamp = aux.LTE.tex.parexam
        winName = tk.StringVar()
        text = tk.Label(frame, text='Window Name: ')
        text.grid(row=1, column=0, pady=5, padx=5, sticky='w')
        field = tk.Entry(frame, textvariable=winName)
        field.grid(row=1, column=1, pady=5, padx=5)
        givename = tk.Button(frame, text='Give name', command=lambda: self.name_window(winName, frame))
        givename.grid(row=1, column=2, pady=5, padx=5)
        for i in range(3):
            par = tk.StringVar()
            text = tk.Label(frame, text=parnames[i])
            text.grid(row=i + 2, column=0, pady=5, padx=5, sticky='w')
            field = tk.Entry(frame, textvariable=par)
            field.grid(row=i + 2, column=1, pady=5, padx=5)
            sv_pars.append(par)
        aux.Misc().help_button(frame, lambda: self.call_helper \
            (parnames[0], parsdesc[0], parexamp[0])) \
            .grid(row=2, column=2, padx=5, pady=5)
        aux.Misc().help_button(frame, lambda: self.call_helper \
            (parnames[1], parsdesc[1], parexamp[1])) \
            .grid(row=3, column=2, padx=5, pady=5)
        aux.Misc().help_button(frame, lambda: self.call_helper \
            (parnames[2], parsdesc[2], parexamp[2])) \
            .grid(row=4, column=2, padx=5, pady=5)
        texinst = aux.LTE.tex()
        calc_tex = tk.Button(frame, text='Calculate Tex', command=lambda: texinst.calculate_Tex(result_sv, *sv_pars))
        calc_tex.grid(row=5, column=1, pady=5, padx=5)
        result_sv = tk.StringVar()
        text = tk.Label(frame, text='Result: ')
        text.grid(row=6, column=0, pady=5, padx=5, sticky='w')
        field = tk.Entry(frame, textvariable=result_sv)
        field.grid(row=6, column=1, pady=5, padx=5)
        close_button = tk.Button(frame, text='Close Window', command=frame.destroy)
        close_button.grid(row=10, column=0, columnspan=2)

    def col_window(self, frame):
        frame.geometry('600x600')
        winName = tk.StringVar()
        text = tk.Label(frame, text='Window Name: ')
        text.grid(row=1, column=0, pady=5, padx=5, sticky='w')
        field = tk.Entry(frame, textvariable=winName)
        field.grid(row=1, column=1, pady=5, padx=5)
        givename = tk.Button(frame, text='Give name', command=lambda: self.name_window(winName, frame))
        givename.grid(row=1, column=2, pady=5, padx=5)
        options = ["Manual Input", "LAMDA File  "]
        modo = tk.StringVar()
        modo.set(options[0])
        mode_select = tk.OptionMenu(frame, modo, *options)
        mode_select.grid(row=2, padx=5, pady=5, column=0)
        go_mode = tk.Button(frame, text='Go!', command=lambda: self.call_column(modo, frame))
        go_mode.grid(row=2, padx=5, pady=5, column=1)
        close_button = tk.Button(frame, text='Close Window', command=frame.destroy)
        close_button.grid(row=30, column=0, columnspan=3)

    def call_column(self, modo, frame):
        modostr = modo.get()
        column_obj = aux.LTE.col()
        if modostr == "Manual Input":
            tk.Label(frame, text='Manual entry mode').grid(row=3)
            col_pars = []
            for i in range(len(column_obj.parnames)):
                par = tk.StringVar()
                col_pars.append(par)
                texto = tk.Label(frame, text=column_obj.parnames[i])
                texto.grid(row=4 + i, column=0, sticky='w', padx=5, pady=5)
                entrada = tk.Entry(frame, textvariable=par)
                entrada.grid(row=4 + i, column=1, sticky='w', padx=5, pady=5)
                help = aux.Misc().help_button(frame, lambda: self.call_helper(column_obj.parnames[i], "", ""))
                help.grid(row=4 + i, column=2, sticky='w', padx=5, pady=5)
        else:
            Misc().error_msg("Mode Not implemented yet.")


    def bb_window(self, frame):
        bb_ins = aux.LTE.bb()
        toptext = tk.Label(frame, text='Black body Quantities')
        toptext.grid(row=0, column=0, columnspan=5)
        frame.wm_title('Black body Quantities')
        bnulabel = tk.Label(frame, text='B_{nu}:')
        bnulabel.grid(row=1, column=0, columnspan=1, sticky='w')
        bnupars = []
        for i in range(3):
            par = tk.StringVar()
            tk.Label(frame, text=bb_ins.bnuNames[i]).grid(row=2, column=i, padx=5, pady=5)
            tk.Entry(frame, textvariable=par).grid(row=3, column=i, padx=5, pady=5)
            bnupars.append(par)
        gobnu = tk.Button(frame, text='Go!', command=lambda: self.status_check(bb_ins.decide_bnu_ibnu(bnupars)))
        gobnu.grid(row=3, column=4, padx=5, pady=5)
        helpbnu = aux.Misc().help_button(frame, frame.destroy)
        helpbnu.grid(row=3, column=5, padx=5, pady=5)

        jnulabel = tk.Label(frame, text='J_{nu}:')
        jnulabel.grid(row=4, column=0, columnspan=1, sticky='w')
        jnupars = []
        for i in range(3):
            par = tk.StringVar()
            tk.Label(frame, text=bb_ins.jnuNames[i]).grid(row=5, column=i, padx=5, pady=5)
            tk.Entry(frame, textvariable=par).grid(row=6, column=i, padx=5, pady=5)
            jnupars.append(par)
        gojnu = tk.Button(frame, text='Go!', command=lambda: self.status_check(bb_ins.decide_jnu_ijnu(jnupars)))
        gojnu.grid(row=6, column=4, padx=5, pady=5)
        helpjnu = aux.Misc().help_button(frame, frame.destroy)
        helpjnu.grid(row=6, column=5, padx=5, pady=5)

        emerglabel = tk.Label(frame, text='Emergent Intensity:')
        emerglabel.grid(row=7, column=0, columnspan=1, sticky='w')
        emergpars = []
        for i in range(4):
            par = tk.StringVar()
            tk.Label(frame, text=bb_ins.emergNames[i]).grid(row=8, column=i, padx=5, pady=5)
            tk.Entry(frame, textvariable=par).grid(row=9, column=i, padx=5, pady=5)
            emergpars.append(par)
        goemerg = tk.Button(frame, text='Go!', command=lambda: self.status_check(bb_ins.calc_emerging(emergpars)))
        goemerg.grid(row=9, column=4, padx=5, pady=5)
        helpemerg = aux.Misc().help_button(frame, frame.destroy)
        helpemerg.grid(row=9, column=5, padx=5, pady=5)

        close_button = tk.Button(frame, text='Close Window', command=frame.destroy)
        close_button.grid(row=10, column=0, columnspan=5, pady=5)

    def name_window(self, newname, frame):
        name = newname.get()
        frame.wm_title(name)

root = tk.Tk()
root.title("ChyExMachina Version: " + aux.version)
main = MainWindow(root)
main.pack(side="top", fill="both", expand=True)
root.mainloop()
