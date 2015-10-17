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

    def data_calc(self, Voltage, Amperage, axis=1):
        '''
            Works but only about 5% accurate
            This will be extremely fast
            if speed is a problem use this
        '''
        self.Vrms = np.sqrt(np.mean(np.square(Voltage), axis=axis))
        self.Arms = np.sqrt(np.mean(np.square(Amperage), axis=axis))
        self.VA = self.Vrms * self.Arms
        self.W = np.mean((Voltage * Amperage), axis=axis)
        self.PF = self.W / self.VA

    def reg_calc(self, time, Voltage, Amperage, phase, axis=1):
        '''
            The recommended calcs to use
            This only works with one phase
        '''
        fitfunc = lambda C, t: C[0]*np.sin(C[1]*t+C[2])
        errfunc = lambda params, t, Y: fitfunc(params, t) - Y
        init_p = np.array([100.0, 60.0, 0.0])
        VC, success = leastsq(errfunc, init_p.copy(), args=(time, Voltage))
        AC, success = leastsq(errfunc, init_p.copy(), args=(time, Amperage))
        self.Vrms[phase] = VC[0]/sqrt(2)
        self.Arms[phase] = AC[0]/sqrt(2)
        self.VA[phase] = self.Vrms[phase] * self.Arms[phase]
        self.PF[phase] = abs(cos(AC[2]-VC[2]))
        self.W[phase] = self.VA[phase] * self.PF[phase]

    def calc(self, time, Voltage, Amperage, axis=1):
        if Voltage.ndim > 1:
            phase = len(Voltage)
        else:
            phase = 1
        self.Vrms = np.zeros(phase)
        self.Arms = np.zeros(phase)
        self.VA = np.zeros(phase)
        self.PF = np.zeros(phase)
        self.W = np.zeros(phase)
        for i in range(phase):
            self.reg_calc(time, Voltage[i], Amperage[i], i)
