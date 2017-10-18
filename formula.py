"""This module contains mathematical functions and classes required for the project."""
__version__ = "0.8"
__author__ = "Fereon"

import math

def binomial_coefficient(n, k):
    """Returns the value for n choose k."""
    return math.factorial(n)/(math.factorial(k)*math.factorial(n-k))

def binomial_probability(n, k, p):
    """Returns the value P for the probabillity mass function P(k;n,p) = (n k) p^k (1-p)^n-k ."""
    return binomial_coefficient(n, k)*(p**k)*((1-p)**(n-k))

def binomial_distribution(n, k, p):
    """Returns the value F for the cumulative distribution function F(k,n,p)."""
    return sum([binomial_probability(n, i, p) for i in range(k+1)])

class Battle:
    """The Battle class is a tool to track, monitor and calculate events involving
    dices in an rpg scenario.""" 

    def __init__(self, minPlayer=1, maxPlayer=20, playerHP=3, minEnemy=1, maxEnemy=20, tankMode=False):
        """Initializes an instance of the Battle class."""
        self.min_player = minPlayer
        self.max_player = maxPlayer
        self.player_hp = playerHP
        self.min_enemy = minEnemy
        self.max_enemy = maxEnemy
        self.tank_mode = tankMode
        self.calculate()
    
    def change(self, **kwargs):
        """Changes and applies instance variables of Battle.
        Allowed keywords: min_player max_player player_hp min_enemy max_enemy"""
        for key, value in kwargs.items():
            if hasattr(self, key): setattr(self, key, value)
        self.calculate()
    
    def calculate(self):
        """Calculates the number of all the possible win, lose and stalemate events."""
        pevent, eevent, sevent = 0, 0, 0
        for playerdice in range(self.min_player, self.max_player+1):
            for enemydice in range(self.min_enemy-self.tank_mode, self.max_enemy+1-self.tank_mode):
                if playerdice > enemydice:
                    pevent = pevent+1
                elif playerdice < enemydice:
                    eevent = eevent+1
                else:
                    sevent = sevent+1
        self.event_player = pevent
        self.event_enemy = eevent
        self.event_stalemate = sevent

    def exportcsv(self):
        """Returns all values as String suitable to make a CSV file."""
        listrange = list(range(self.player_hp, self.player_hp+5))
        listresults = [self.expected_fall_distribution(t) for t in listrange]
        listtext = ";\n\nZüge;p Ausscheiden"
        for atem, btem in zip(listrange, listresults):
            listtext = listtext + ';\n' + str(atem) + ';' + str(btem)
        
        export = ["Kleinster Spielerwurf;" + str(self.min_player) + ";;Spielerereignisse;" + str(self.event_player) + ";;p Spieler;=E1/(E1+E2+E3)",
        ";\nGrößter Spielerwurf;" + str(self.max_player) + ";;Gegnerereignisse;" + str(self.event_enemy) + ";;p Gegner;=E2/(E1+E2+E3)",
        ";\nSpielerleben;" + str(self.player_hp) + ";;Gleichstand;" + str(self.event_stalemate) + ";;p Gleichstand;=E3/(E1+E2+E3)",
        ";\nKleinster Gegnerwurf;" + str(self.min_enemy) + ";;Total;=E1+E2+E3;;p SpielerEffektiv;=E1/(E1+E2)",
        ";\nGrößter Gegnerwurf;" + str(self.max_enemy) + ";;;;;p GegnerEffektiv;=E1/(E1+E2)",
        ";\nTank Modus;" + str(self.tank_mode), listtext + ';']

        return ''.join(export).replace('.', ',')

    def expected_fall_distribution(self, turn):
        """Returns the probability for sudden death after reaching a turn."""
        probability = self.event_enemy/(self.event_enemy+self.event_player)
        return 1-binomial_distribution(turn, self.player_hp-1, probability)