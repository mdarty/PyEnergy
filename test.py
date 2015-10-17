#!/usr/bin/env python3
import unittest
from pyenergy import pyenergy
import numpy as np
from math import sin, sqrt, acos
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

w = 60.0
theta = 0.0
samples = 200
d = 3.5
Vrms = 117.0
Vpeak = Vrms*sqrt(2.0)
time = np.array([t/samples for t in range(int(samples/d))])
V = np.array([Vpeak*sin(w*float(t)/samples+theta) for t in range(int(samples/d))])
PF = 0.85
theta = acos(PF)
Arms = 15.0
Apeak = Arms*sqrt(2.0)
A = np.array([Apeak*sin(w*float(t)/samples+theta) for t in range(int(samples/d))])

p = pyenergy()
p.calc2(time, V, A, axis=0)


class TestPyEnergy(unittest.TestCase):
    def setUp(self):
        pass

    def test_Vrms(self):
        self.assertEqual(round(p.Vrms), round(Vrms))

    def test_Arms(self):
        self.assertEqual(round(p.Arms), round(Arms))

    def test_VA(self):
        self.assertEqual(round(p.VA), round(Vrms*Arms))

    def test_PF(self):
        self.assertEqual(round(p.PF, 2), round(PF, 2))

    def test_W(self):
        self.assertEqual(round(p.W), round(abs(Vrms*Arms*PF)))

if __name__ == '__main__':
        plt.plot(time, V/Vpeak)
        plt.plot(time, A/Apeak)
        plt.plot(time, (V/Vpeak * A/Apeak).clip(0))
        plt.savefig('pye.png')
        unittest.main()
