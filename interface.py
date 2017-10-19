"""This module contains all graphical user interface objects."""
__version__ = "0.8"
__author__ = "Fereon"

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import formula

class WrflGUI(tk.Tk):
    """Docstring"""
    def __init__(self, battle=formula.Battle()):
        """Initialization of GUI."""
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "Wrfl")
        tk.Tk.iconbitmap(self, default='Wrfl.ico')
        self.battle = battle

        # Master self.Frame
        self.frame = tk.Frame(self)
        self.frame.grid(sticky="nwse")

        # Plots
        self.figurepie = Figure(figsize=(3, 3), dpi=85)
        self.figurepieeff = Figure(figsize=(3, 3), dpi=85)
        self.figurebars = Figure(figsize=(5, 4), dpi=64)

        self.plotpie = self.figurepie.add_subplot(111)
        self.plotpieeff = self.figurepieeff.add_subplot(111)
        self.plotbars = self.figurebars.add_subplot(111)

        self.canvaspie = FigureCanvasTkAgg(self.figurepie, self)
        self.canvaspieeff = FigureCanvasTkAgg(self.figurepieeff, self)
        self.canvasbars = FigureCanvasTkAgg(self.figurebars, self)

        self.canvaspie.get_tk_widget().grid(row=0, column=5, rowspan=6)
        self.canvaspieeff.get_tk_widget().grid(row=6, column=5, sticky='nw')
        self.canvasbars.get_tk_widget().grid(row=6, column=0, columnspan=5, sticky='ne')

        self.redraw()

        # GUI elements
        self.managemenubar()
        self.managestaticlabels()
        self.managesliders()
        self.managecheckbox()

    def managemenubar(self):
        """Manages the menu bar."""
        menubar = tk.Menu(self.frame)
        menu = tk.Menu(menubar, tearoff=0)
        menu.add_command(label="Nach CSV exportieren", command=lambda: self.savexport())
        menu.add_command(label="Schließen", command=lambda: exit(0))
        menubar.add_cascade(label="Menü", menu=menu)
        tk.Tk.config(self, menu=menubar)

    def savexport(self):
        """Manages the saving of exports."""
        try: 
            export = filedialog.asksaveasfile(mode='w', title='Wrfl Export', defaultextension='.csv', filetypes=(("CVS Datei", "*.csv"),("Alle Datein", "*.*")))
            data = self.battle.exportcsv()
            export.write(data)
            export.close()
        except (AttributeError):
            pass

    def managestaticlabels(self):
        """Manages static labels."""
        labelplayermin = ttk.Label(self.frame, text="Spieler Minimum")
        labelplayermax = ttk.Label(self.frame, text="Spieler Maximum")
        labelplayerhp = ttk.Label(self.frame, text="Spieler Leben")
        labeltankmode = ttk.Label(self.frame, text="Tank Modus")
        labelenemymin = ttk.Label(self.frame, text="Gegner Minimum")
        labelenemymax = ttk.Label(self.frame, text="Gegner Maximum")

        labelplayermin.grid(row=0, column=0, sticky='w')
        labelplayermax.grid(row=1, column=0, sticky='w')
        labelplayerhp.grid(row=2, column=0, sticky='w')
        labeltankmode.grid(row=2, column=3, sticky='e')
        labelenemymin.grid(row=3, column=0, sticky='w')
        labelenemymax.grid(row=4, column=0, sticky='w')

    def managesliders(self):
        """Manages sliders and associated labels."""
        varplayermin = tk.IntVar()
        varplayermax = tk.IntVar()
        varplayerhp = tk.IntVar()
        varenemymin = tk.IntVar()
        varenemymax = tk.IntVar()

        varplayermin.set(self.battle.min_player)
        varplayermax.set(self.battle.max_player)
        varplayerhp.set(self.battle.player_hp)
        varenemymin.set(self.battle.min_enemy)
        varenemymax.set(self.battle.max_enemy)
        
        sliderlabelplayermin = ttk.Label(self.frame, textvariable=varplayermin)
        sliderlabelplayermax = ttk.Label(self.frame, textvariable=varplayermax)
        sliderlabelplayerhp = ttk.Label(self.frame, textvariable=varplayerhp)
        sliderlabelenemymin = ttk.Label(self.frame, textvariable=varenemymin)
        sliderlabelenemymax = ttk.Label(self.frame, textvariable=varenemymax)

        sliderlabelplayermin.grid(row=0, column=4, sticky='w')
        sliderlabelplayermax.grid(row=1, column=4, sticky='w')
        sliderlabelplayerhp.grid(row=2, column=2, sticky='w')
        sliderlabelenemymin.grid(row=3, column=4, sticky='w')
        sliderlabelenemymax.grid(row=4, column=4, sticky='w')

        def slidercommand(self, value, varlabel, battlevar):
            """Command invoked with sliders"""
            labelvalue = round(float(value))
            if labelvalue == varlabel.get(): return
            if (varlabel is varplayermin) and labelvalue > varplayermax.get(): sliderplayermax.set(labelvalue)
            elif (varlabel is varplayermax) and labelvalue < varplayermin.get(): sliderplayermin.set(labelvalue)
            elif (varlabel is varenemymin) and labelvalue > varenemymax.get(): sliderenemymax.set(labelvalue)
            elif (varlabel is varenemymax) and labelvalue < varenemymin.get(): sliderenemymin.set(labelvalue)
            keyword = {battlevar : labelvalue}
            varlabel.set(labelvalue)
            self.battle.change(**keyword)
            self.redraw()
        
        sliderplayermin = ttk.Scale(self.frame, from_=1, to=30, value=self.battle.min_player, orient=tk.HORIZONTAL, length=200,
        command=lambda s: slidercommand(self, s, varplayermin, 'min_player'))
        sliderplayermax = ttk.Scale(self.frame, from_=1, to=30, value=self.battle.max_player, orient=tk.HORIZONTAL, length=200,
        command=lambda s: slidercommand(self, s, varplayermax, 'max_player'))
        sliderplayerhp = ttk.Scale(self.frame, from_=1, to=10, value=self.battle.player_hp, orient=tk.HORIZONTAL,
        command=lambda s: slidercommand(self, s, varplayerhp, 'player_hp'))
        sliderenemymin = ttk.Scale(self.frame, from_=1, to=30, value=self.battle.min_enemy, orient=tk.HORIZONTAL, length=200,
        command=lambda s: slidercommand(self, s, varenemymin, 'min_enemy'))
        sliderenemymax = ttk.Scale(self.frame, from_=1, to=30, value=self.battle.max_player, orient=tk.HORIZONTAL, length=200,
        command=lambda s: slidercommand(self, s, varenemymax, 'max_enemy'))

        sliderplayermin.grid(row=0, column=1, sticky='w', columnspan=3)
        sliderplayermax.grid(row=1, column=1, sticky='w', columnspan=3)
        sliderplayerhp.grid(row=2, column=1, sticky='w', columnspan=1)
        sliderenemymin.grid(row=3, column=1, sticky='w', columnspan=3)
        sliderenemymax.grid(row=4, column=1, sticky='w', columnspan=3)

    def managecheckbox(self):
        """Manages the check box.""" 

        def checkcommand(variable):
            """Command invoked if checkbox is toggled."""
            if variable.get(): self.battle.change(tank_mode=True)
            else: self.battle.change(tank_mode=False)
            self.redraw()
        
        checkvar = tk.IntVar()
        checktank = ttk.Checkbutton(self.frame, variable=checkvar, command=lambda: checkcommand(checkvar))
        checktank.grid(row=2, column=4, sticky='w')        

    def redraw(self):
        self.plotpie.clear()
        self.plotpieeff.clear()
        self.plotbars.clear()

        self.plotpie.set_title("Trefferwahrscheinlichkeiten", verticalalignment='top')
        self.plotpieeff.set_title("Trefferwahrscheinlichkeiten:\nEffektiv", verticalalignment='top')

        self.plotbars.set_title("Ausscheidewahrscheinlichkeit nach Zug: Spieler")
        self.plotbars.set_xlabel("Zug")
        self.plotbars.set_ylabel("P in dezimal")

        self.plotpie.pie([self.battle.event_player, self.battle.event_stalemate, self.battle.event_enemy],
        colors=['#2ca02c','#ff7f0e', '#1f77b4'], startangle=90, labels=['Spieler', 'Gleichstand', 'Gegner'],
        autopct='%1.1f%%', radius=0.9)
        self.plotpieeff.pie([self.battle.event_player, self.battle.event_enemy], colors=['#2ca02c', '#1f77b4'],
        startangle=90,  labels=['Spieler', 'Gegner'], autopct='%1.1f%%', radius=0.9)
        listrange = list(range(self.battle.player_hp, self.battle.player_hp+5))
        listresults =[self.battle.expected_fall_distribution(t) for t in listrange]
        self.plotbars.bar(listrange, listresults, width=1, color='#2ca02c', tick_label=listrange)
        for a,b in zip(listrange, listresults):
            self.plotbars.text(a, b, '{:.1%}'.format(b))

        self.canvaspie.show()
        self.canvaspieeff.show()
        self.canvasbars.show()
