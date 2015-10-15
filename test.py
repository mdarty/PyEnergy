#!/usr/bin/env python3
import unittest
from pyenergy import pyenergy
import numpy as np
from math import sin, sqrt, cos, pi

w=60.0
theta=0.0
samples = 400
Vrms=117.0
Vpeak=Vrms*sqrt(2.0)
V = np.array([ Vpeak*sin(w*t/samples+theta) for t in range(samples) ])
theta=pi/4.0
Arms=15.0
Apeak=Arms*sqrt(2.0)
A = np.array([ Apeak*sin(w*t/samples+theta) for t in range(samples) ])

p = pyenergy()
p.calc(V, A, axis=0)

# print("{:.2f} V".format(p.Vrms))
# print("{:.2f} A".format(p.Arms))
# print("{:.2f} VA".format(p.VA))
# print("{:.2f} PF".format(p.PF))
# print("{:.2f} W".format(p.W))

class TestPyEnergy(unittest.TestCase):
    def setUp(self):
        pass

    def test_Vrms(self):
        self.assertEqual(round(p.Vrms), round(Vrms))

    def test_Arms(self):
        self.assertEqual(round(p.Arms), round(Arms))

    def test_VA(self):
        self.assertEqual(round(p.VA), round(Vrms*Arms))

    def test_W(self):
        self.assertEqual(round(p.W), round(abs(Vrms*Arms*cos(theta))))

if __name__ == '__main__':
        unittest.main()
