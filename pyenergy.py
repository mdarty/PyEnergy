#!/usr/bin/env python3
import numpy as np
from os import nice
from time import sleep
from math import sqrt, cos
from signal import signal, SIGINT
from scipy.optimize import leastsq
from multiprocessing import Process, Pipe


def signal_handler(signal, frame):
    global end
    end = True

global end
end = False
signal(SIGINT, signal_handler)


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


def worker(conn_time, conn_volt, conn_amps):
    nice(1)
    input_time.close()
    input_volt.close()
    input_amps.close()
    p = pyenergy()
    samples = 200
    time = [None] * samples
    Voltage = [None] * samples
    Amperage = [None] * samples
    while True:
        for i in range(samples):
            try:
                time[i] = conn_time.recv()
                Voltage[i] = conn_volt.recv()
                Amperage[i] = conn_amps.recv()
            except EOFError:
                return
        time = np.array(time)
        Voltage = np.array(Voltage)
        Amperage = np.array(Amperage)
        p.calc(time, np.transpose(Voltage), np.transpose(Amperage))
        print(time[199])


if __name__ == '__main__':
    output_time, input_time = Pipe(False)
    output_volt, input_volt = Pipe(False)
    output_amps, input_amps = Pipe(False)
    p = Process(target=worker, args=(output_time, output_volt, output_amps))
    p.start()
    Hz = 5000.0
    samples = 200
    d = 3.5
    w = np.array([60.0, 60.0, 60.0])
    theta = np.array([0.0, 0.0, 0.0])
    Vrms = np.array([117.0, 117.0, 117.0])
    Vpeak = Vrms*sqrt(2.0)
    APF = np.array([1.0, 0.85, 0.65])
    Atheta = np.arccos(APF)
    Arms = np.array([15.0, 15.0, 15.0])
    Apeak = Arms*sqrt(2.0)
    for t in range(10**10):
            input_time.send(t/samples)
            input_volt.send(Vpeak*np.sin(w*float(t)/samples+theta))
            input_amps.send(Apeak*np.sin(w*float(t)/samples+Atheta))
            if end:
                break
            sleep(1.0/Hz)
    input_time.close()
    input_volt.close()
    input_amps.close()
    p.join()
    print("\nExiting Gracefully")
