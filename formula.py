"""This module contains mathematical functions and classes required for the project."""
__version__ = "0.1"
__author__ = "Fereon"

import math

def binomial_coefficient(n, k):
    """Returns the value for n choose k."""
    return math.factorial(n)/(math.factorial(k)*math.factorial(n-k))

def binomial_probability(k, n, p):
    """Returns the value P for the probabillity mass function P(k;n,p) = (n k) p^k (1-p)^n-k ."""
    return binomial_coefficient(n, k)*(p**k)*((1-p)**(n-k))

def binomial_distribution(k, n, p):
    """Returns the value F for the cumulative distribution function F(k,n,p)."""
    return sum([binomial_probability(i, n, p) for i in range(1, k+1)])

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
            for enemydice in range(self.min_enemy, self.max_enemy+1-self.tank_mode):
                if playerdice > enemydice:
                    pevent = pevent+1
                elif playerdice < enemydice:
                    eevent = eevent+1
                else:
                    sevent = sevent+1
        self.event_enemy = pevent
        self.event_player = eevent
        self.event_stalemate = sevent
