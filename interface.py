"""This module contains all graphical user interface objects."""
__version__ = "0.1"
__author__ = "Fereon"

import tkinter as tk
from tkinter import ttk
import formula

class WrflGUI(tk.Tk):
    """Docstring"""
    def __init__(self, battle=formula.Battle()):
        """Initialization of GUI."""
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "Wrfl")
        tk.Tk.iconbitmap(self, default='Wrfl.ico')

        # Master Frame
        frame = tk.Frame(self)
        frame.grid(sticky="nwse")

        # Menubar
        menubar = tk.Menu(frame)
        menu = tk.Menu(menubar, tearoff=0)
        menu.add_command(label="Nach CSV exportieren")
        menu.add_command(label="Schließen", command=lambda: quit())
        menubar.add_cascade(label="Menü", menu=menu)
        tk.Tk.config(self, menu=menubar)

        # Labels, Sliders and Checkboxes
        labelplayermin = ttk.Label(frame, text="Spieler Minimum")
        labelplayermax = ttk.Label(frame, text="Spieler Maximum")
        labelplayerhp = ttk.Label(frame, text="Spieler Leben")
        labeltankmode = ttk.Label(frame, text="Tank Modus")
        labelenemymin = ttk.Label(frame, text="Gegner Minimum")
        labelenemymax = ttk.Label(frame, text="Gegner Maximum")

        labelplayermin.grid(row=0, column=0, sticky='w')
        labelplayermax.grid(row=1, column=0, sticky='w')
        labelplayerhp.grid(row=2, column=0, sticky='w')
        labeltankmode.grid(row=2, column=3, sticky='e')
        labelenemymin.grid(row=3, column=0, sticky='w')
        labelenemymax.grid(row=4, column=0, sticky='w')

        varplayermin = tk.IntVar()
        varplayermax = tk.IntVar()
        varplayerhp = tk.IntVar()
        varenemymin = tk.IntVar()
        varenemymax = tk.IntVar()

        varplayermin.set(battle.min_player)
        varplayermax.set(battle.max_player)
        varplayerhp.set(battle.player_hp)
        varenemymin.set(battle.min_enemy)
        varenemymax.set(battle.max_enemy)
        
        sliderlabelplayermin = ttk.Label(frame, textvariable=varplayermin)
        sliderlabelplayermax = ttk.Label(frame, textvariable=varplayermax)
        sliderlabelplayerhp = ttk.Label(frame, textvariable=varplayerhp)
        sliderlabelenemymin = ttk.Label(frame, textvariable=varenemymin)
        sliderlabelenemymax = ttk.Label(frame, textvariable=varenemymax)

        sliderlabelplayermin.grid(row=0, column=4, sticky='w')
        sliderlabelplayermax.grid(row=1, column=4, sticky='w')
        sliderlabelplayerhp.grid(row=2, column=2, sticky='w')
        sliderlabelenemymin.grid(row=3, column=4, sticky='w')
        sliderlabelenemymax.grid(row=4, column=4, sticky='w')

        sliderplayermin = ttk.Scale(frame, from_=1, to=30, value=battle.min_player, orient=tk.HORIZONTAL, length=200, command=lambda s:varplayermin.set(round(float(s))))
        sliderplayermax = ttk.Scale(frame, from_=1, to=30, value=battle.max_player, orient=tk.HORIZONTAL, length=200)
        sliderplayerhp = ttk.Scale(frame, from_=1, to=10, value=battle.player_hp, orient=tk.HORIZONTAL)
        sliderenemymin = ttk.Scale(frame, from_=1, to=30, value=battle.min_enemy, orient=tk.HORIZONTAL, length=200)
        sliderenemymax = ttk.Scale(frame, from_=1, to=30, value=battle.max_player, orient=tk.HORIZONTAL, length=200)

        sliderplayermin.grid(row=0, column=1, sticky='w', columnspan=3)
        sliderplayermax.grid(row=1, column=1, sticky='w', columnspan=3)
        sliderplayerhp.grid(row=2, column=1, sticky='w', columnspan=1)
        sliderenemymin.grid(row=3, column=1, sticky='w', columnspan=3)
        sliderenemymax.grid(row=4, column=1, sticky='w', columnspan=3)

        checktank = ttk.Checkbutton(frame)
        checktank.grid(row=2, column=4, sticky='w')