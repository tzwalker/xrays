# -*- coding: utf-8 -*-
"""
Created on Fri May 17 16:54:26 2019

@author: Trumann
"""
import numpy as np
import matplotlib.pyplot as plt

coeff = [-3.010e4, 0.0114, -0.179, 1.533, -7.637, 22.28, -35.406, 25.488, -4.409, 18.360]

NBL3_1_CuGradient = np.poly1d(coeff)

def eval_polynomial(polynomial,x):
    terms = [coefficient*x**i for i,coefficient in enumerate(polynomial)]
    ans = sum(terms)
    return ans

x = np.linspace(0, 12, 12001)

y = eval_polynomial(NBL3_1_CuGradient, x)

plt.semilogy(x, y)