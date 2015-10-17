#!/usr/bin/python3
import numpy as np
from math import sqrt, cos
from scipy.optimize import leastsq


class pyenergy:
    def __init__(self):
        '''
            Should work for split phase, single phase, or 3 phase
        '''
        pass


    def calc(self, Voltage, Amperage, axis=1):
        '''
            Works but only about 5% accurate
        '''
        self.Vrms = np.sqrt(np.mean(np.square(Voltage), axis=axis))
        self.Arms = np.sqrt(np.mean(np.square(Amperage), axis=axis))
        self.VA = self.Vrms * self.Arms
        self.W = np.mean((Voltage * Amperage), axis=axis)
        self.PF = self.W / self.VA

    def calc2(self, time, Voltage, Amperage, axis=1):
        '''
            The reccomended calcs to use
        '''
        fitfunc = lambda C, t: C[0]*np.sin(C[1]*t+C[2])
        errfunc = lambda params, t, Y: fitfunc(params, t) - Y
        init_p = np.array([100.0, 60.0, 0.0])
        VC, success = leastsq(errfunc, init_p.copy(), args = (time, Voltage))
        AC, success = leastsq(errfunc, init_p.copy(), args = (time, Amperage))
        self.Vrms = VC[0]/sqrt(2)
        self.Arms = AC[0]/sqrt(2)
        self.VA = self.Vrms * self.Arms
        self.PF = abs(cos(AC[2]-VC[2]))
        self.W = self.VA * self.PF
