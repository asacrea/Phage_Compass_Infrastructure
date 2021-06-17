#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 11:45:03 2020

@author: andressacre
"""
import numpy as np
from time import time
from numba import njit
from concurrent.futures import ProcessPoolExecutor

x = np.random.random((10000,10000))
y = np.random.random((10000,10000))

def do_trig(x,y):
    z = np.sin(x**2) + np.cos(y)
    return z

start_time = time()
z = do_trig(x, x)
#Measure time
elapsed_time = time() - start_time
print(elapsed_time)


start_time = time()
do_trig_jit_par = njit(parallel=True)(do_trig)
do_trig_jit_par(x,y)
#Measure time
elapsed_time = time() - start_time
print(elapsed_time)
