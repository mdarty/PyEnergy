#!/usr/bin/env python3
"""Testing PyEnergy"""
import unittest
from pyenergy import pyenergy
import numpy as np
from math import sin, sqrt

samples = 200
d = 3.5
w_all = np.array([60.0, 60.0, 60.0])
theta_all = np.array([0.0, 0.0, 0.0])
Vrms_all = np.array([117.0, 117.0, 117.0])
Vpeak_all = Vrms_all*sqrt(2.0)
time = np.array([t/samples for t in range(int(samples/d))])
V_list = []
for w, theta, Vpeak in zip(w_all, theta_all, Vpeak_all):
    V_list.append([Vpeak*sin(w*float(t)/samples+theta) for t in range(int(samples/d))])
V = np.array(V_list)

PF_all = np.array([1.0, 0.85, 0.65])
theta_all = np.arccos(PF_all)
Arms_all = np.array([15.0, 15.0, 15.0])
Apeak_all = Arms_all*sqrt(2.0)
A_list = []
for w, theta, Apeak in zip(w_all, theta_all, Apeak_all):
    A_list.append([Apeak*sin(w*float(t)/samples+theta) for t in range(int(samples/d))])
A = np.array(A_list)

p = pyenergy()
p.calc(time, V, A, axis=0)


class TestPyEnergy(unittest.TestCase):
    """Testing PyEnergy"""
    def setUp(self):
        """Setup Testing"""
        pass

    def test_Vrms(self):
        """Test Vrms"""
        for pVrms, Vrms in zip(p.Vrms, Vrms_all):
            self.assertEqual(round(pVrms), round(Vrms))

    def test_Arms(self):
        """Test Arms"""
        for pArms, Arms in zip(p.Arms, Arms_all):
            self.assertEqual(round(pArms), round(Arms))

    def test_VA(self):
        """Test VA"""
        for pVA, VA in zip(p.VA, Vrms_all*Arms_all):
            self.assertEqual(round(pVA), round(VA))

    def test_PF(self):
        """Test PF"""
        for pPF, PF in zip(p.PF, PF_all):
            self.assertEqual(round(pPF, 2), round(PF, 2))

    def test_W(self):
        """Test W"""
        for pW, W in zip(p.W, Vrms_all*Arms_all*PF_all):
            self.assertEqual(round(pW), round(abs(W)))

if __name__ == '__main__':
    unittest.main()
