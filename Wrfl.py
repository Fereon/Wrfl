"""This is the main file of this project."""
__version__ = "0.1"
__author__ = "Fereon"

import formula
import interface

battle = formula.Battle()
app = interface.WrflGUI(battle)
app.mainloop()
