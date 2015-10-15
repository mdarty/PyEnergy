#!/usr/bin/python3
import numpy as np


class pyenergy:
    def __init__(self):
        '''
            Should work for split phase, single phase, or 3 phase
        '''
        pass
    

    def calc(self, Voltage, Amperage, axis=1):
        self.Vrms = np.sqrt(np.mean(np.square(Voltage), axis=axis))
        self.Arms = np.sqrt(np.mean(np.square(Amperage), axis=axis))
        self.VA = self.Vrms * self.Arms
        self.W = np.mean(np.abs(Voltage) * np.abs(Amperage), axis=axis)
        self.PF = self.W / self.VA
